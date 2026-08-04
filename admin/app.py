# -*- coding: utf-8 -*-
"""[Context] backoffice.

Everything behind one unguessable path prefix *and* a password. The prefix
keeps the door out of logs and crawlers; the password is what actually stops
anyone. Obscurity is not access control, so both are required and neither is
optional.

Run it:

    export CONTEXT_ADMIN_PASSWORD='...'        # required
    export CONTEXT_ADMIN_PREFIX='/x7fq...'     # required, unguessable
    export ANTHROPIC_API_KEY='sk-ant-...'      # required for generation
    uvicorn admin.app:app --host 127.0.0.1 --port 8800

The API key lives here, server-side, and never reaches a browser.
"""
import asyncio
import hashlib
import hmac
import html
import json
import os
import threading
import time
import traceback

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse

from . import backend, publish, research, store

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _load_env():
    """Read admin/.env if it exists, so settings survive closing the terminal.

    Real environment variables always win — a value already exported is a
    deliberate act and should not be silently overridden by a checked-in file.
    """
    path = os.path.join(ROOT, 'admin', '.env')
    try:
        with open(path, encoding='utf-8') as fh:
            lines = fh.readlines()
    except OSError:
        return
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, _, value = line.partition('=')
        key, value = key.strip(), value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_env()

PREFIX = os.environ.get('CONTEXT_ADMIN_PREFIX', '/backoffice').rstrip('/')
PASSWORD = os.environ.get('CONTEXT_ADMIN_PASSWORD', '')
SECURE_COOKIE = os.environ.get('CONTEXT_ADMIN_INSECURE_COOKIE', '') != '1'
COOKIE = 'ctx_admin'

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
store.init()


# ---------------------------------------------------------------- chrome

CSS = """
:root{--page:#fff;--surface:#F7F9FC;--ink:#101828;--muted:#5A6875;
--border:#E6EAF2;--accent:#6D28D9;--r:14px}
*{box-sizing:border-box}
body{margin:0;background:var(--page);color:var(--ink);font:16px/1.6 system-ui,sans-serif}
a{color:var(--accent)}
.bar{display:flex;gap:1.2rem;align-items:center;padding:.9rem 1.4rem;
border-bottom:1px solid var(--border);flex-wrap:wrap}
.bar b{font-size:1.05rem}.bar a{text-decoration:none;color:var(--muted);font-weight:600}
.bar a.on{color:var(--ink)}.bar .sp{margin-left:auto}
.wrap{width:min(64rem,100% - 2.5rem);margin:1.8rem auto}
h1{font-size:1.6rem;margin:0 0 .3rem}h2{font-size:1.15rem;margin:1.8rem 0 .6rem}
p.sub{color:var(--muted);margin:0 0 1.4rem}
table{width:100%;border-collapse:collapse;font-size:.94rem}
th,td{text-align:left;padding:.6rem .5rem;border-bottom:1px solid var(--border);
vertical-align:top}
th{color:var(--muted);font-size:.76rem;text-transform:uppercase;letter-spacing:.07em}
.card{border:1px solid var(--border);border-radius:var(--r);padding:1.1rem 1.2rem;
margin-bottom:1rem;background:var(--page)}
input,textarea,select{font:inherit;width:100%;padding:.6rem .7rem;
border:1px solid var(--border);border-radius:10px;background:var(--page);color:var(--ink)}
textarea{min-height:6rem;resize:vertical}
label{display:block;font-weight:600;font-size:.86rem;margin:.9rem 0 .3rem}
button,.btn{font:inherit;font-weight:600;padding:.55rem 1rem;border-radius:999px;
border:1px solid var(--accent);background:var(--accent);color:#fff;cursor:pointer;
text-decoration:none;display:inline-block}
.btn.ghost,button.ghost{background:transparent;color:var(--accent)}
.btn.danger,button.danger{background:#B91C1C;border-color:#B91C1C;color:#fff}
.pill{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.08em;
padding:.15rem .5rem;border-radius:999px;background:var(--surface);color:var(--muted)}
.pill.ok{background:#DCFCE7;color:#166534}.pill.warn{background:#FEF3C7;color:#92400E}
.pill.bad{background:#FEE2E2;color:#991B1B}.pill.go{background:#EDE9FE;color:#5B21B6}
pre{background:var(--surface);border:1px solid var(--border);border-radius:10px;
padding:.8rem;overflow:auto;font-size:.82rem;max-height:26rem;white-space:pre-wrap}
.row{display:flex;gap:.5rem;align-items:center;flex-wrap:wrap}
.muted{color:var(--muted)}.right{text-align:right}
.stage{display:flex;gap:.6rem;align-items:center;padding:.45rem 0;
border-bottom:1px solid var(--border)}
.dot{width:.6rem;height:.6rem;border-radius:50%;background:var(--border);flex:none}
.dot.done{background:#16A34A}.dot.live{background:var(--accent);
animation:p 1.1s ease-in-out infinite}
@keyframes p{50%{opacity:.3}}
"""


def e(x):
    return html.escape(str(x if x is not None else ''))


def page(title, body, nav='', message=''):
    tabs = [('', 'Dashboard'), ('/stories', 'Stories'), ('/generate', 'Generate'),
            ('/queue', 'Queue'), ('/runs', 'Runs')]
    links = ''.join(
        f'<a class="{"on" if nav == p else ""}" href="{PREFIX}{p or "/"}">{n}</a>'
        for p, n in tabs)
    msg = f'<div class="card"><b>{e(message)}</b></div>' if message else ''
    return HTMLResponse(f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{e(title)} — [Context]</title>
<style>{CSS}</style></head><body>
<div class="bar"><b>[Context]</b>{links}
<span class="sp"></span>
<a href="{PREFIX}/logout">Sign out</a></div>
<div class="wrap"><h1>{e(title)}</h1>{msg}{body}</div></body></html>""")


def authed(request):
    return store.session_ok(request.cookies.get(COOKIE))


def login_redirect():
    return RedirectResponse(PREFIX + '/login', status_code=303)


def go(path, msg=''):
    sep = '&' if '?' in path else '?'
    url = PREFIX + path + (f'{sep}m={msg}' if msg else '')
    return RedirectResponse(url, status_code=303)


# ---------------------------------------------------------------- auth

@app.get(PREFIX + '/login')
def login_form(request: Request, bad: int = 0):
    if not PASSWORD:
        return page('Not configured', '<div class="card">Set '
                    '<code>CONTEXT_ADMIN_PASSWORD</code> before starting the '
                    'backoffice. It will not run open.</div>')
    warn = '<p class="muted">That password was not right.</p>' if bad else ''
    return page('Sign in', f"""{warn}
<form method="post" action="{PREFIX}/login" class="card" style="max-width:24rem">
<label for="pw">Password</label>
<input id="pw" name="password" type="password" autofocus autocomplete="current-password">
<p></p><button type="submit">Sign in</button></form>""")


@app.post(PREFIX + '/login')
def login(response_password: str = Form('', alias='password')):
    # Constant-time compare: a timing side channel on the one secret guarding
    # everything is not a theoretical concern.
    ok = PASSWORD and hmac.compare_digest(
        hashlib.sha256(response_password.encode()).digest(),
        hashlib.sha256(PASSWORD.encode()).digest())
    if not ok:
        store.log('login.failed')
        time.sleep(1.0)
        return RedirectResponse(PREFIX + '/login?bad=1', status_code=303)
    token = store.new_session()
    store.log('login.ok')
    resp = RedirectResponse(PREFIX + '/', status_code=303)
    resp.set_cookie(COOKIE, token, httponly=True, samesite='lax',
                    secure=SECURE_COOKIE, max_age=store.SESSION_TTL, path=PREFIX)
    return resp


@app.get(PREFIX + '/logout')
def logout(request: Request):
    store.drop_session(request.cookies.get(COOKIE))
    resp = login_redirect()
    resp.delete_cookie(COOKIE, path=PREFIX)
    return resp


# ---------------------------------------------------------------- dashboard

def _site_stories():
    """Read the live site's story list fresh — the modules are the truth about
    what is published, and they change under us when content is written."""
    import importlib
    import stories_data
    importlib.reload(stories_data)
    return stories_data.STORIES


@app.get(PREFIX + '/')
@app.get(PREFIX)
def dashboard(request: Request, m: str = ''):
    if not authed(request):
        return login_redirect()
    queued = store.list_drafts('queued')
    runs = store.list_runs(6)
    live = len(_site_stories())
    hidden = sum(1 for v in publish.read_visibility().values() if not v)
    gen = len(os.listdir(publish.STORIES)) if os.path.isdir(publish.STORIES) else 0

    rows = ''.join(
        f'<tr><td><a href="{PREFIX}/draft/{d["id"]}">{e(d["title"] or d["slug"])}</a></td>'
        f'<td><span class="pill go">{e(d["lens"])}</span></td>'
        f'<td class="muted">{e(d["domain"])}</td></tr>' for d in queued[:8])
    run_rows = ''.join(
        f'<tr><td><a href="{PREFIX}/run/{r["id"]}">{e(r["goal"][:70])}</a></td>'
        f'<td><span class="pill {"ok" if r["state"] == "done" else "bad" if r["state"] == "failed" else "warn"}">'
        f'{e(r["state"])}</span></td><td class="muted">{e(r["stage"])}</td></tr>'
        for r in runs)

    kind, label = backend.describe()
    badge = (f'<div class="card"><span class="pill {"ok" if kind != "none" else "bad"}">'
             f'{e(kind)}</span> {e(label)}</div>')
    return page('Dashboard', f"""{badge}
<div class="row" style="gap:1rem">
  <div class="card" style="flex:1"><b style="font-size:1.8rem">{live}</b>
    <div class="muted">live on the site</div></div>
  <div class="card" style="flex:1"><b style="font-size:1.8rem">{len(queued)}</b>
    <div class="muted">awaiting approval</div></div>
  <div class="card" style="flex:1"><b style="font-size:1.8rem">{gen}</b>
    <div class="muted">generated &amp; published</div></div>
  <div class="card" style="flex:1"><b style="font-size:1.8rem">{hidden}</b>
    <div class="muted">hidden</div></div>
</div>
<h2>Waiting for you</h2>
<table><tr><th>Story</th><th>Lens</th><th>Domain</th></tr>
{rows or '<tr><td colspan="3" class="muted">Nothing in the queue.</td></tr>'}</table>
<h2>Recent runs</h2>
<table><tr><th>Goal</th><th>State</th><th>Stage</th></tr>
{run_rows or '<tr><td colspan="3" class="muted">No runs yet.</td></tr>'}</table>
<p><a class="btn" href="{PREFIX}/generate">Start a research run</a></p>""", '', m)


# ---------------------------------------------------------------- stories

@app.get(PREFIX + '/stories')
def stories(request: Request, m: str = ''):
    if not authed(request):
        return login_redirect()
    vis = publish.read_visibility()
    generated = set()
    if os.path.isdir(publish.STORIES):
        generated = {f[:-5] for f in os.listdir(publish.STORIES) if f.endswith('.json')}

    live = {s['slug']: s for s in _site_stories()}
    # A hidden story is absent from STORIES, so read the union from disk.
    all_slugs = sorted(set(live) | set(vis) | generated)

    rows = ''
    for slug in all_slugs:
        s = live.get(slug)
        shown = vis.get(slug, True)
        title = s['title'] if s else slug
        lens = s.get('lens', '—') if s else '—'
        origin = 'generated' if slug in generated else 'hand-written'
        action = 'hide' if shown else 'show'
        rows += f"""<tr><td><b>{e(title)}</b><br><span class="muted">{e(slug)}</span></td>
<td><span class="pill go">{e(lens)}</span></td>
<td><span class="pill">{origin}</span></td>
<td><span class="pill {'ok' if shown else 'bad'}">{'visible' if shown else 'hidden'}</span></td>
<td class="right"><form method="post" action="{PREFIX}/stories/visibility" class="row">
<input type="hidden" name="slug" value="{e(slug)}">
<input type="hidden" name="visible" value="{'0' if shown else '1'}">
<button class="ghost" type="submit">{action.title()}</button></form></td></tr>"""

    return page('Stories', f"""
<p class="sub">Every story on the site. Hiding takes one off the site without
deleting it — the file and its history stay. Changes go live on the next publish.</p>
<table><tr><th>Story</th><th>Lens</th><th>Origin</th><th>State</th><th></th></tr>
{rows}</table>
<h2>Push visibility changes</h2>
<form method="post" action="{PREFIX}/publish-site" class="card">
<p class="muted" style="margin-top:0">Rebuilds the site and pushes. Pages redeploys itself.</p>
<button type="submit">Rebuild and push</button></form>""", '/stories', m)


@app.post(PREFIX + '/stories/visibility')
def set_visibility(request: Request, slug: str = Form(...), visible: str = Form('1')):
    if not authed(request):
        return login_redirect()
    publish.set_visible(slug, visible == '1')
    store.log('visibility', f'{slug} -> {"visible" if visible == "1" else "hidden"}')
    return go('/stories', 'Saved. Rebuild and push to make it live.')


@app.post(PREFIX + '/publish-site')
def publish_site(request: Request):
    if not authed(request):
        return login_redirect()
    ok, log = publish.commit_and_push('Update story visibility')
    store.log('publish.site', log[-500:])
    return page('Publish', f'<pre>{e(log)}</pre>'
                f'<p><a class="btn" href="{PREFIX}/stories">Back to stories</a></p>',
                '/stories', 'Published.' if ok else 'Publish failed — see the log.')


# ---------------------------------------------------------------- generate

RUNNING = {}


@app.get(PREFIX + '/generate')
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


def _worker(run_id, goal, lens_hint):
    def on_stage(name, output, seconds):
        store.add_stage(run_id, name, output, seconds)
        nxt = research.STAGES.index(name) + 1
        store.update_run(run_id, stage=research.STAGES[nxt]
                         if nxt < len(research.STAGES) else 'done')

    try:
        store.update_run(run_id, stage='plan', state='running')
        result = research.run(goal, lens_hint, on_stage,
                              lambda a, b: store.add_tokens(run_id, a, b))
        s = result['story']
        s['_findings'] = result['check']
        s['_date'] = time.strftime('%B %Y')
        draft_id = store.create_draft(
            s.get('slug') or publish.slugify(s.get('title')),
            s.get('lens', 'What'), s.get('domain', 'General'), s.get('title', ''),
            s, result['check'],
            notes=json.dumps({'checklist': result['checklist'],
                              'changes': result['changes'],
                              'ship': result['ship'],
                              'plan': result['plan']}, indent=1))
        store.update_run(run_id, state='done', stage='done', draft_id=draft_id)
        store.log('run.done', f'run {run_id} -> draft {draft_id}')
    except Exception as exc:                      # noqa: BLE001 - shown to a human
        store.update_run(run_id, state='failed',
                         error=f'{exc}\n\n{traceback.format_exc()[-1500:]}')
        store.log('run.failed', str(exc)[:400])
    finally:
        RUNNING.pop(run_id, None)


@app.post(PREFIX + '/generate')
def generate(request: Request, goal: str = Form(...), lens_hint: str = Form('')):
    if not authed(request):
        return login_redirect()
    goal = goal.strip()
    if not goal:
        return go('/generate', 'Give the team something to research.')
    run_id = store.create_run(goal, lens_hint)
    t = threading.Thread(target=_worker, args=(run_id, goal, lens_hint), daemon=True)
    RUNNING[run_id] = t
    t.start()
    store.log('run.start', goal[:200])
    return go(f'/run/{run_id}')


@app.get(PREFIX + '/runs')
def runs(request: Request, m: str = ''):
    if not authed(request):
        return login_redirect()
    rows = ''.join(
        f'<tr><td><a href="{PREFIX}/run/{r["id"]}">{e(r["goal"][:80])}</a></td>'
        f'<td><span class="pill {"ok" if r["state"] == "done" else "bad" if r["state"] == "failed" else "warn"}">'
        f'{e(r["state"])}</span></td><td class="muted">{e(r["stage"])}</td>'
        f'<td class="right muted">{r["cost_in"] + r["cost_out"]:,} tok</td></tr>'
        for r in store.list_runs())
    return page('Runs', f'<table><tr><th>Goal</th><th>State</th><th>Stage</th>'
                f'<th class="right">Tokens</th></tr>{rows or ""}</table>', '/runs', m)


@app.get(PREFIX + '/run/{run_id}')
def run_detail(request: Request, run_id: int, m: str = ''):
    if not authed(request):
        return login_redirect()
    r = store.get_run(run_id)
    if not r:
        return page('Not found', '<div class="card">No such run.</div>')
    done = {s['name'] for s in store.run_stages(run_id)}
    rows = ''
    for name in research.STAGES:
        state = 'done' if name in done else ('live' if r['stage'] == name
                                             and r['state'] == 'running' else '')
        rows += (f'<div class="stage"><span class="dot {state}"></span>'
                 f'<b>{name.title()}</b><span class="sp"></span></div>')

    stages = ''.join(
        f'<h2>{s["name"].title()} <span class="muted" style="font-weight:400">'
        f'{s["seconds"]:.0f}s</span></h2><pre>{e(s["output"])}</pre>'
        for s in store.run_stages(run_id))

    err = f'<div class="card"><b>Failed.</b><pre>{e(r["error"])}</pre></div>' if r['error'] else ''
    link = (f'<p><a class="btn" href="{PREFIX}/draft/{r["draft_id"]}">'
            f'Open the draft</a></p>' if r['draft_id'] else '')
    poll = ('<script>setTimeout(function(){location.reload()},5000)</script>'
            if r['state'] == 'running' else '')
    return page(r['goal'][:70], f"""
<p class="sub">{e(r['cost_in'] + r['cost_out']):} tokens so far.</p>
<div class="card">{rows}</div>{err}{link}{stages}{poll}""", '/runs', m)


# ---------------------------------------------------------------- queue

@app.get(PREFIX + '/queue')
def queue(request: Request, m: str = ''):
    if not authed(request):
        return login_redirect()
    rows = ''
    for d in store.list_drafts():
        if d['status'] in ('published', 'rejected'):
            continue
        rows += (f'<tr><td><a href="{PREFIX}/draft/{d["id"]}">'
                 f'{e(d["title"] or d["slug"])}</a><br>'
                 f'<span class="muted">{e(d["slug"])}</span></td>'
                 f'<td><span class="pill go">{e(d["lens"])}</span></td>'
                 f'<td class="muted">{e(d["domain"])}</td>'
                 f'<td><span class="pill warn">{e(d["status"])}</span></td></tr>')
    return page('Approval queue', f"""
<p class="sub">Drafts the research team has finished. Read, edit by prompt if
something is off, then approve — approving publishes and pushes.</p>
<table><tr><th>Story</th><th>Lens</th><th>Domain</th><th>Status</th></tr>
{rows or '<tr><td colspan="4" class="muted">Empty.</td></tr>'}</table>""", '/queue', m)


def _preview(s):
    d1, d2 = s.get('diagram_one', {}), s.get('diagram_two', {})
    return f"""
<div class="card"><span class="pill go">{e(s.get('lens'))}</span>
<span class="pill">{e(s.get('domain'))}</span>
<h2 style="margin-top:.6rem">{e(s.get('title'))}</h2>
<p>{e(s.get('teaser'))}</p>
<p class="muted"><b>You will come away knowing:</b> {e(s.get('takeaway'))}</p>
<p class="muted"><b>Standfirst:</b> {e(s.get('standfirst'))}</p></div>

<div class="card"><b>1 · Wrong picture — {e(s.get('wrong_head'))}</b>
<p>{e(s.get('wrong_body'))}</p></div>
<div class="card"><b>2 · Diagram — {e(d1.get('kind'))}: {e(d1.get('title'))}</b>
<p class="muted">{e(d1.get('sub'))}</p><pre>{e(d1.get('data'))}</pre>
<p class="muted">{e(d1.get('caption'))}</p></div>
<div class="card"><b>3 · Crack — {e(s.get('crack_head'))}</b>
<p>{e(s.get('crack_body'))}</p></div>
<div class="card" style="background:var(--surface)"><b>4 · The Turn</b>
<p style="font-size:1.15rem"><b>{e(s.get('turn'))}</b></p></div>
<div class="card"><b>5 · Diagram — {e(d2.get('kind'))}: {e(d2.get('title'))}</b>
<p class="muted">{e(d2.get('sub'))}</p><pre>{e(d2.get('data'))}</pre>
<p class="muted">{e(d2.get('caption'))}</p></div>
<div class="card"><b>6 · Cost — {e(s.get('cost_head'))}</b>
<p>{e(s.get('cost_body'))}</p></div>
<div class="card"><b>7 · Long view</b><p>{e(s.get('zoomout'))}</p></div>
<div class="card"><b>Paper</b><p class="muted">{e(s.get('paper_subtitle'))}</p>
<p>{e(s.get('paper_abstract'))}</p>
<p class="muted"><b>Method:</b> {e(s.get('method'))}</p></div>"""


@app.get(PREFIX + '/draft/{draft_id}')
def draft_detail(request: Request, draft_id: int, m: str = ''):
    if not authed(request):
        return login_redirect()
    d = store.get_draft(draft_id)
    if not d:
        return page('Not found', '<div class="card">No such draft.</div>')
    s = json.loads(d['story_json'])
    check = json.loads(d['paper_json'] or '{}')
    notes = json.loads(d['notes'] or '{}')

    checklist = ''.join(
        f'<div class="stage"><span class="pill {"ok" if c.get("pass") else "bad"}">'
        f'{"pass" if c.get("pass") else "fail"}</span> {e(c.get("item"))} '
        f'<span class="muted">{e(c.get("note"))}</span></div>'
        for c in notes.get('checklist', []))

    findings = ''.join(
        f'<tr><td>{e(f.get("claim"))}</td>'
        f'<td><span class="pill {"ok" if f.get("confidence") == "established" else "warn"}">'
        f'{e(f.get("confidence"))}</span></td>'
        f'<td class="muted">{e(f.get("basis"))}</td></tr>'
        for f in check.get('findings', []))

    edits = ''.join(
        f'<div class="stage"><span class="muted">'
        f'{time.strftime("%d %b %H:%M", time.localtime(x["created_at"]))}</span> '
        f'{e(x["prompt"])}</div>' for x in store.draft_edits(draft_id))

    discarded = ''.join(f'<li>{e(x)}</li>' for x in check.get('discarded', []))

    return page(s.get('title', d['slug']), f"""
{_preview(s)}
<h2>Prompt-based edit</h2>
<form method="post" action="{PREFIX}/draft/{draft_id}/revise" class="card">
<p class="muted" style="margin-top:0">Say what to change in plain English. The
Editor applies it and returns the whole draft.</p>
<textarea name="instruction" placeholder="Make the Turn sharper and cut the last sentence of the Cost section."></textarea>
<p></p><button type="submit">Apply edit</button></form>
{f'<h2>Edits so far</h2><div class="card">{edits}</div>' if edits else ''}

<h2>Editor's checklist</h2><div class="card">{checklist or '<span class="muted">None recorded.</span>'}</div>
<h2>Graded findings</h2>
<table><tr><th>Claim</th><th>Confidence</th><th>Basis</th></tr>{findings}</table>
{f'<h2>Discarded by the fact checker</h2><div class="card"><ul>{discarded}</ul></div>' if discarded else ''}

<h2>Decide</h2>
<div class="card"><div class="row">
<form method="post" action="{PREFIX}/draft/{draft_id}/approve">
<button type="submit">Approve &amp; publish</button></form>
<form method="post" action="{PREFIX}/draft/{draft_id}/reject">
<button class="danger" type="submit">Reject</button></form>
</div><p class="muted">Approving writes the story into <code>content/</code>,
rebuilds the site, commits and pushes. Pages redeploys itself.</p></div>""",
                '/queue', m)


@app.post(PREFIX + '/draft/{draft_id}/revise')
def revise(request: Request, draft_id: int, instruction: str = Form(...)):
    if not authed(request):
        return login_redirect()
    d = store.get_draft(draft_id)
    if not d:
        return go('/queue', 'No such draft.')
    before = json.loads(d['story_json'])
    try:
        after, changes = research.revise(before, instruction.strip())
    except Exception as exc:                      # noqa: BLE001 - shown to a human
        return go(f'/draft/{draft_id}', f'Edit failed: {exc}'[:180])
    after['_findings'] = before.get('_findings', {})
    after['_date'] = before.get('_date', '')
    store.record_edit(draft_id, instruction.strip(), before, after)
    store.update_draft(draft_id, story_json=json.dumps(after),
                       title=after.get('title', d['title']))
    store.log('draft.revise', f'{draft_id}: {instruction[:120]}')
    return go(f'/draft/{draft_id}', 'Applied: ' + '; '.join(changes)[:150])


@app.post(PREFIX + '/draft/{draft_id}/reject')
def reject(request: Request, draft_id: int):
    if not authed(request):
        return login_redirect()
    store.update_draft(draft_id, status='rejected')
    store.log('draft.reject', str(draft_id))
    return go('/queue', 'Rejected. It stays in the database if you want it back.')


@app.post(PREFIX + '/draft/{draft_id}/approve')
def approve(request: Request, draft_id: int):
    if not authed(request):
        return login_redirect()
    d = store.get_draft(draft_id)
    if not d:
        return go('/queue', 'No such draft.')
    s = json.loads(d['story_json'])
    story, paper = publish.expand(s)
    publish.write_story(story, paper)
    ok, log = publish.commit_and_push(f'Publish: {story["title"]}')
    store.update_draft(draft_id, status='published' if ok else 'approved')
    store.log('draft.approve', f'{draft_id} {story["slug"]} ok={ok}')
    return page('Publish', f'<pre>{e(log)}</pre>'
                f'<p><a class="btn" href="{PREFIX}/queue">Back to the queue</a></p>',
                '/queue',
                'Published.' if ok else 'Written and committed, but not pushed — see the log.')


@app.get(PREFIX + '/health')
def health():
    return JSONResponse({'ok': True, 'stories': len(_site_stories())})
