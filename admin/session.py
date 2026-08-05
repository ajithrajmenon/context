# -*- coding: utf-8 -*-
"""Who is allowed in, and where to send them.

One password guards everything, so the cookie policy is written once, here,
rather than in whichever route happened to need it. Every router imports these
four functions and none of them knows how a session is stored.

    authed()          is this request signed in?
    sign_in()         a redirect carrying a fresh session
    sign_out()        a redirect that drops it
    login_redirect()  send an unauthenticated request to the form
    go()              redirect after a POST, with a message
"""
import hashlib
import hmac
import time

from fastapi.responses import RedirectResponse

from . import store
from .config import COOKIE, PASSWORD, PREFIX, SECURE_COOKIE


def authed(request):
    return store.session_ok(request.cookies.get(COOKIE))


def password_ok(candidate):
    """Constant-time compare: a timing side channel on the one secret guarding
    everything is not a theoretical concern. Hashing both sides first keeps the
    comparison a fixed length whatever was typed."""
    if not PASSWORD:
        return False
    return hmac.compare_digest(
        hashlib.sha256((candidate or '').encode()).digest(),
        hashlib.sha256(PASSWORD.encode()).digest())


def login_redirect(bad=False):
    return RedirectResponse(PREFIX + '/login' + ('?bad=1' if bad else ''),
                            status_code=303)


def sign_in():
    """A redirect to the dashboard carrying a fresh session.

    httponly so script cannot read it, samesite=lax so another site cannot
    drive it, and path-scoped to the prefix so the cookie is not sent anywhere
    else. `secure` is on unless explicitly relaxed for local http testing.
    """
    token = store.new_session()
    store.log('login.ok')
    resp = RedirectResponse(PREFIX + '/', status_code=303)
    resp.set_cookie(COOKIE, token, httponly=True, samesite='lax',
                    secure=SECURE_COOKIE, max_age=store.SESSION_TTL, path=PREFIX)
    return resp


def refuse():
    """A failed sign-in. The delay is a brake on guessing, not a defence."""
    store.log('login.failed')
    time.sleep(1.0)
    return login_redirect(bad=True)


def sign_out(request):
    store.drop_session(request.cookies.get(COOKIE))
    resp = login_redirect()
    resp.delete_cookie(COOKIE, path=PREFIX)
    return resp


def go(path, msg=''):
    """Redirect after a POST, so a reload does not repeat the action."""
    sep = '&' if '?' in path else '?'
    return RedirectResponse(PREFIX + path + (f'{sep}m={msg}' if msg else ''),
                            status_code=303)
