# -*- coding: utf-8 -*-
"""Running the research team in the background, and recording what happened.

A run takes minutes, so it cannot happen inside a request. This module owns that
job: start a run, follow it stage by stage, and turn a finished result into a
draft in the approval queue.

It was inside app.py, which meant the web layer owned thread lifetimes, token
accounting and draft creation as well as routing. Out here it can be driven from
a script or a test without a server, and app.py is left doing what a routing
module should do — read the request, call one function, render the answer.

    start()    kick off a run, return its id immediately
    active()   which run ids are still going in this process

Progress is written to the database rather than held in memory, so the run page
can be reloaded, closed, or opened on another device, and a run that outlives the
request that started it still reports itself. The thread registry below is only
so the process knows what it has in flight; it is deliberately not the source of
truth about a run's state.
"""
import json
import threading
import time
import traceback

from . import publish, research, store

# run_id -> Thread, for runs started by this process. A restart empties it; the
# database still holds every run, which is why this is a convenience and not a
# record. A run left 'running' by a restart is a stale row, not a lost thread.
RUNNING = {}


def active():
    """Run ids still going in this process."""
    return sorted(RUNNING)


def _record_stages(run_id):
    """Persist each agent's output as it lands, and point `stage` at whoever is
    up next so the run page can show the rail without guessing."""
    def on_stage(name, output, seconds):
        store.add_stage(run_id, name, output, seconds)
        nxt = research.STAGES.index(name) + 1
        store.update_run(run_id, stage=research.STAGES[nxt]
                         if nxt < len(research.STAGES) else 'done')
    return on_stage


def _queue_draft(run_id, result):
    """A finished run -> a draft awaiting a human.

    The graded findings and the date ride along on the story under underscored
    keys. They are not part of what the writer produced, but the paper cannot be
    rendered without them and they must survive a prompt-based edit, so they are
    carried with the draft rather than recomputed later.
    """
    s = result['story']
    s['_findings'] = result['check']
    s['_date'] = time.strftime('%B %Y')
    return store.create_draft(
        s.get('slug') or publish.slugify(s.get('title')),
        s.get('lens', 'What'), s.get('domain', 'General'), s.get('title', ''),
        s, result['check'],
        notes=json.dumps({'checklist': result['checklist'],
                          'changes': result['changes'],
                          'ship': result['ship'],
                          'plan': result['plan']}, indent=1))


def _work(run_id, goal, lens_hint):
    try:
        store.update_run(run_id, stage='plan', state='running')
        result = research.run(goal, lens_hint, _record_stages(run_id),
                              lambda a, b: store.add_tokens(run_id, a, b))
        draft_id = _queue_draft(run_id, result)
        store.update_run(run_id, state='done', stage='done', draft_id=draft_id)
        store.log('run.done', f'run {run_id} -> draft {draft_id}')
    except Exception as exc:                      # noqa: BLE001 - shown to a human
        # Every failure mode here ends up in front of a person: a refusal, a
        # dropped premise, an expired login, a rate limit. Swallowing the type
        # and keeping the traceback is deliberate — the run page shows it.
        store.update_run(run_id, state='failed',
                         error=f'{exc}\n\n{traceback.format_exc()[-1500:]}')
        store.log('run.failed', str(exc)[:400])
    finally:
        RUNNING.pop(run_id, None)


def start(goal, lens_hint=''):
    """Begin a run and return its id straight away. The caller redirects to the
    run page; the work carries on without it."""
    run_id = store.create_run(goal, lens_hint)
    thread = threading.Thread(target=_work, args=(run_id, goal, lens_hint),
                              daemon=True)
    RUNNING[run_id] = thread
    thread.start()
    store.log('run.start', goal[:200])
    return run_id
