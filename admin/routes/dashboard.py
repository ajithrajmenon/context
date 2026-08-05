# -*- coding: utf-8 -*-
"""The landing page: what is waiting for you, and what the team has been doing."""
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from .. import backend, catalogue, store
from ..config import PREFIX
from ..session import authed, login_redirect
from ..ui import e, page, state_pill

router = APIRouter()


@router.get(PREFIX + '/')
@router.get(PREFIX)
def dashboard(request: Request, m: str = ''):
    if not authed(request):
        return login_redirect()
    queued = store.list_drafts('queued')
    runs = store.list_runs(6)
    n = catalogue.counts(queued=len(queued))

    rows = ''.join(
        f'<tr><td><a href="{PREFIX}/draft/{d["id"]}">{e(d["title"] or d["slug"])}</a></td>'
        f'<td><span class="pill go">{e(d["lens"])}</span></td>'
        f'<td class="muted">{e(d["domain"])}</td></tr>' for d in queued[:8])
    run_rows = ''.join(
        f'<tr><td><a href="{PREFIX}/run/{r["id"]}">{e(r["goal"][:70])}</a></td>'
        f'<td>{state_pill(r["state"])}</td>'
        f'<td class="muted">{e(r["stage"])}</td></tr>'
        for r in runs)

    kind, label = backend.describe()
    badge = (f'<div class="card"><span class="pill {"ok" if kind != "none" else "bad"}">'
             f'{e(kind)}</span> {e(label)}</div>')
    return page('Dashboard', f"""{badge}
<div class="row" style="gap:1rem">
  <div class="card" style="flex:1"><b style="font-size:1.8rem">{n['live']}</b>
    <div class="muted">live on the site</div></div>
  <div class="card" style="flex:1"><b style="font-size:1.8rem">{n['queued']}</b>
    <div class="muted">awaiting approval</div></div>
  <div class="card" style="flex:1"><b style="font-size:1.8rem">{n['generated']}</b>
    <div class="muted">generated &amp; published</div></div>
  <div class="card" style="flex:1"><b style="font-size:1.8rem">{n['hidden']}</b>
    <div class="muted">hidden</div></div>
</div>
<h2>Waiting for you</h2>
<table><tr><th>Story</th><th>Lens</th><th>Domain</th></tr>
{rows or '<tr><td colspan="3" class="muted">Nothing in the queue.</td></tr>'}</table>
<h2>Recent runs</h2>
<table><tr><th>Goal</th><th>State</th><th>Stage</th></tr>
{run_rows or '<tr><td colspan="3" class="muted">No runs yet.</td></tr>'}</table>
<p><a class="btn" href="{PREFIX}/generate">Start a research run</a></p>""", '', m)


@router.get(PREFIX + '/health')
def health():
    return JSONResponse({'ok': True, 'stories': len(catalogue.live())})
