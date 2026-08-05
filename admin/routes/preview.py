# -*- coding: utf-8 -*-
"""Serving a draft as the page it will become.

The preview is rendered by build.py — the same function that writes
site/stories/*.html — so these routes exist only to feed it the assets and links
it expects. See drafts.pages() for why it is the real renderer and not a mock-up.
"""
import os

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, Response

from .. import drafts
from ..config import PREFIX, ROOT
from ..session import authed, login_redirect

router = APIRouter()

ASSETS = os.path.join(ROOT, 'assets')


@router.get(PREFIX + '/preview/assets/style.css')
def preview_css():
    return Response(drafts.preview_css(), media_type='text/css')


@router.get(PREFIX + '/preview/assets/{name:path}')
def preview_asset(name: str):
    # Resolve first, then check the result is still inside assets/ — a path like
    # `../../admin/.env` normalises out of the directory, and this is the check
    # that stops it.
    path = os.path.normpath(os.path.join(ASSETS, name))
    if not path.startswith(ASSETS) or not os.path.isfile(path):
        return Response('not found', status_code=404)
    kind = ('text/javascript' if name.endswith('.js') else
            'font/woff2' if name.endswith('.woff2') else
            'application/octet-stream')
    with open(path, 'rb') as fh:
        return Response(fh.read(), media_type=kind)


@router.get(PREFIX + '/preview/papers/{draft_id}.html')
def preview_paper(request: Request, draft_id: int):
    if not authed(request):
        return login_redirect()
    _, paper_html = drafts.pages(draft_id)
    return HTMLResponse(paper_html or 'No such draft.')


@router.get(PREFIX + '/preview/{draft_id}/story.html')
def preview_story(request: Request, draft_id: int):
    if not authed(request):
        return login_redirect()
    story_html, _ = drafts.pages(draft_id)
    if not story_html:
        return HTMLResponse('No such draft.')
    # The page is written for a directory two deep in site/, so '../assets/' and
    # '../papers/' are rewritten to land on the routes above. Doing it here keeps
    # build.py free of any knowledge that a backoffice exists.
    return HTMLResponse(story_html.replace(
        '../papers/', f'{PREFIX}/preview/papers/').replace(
        '../assets/', f'{PREFIX}/preview/assets/').replace(
        '../stories.html', f'{PREFIX}/queue').replace(
        '../index.html', f'{PREFIX}/'))
