# -*- coding: utf-8 -*-
"""[Context] backoffice — the application, assembled.

This file used to be the whole backoffice: routing, authentication, seventy lines
of CSS, HTML templating, thread management and publishing logic in one place. It
is now the assembly point and nothing else, which is the only job it should have
had. Everything lives next door:

    config.py      where the settings come from
    session.py     who is allowed in, and the cookie policy
    ui.py          how it looks — CSS, chrome, the progress rail
    catalogue.py   what is actually on the site
    drafts.py      preview, revise, approve, reject
    runner.py      running the research team in the background
    publish.py     approved draft -> content/ -> git -> Pages
    store.py       the database
    research.py    the six agents
    backend.py     how we reach Claude
    routes/        one router per thing the tool is for

Everything is behind one unguessable path prefix *and* a password. The prefix
keeps the door out of logs and crawlers; the password is what actually stops
anyone. Obscurity is not access control, so both are required and neither is
optional. The API key lives server-side and never reaches a browser.

Run it:

    python admin/serve.py

which writes admin/.env on the first run and prints your login link. The long way
is the same thing:

    export CONTEXT_ADMIN_PASSWORD='...'        # required
    export CONTEXT_ADMIN_PREFIX='/x7fq...'     # required, unguessable
    uvicorn admin.app:app --host 127.0.0.1 --port 8800
"""
from fastapi import FastAPI

from . import store
from .routes import ROUTERS

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# Cheap, idempotent, and it means a fresh clone does not need a setup step.
store.init()

for router in ROUTERS:
    app.include_router(router)
