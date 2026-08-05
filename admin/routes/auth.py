# -*- coding: utf-8 -*-
"""Signing in and out. The only pages that do not require a session."""
from fastapi import APIRouter, Form, Request

from .. import session
from ..config import PASSWORD, PREFIX
from ..ui import page

router = APIRouter()


@router.get(PREFIX + '/login')
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


@router.post(PREFIX + '/login')
def login(response_password: str = Form('', alias='password')):
    if not session.password_ok(response_password):
        return session.refuse()
    return session.sign_in()


@router.get(PREFIX + '/logout')
def logout(request: Request):
    return session.sign_out(request)
