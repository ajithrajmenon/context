# -*- coding: utf-8 -*-
"""Starting a research run, and watching it happen."""
from fastapi import APIRouter, Form, Request

from .. import backend, research, runner, store
from ..config import PREFIX
from ..session import authed, go, login_redirect
from ..ui import e, page, progress_log, rail, state_pill

router = APIRouter()


@router.get(PREFIX + '/generate')
def generate_form(request: Request, m: str = ''):
    if not authed(request):
        return login_redirect()
    kind, label = backend.describe()
    if kind == 'none':
        warn = (f'<div class="card"><b>No way to reach Claude.</b>'
                f'<p class="muted">{e(label)}</p></div>')
    else:
        warn = (f'<div class="card"><span class="pill ok">{e(kind)}</span> '
                f'{e(label)}</div>')
    return page('Generate', f"""{warn}
<p class="sub">Give the team a research goal. Six agents work it in order —
Planner, Search, Reader, Fact Checker, Writer, Editor — and the result lands in
the approval queue. Nothing publishes without you.</p>
<form method="post" action="{PREFIX}/generate" class="card">
<label for="goal">Research goal</label>
<textarea id="goal" name="goal" placeholder="Why does bread go stale faster in the fridge than on the counter?"></textarea>
<label for="lens">Lens (optional — the Planner decides if you leave it blank)</label>
<select id="lens" name="lens_hint">
<option value="">Let the Planner choose</option>
<option>What</option><option>Why</option><option>How</option><option>What if</option>
</select>
<p></p><button type="submit">Send it to the team</button></form>
<p class="muted">A run takes several minutes. On the CLI backend it draws on your
Claude subscription's usage allowance; on the API backend it bills tokens. It runs
in the background — you can leave this page.</p>""", '/generate', m)


@router.post(PREFIX + '/generate')
def generate(request: Request, goal: str = Form(...), lens_hint: str = Form('')):
    if not authed(request):
        return login_redirect()
    goal = goal.strip()
    if not goal:
        return go('/generate', 'Give the team something to research.')
    return go(f'/run/{runner.start(goal, lens_hint)}')


@router.get(PREFIX + '/runs')
def runs(request: Request, m: str = ''):
    if not authed(request):
        return login_redirect()
    rows = ''.join(
        f'<tr><td><a href="{PREFIX}/run/{r["id"]}">{e(r["goal"][:80])}</a></td>'
        f'<td>{state_pill(r["state"])}</td><td class="muted">{e(r["stage"])}</td>'
        f'<td class="right muted">{r["cost_in"] + r["cost_out"]:,} tok</td></tr>'
        for r in store.list_runs())
    return page('Runs', f'<table><tr><th>Goal</th><th>State</th><th>Stage</th>'
                f'<th class="right">Tokens</th></tr>{rows or ""}</table>', '/runs', m)


@router.get(PREFIX + '/run/{run_id}')
def run_detail(request: Request, run_id: int, m: str = ''):
    if not authed(request):
        return login_redirect()
    r = store.get_run(run_id)
    if not r:
        return page('Not found', '<div class="card">No such run.</div>')
    seconds = {s['name']: s['seconds'] for s in store.run_stages(run_id)}
    progress = rail(research.STAGES, seconds, r['stage'], r['state'])
    # Once a run is no longer going, run_stage below already holds the real,
    # complete output of every stage — the live tail would just repeat it.
    live = progress_log(store.run_progress(run_id)) if r['state'] == 'running' else ''

    stages = ''.join(
        f'<h2>{s["name"].title()} <span class="muted" style="font-weight:400">'
        f'{s["seconds"]:.0f}s</span></h2><pre>{e(s["output"])}</pre>'
        for s in store.run_stages(run_id))

    err = f'<div class="card"><b>Failed.</b><pre>{e(r["error"])}</pre></div>' if r['error'] else ''
    link = (f'<p><a class="btn" href="{PREFIX}/draft/{r["draft_id"]}">'
            f'Open the draft</a></p>' if r['draft_id'] else '')
    # A run outlives the request that started it, so the page reloads itself
    # while it is going and stops the moment it is not.
    poll = ('<script>setTimeout(function(){location.reload()},5000)</script>'
            if r['state'] == 'running' else '')
    total = sum(seconds.values())
    elapsed = (f' &#183; {total / 60:.0f} min so far' if total >= 90
               else f' &#183; {total:.0f}s so far' if total else '')
    return page(r['goal'][:70], f"""
<p class="sub">{e(r['cost_in'] + r['cost_out']):} tokens{elapsed}.</p>
{progress}{live}{err}{link}{stages}{poll}""", '/runs', m)
