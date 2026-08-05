# -*- coding: utf-8 -*-
"""Every story on the site, and whether it is showing."""
from fastapi import APIRouter, Form, Request

from .. import catalogue, publish, store
from ..config import PREFIX
from ..session import authed, go, login_redirect
from ..ui import e, page

router = APIRouter()


@router.get(PREFIX + '/stories')
def stories(request: Request, m: str = ''):
    if not authed(request):
        return login_redirect()

    rows = ''
    for s in catalogue.rows():
        shown = s['visible']
        rows += f"""<tr><td><b>{e(s['title'])}</b><br><span class="muted">{e(s['slug'])}</span></td>
<td><span class="pill go">{e(s['lens'])}</span></td>
<td><span class="pill">{s['origin']}</span></td>
<td><span class="pill {'ok' if shown else 'bad'}">{'visible' if shown else 'hidden'}</span></td>
<td class="right"><form method="post" action="{PREFIX}/stories/visibility" class="row">
<input type="hidden" name="slug" value="{e(s['slug'])}">
<input type="hidden" name="visible" value="{'0' if shown else '1'}">
<button class="ghost" type="submit">{'Hide' if shown else 'Show'}</button></form></td></tr>"""

    return page('Stories', f"""
<p class="sub">Every story on the site. Hiding takes one off the site without
deleting it — the file and its history stay. Changes go live on the next publish.</p>
<table><tr><th>Story</th><th>Lens</th><th>Origin</th><th>State</th><th></th></tr>
{rows}</table>
<h2>Push visibility changes</h2>
<form method="post" action="{PREFIX}/publish-site" class="card">
<p class="muted" style="margin-top:0">Rebuilds the site and pushes. Pages redeploys itself.</p>
<button type="submit">Rebuild and push</button></form>""", '/stories', m)


@router.post(PREFIX + '/stories/visibility')
def set_visibility(request: Request, slug: str = Form(...), visible: str = Form('1')):
    if not authed(request):
        return login_redirect()
    publish.set_visible(slug, visible == '1')
    store.log('visibility', f'{slug} -> {"visible" if visible == "1" else "hidden"}')
    return go('/stories', 'Saved. Rebuild and push to make it live.')


@router.post(PREFIX + '/publish-site')
def publish_site(request: Request):
    if not authed(request):
        return login_redirect()
    ok, log = publish.commit_and_push('Update story visibility')
    store.log('publish.site', log[-500:])
    return page('Publish', f'<pre>{e(log)}</pre>'
                f'<p><a class="btn" href="{PREFIX}/stories">Back to stories</a></p>',
                '/stories', 'Published.' if ok else 'Publish failed — see the log.')
