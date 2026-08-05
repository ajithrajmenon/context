# -*- coding: utf-8 -*-
"""The approval queue: read a draft, edit it by prompt, publish it or reject it.

Nothing reaches the site without passing through here.
"""
import json
import time

from fastapi import APIRouter, Form, Request

from .. import drafts, store
from ..config import PREFIX
from ..session import authed, go, login_redirect
from ..ui import e, page, preview_panel

router = APIRouter()


@router.get(PREFIX + '/queue')
def queue(request: Request, m: str = ''):
    if not authed(request):
        return login_redirect()
    rows = ''.join(
        f'<tr><td><a href="{PREFIX}/draft/{d["id"]}">'
        f'{e(d["title"] or d["slug"])}</a><br>'
        f'<span class="muted">{e(d["slug"])}</span></td>'
        f'<td><span class="pill go">{e(d["lens"])}</span></td>'
        f'<td class="muted">{e(d["domain"])}</td>'
        f'<td><span class="pill warn">{e(d["status"])}</span></td></tr>'
        for d in drafts.pending())
    return page('Approval queue', f"""
<p class="sub">Drafts the research team has finished. Read, edit by prompt if
something is off, then approve — approving publishes and pushes.</p>
<table><tr><th>Story</th><th>Lens</th><th>Domain</th><th>Status</th></tr>
{rows or '<tr><td colspan="4" class="muted">Empty.</td></tr>'}</table>""", '/queue', m)


@router.get(PREFIX + '/draft/{draft_id}')
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
{preview_panel(s.get('lens'), s.get('domain'), draft_id)}
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


@router.post(PREFIX + '/draft/{draft_id}/revise')
def revise(request: Request, draft_id: int, instruction: str = Form(...)):
    if not authed(request):
        return login_redirect()
    try:
        changes = drafts.revise(draft_id, instruction.strip())
    except Exception as exc:                      # noqa: BLE001 - shown to a human
        return go(f'/draft/{draft_id}', f'Edit failed: {exc}'[:180])
    if changes is None:
        return go('/queue', 'No such draft.')
    return go(f'/draft/{draft_id}', 'Applied: ' + '; '.join(changes)[:150])


@router.post(PREFIX + '/draft/{draft_id}/reject')
def reject(request: Request, draft_id: int):
    if not authed(request):
        return login_redirect()
    drafts.reject(draft_id)
    return go('/queue', 'Rejected. It stays in the database if you want it back.')


@router.post(PREFIX + '/draft/{draft_id}/approve')
def approve(request: Request, draft_id: int):
    if not authed(request):
        return login_redirect()
    ok, log, story = drafts.approve(draft_id)
    if story is None:
        return go('/queue', log)
    return page('Publish', f'<pre>{e(log)}</pre>'
                f'<p><a class="btn" href="{PREFIX}/queue">Back to the queue</a></p>',
                '/queue',
                'Published.' if ok else 'Written and committed, but not pushed — see the log.')
