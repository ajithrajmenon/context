# -*- coding: utf-8 -*-
"""Where the backoffice reads its settings.

Split out of app.py because three modules need the URL prefix and none of them
should have to import the web application to get it — importing app.py has the
side effect of registering every route, which is not something a helper should
cause.

Everything behind one unguessable path prefix *and* a password. The prefix keeps
the door out of logs and crawlers; the password is what actually stops anyone.
Obscurity is not access control, so both are required and neither is optional.

    CONTEXT_ADMIN_PREFIX            required, unguessable
    CONTEXT_ADMIN_PASSWORD          required
    CONTEXT_ADMIN_INSECURE_COOKIE   1 only for local http:// testing
    ANTHROPIC_API_KEY               only for the API backend

The API key lives here, server-side, and never reaches a browser.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(ROOT, 'admin', '.env')


def load_env(path=ENV_FILE):
    """Read admin/.env if it exists, so settings survive closing the terminal.

    Real environment variables always win — a value already exported is a
    deliberate act and should not be silently overridden by a checked-in file.
    """
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


load_env()

PREFIX = os.environ.get('CONTEXT_ADMIN_PREFIX', '/backoffice').rstrip('/')
PASSWORD = os.environ.get('CONTEXT_ADMIN_PASSWORD', '')
SECURE_COOKIE = os.environ.get('CONTEXT_ADMIN_INSECURE_COOKIE', '') != '1'
COOKIE = 'ctx_admin'
