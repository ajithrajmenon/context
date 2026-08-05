# -*- coding: utf-8 -*-
"""The routers, in the order they are mounted.

One module per thing the backoffice is for. A router reads the request, calls one
function from the service layer, and renders the answer — if a route is doing
more than that, the work belongs next door in drafts.py, catalogue.py, runner.py
or publish.py.

Every path is written out in full, including the secret prefix, so that grepping
for a URL finds the route that serves it.
"""
from . import auth, dashboard, generate, preview, queue, stories

# Mount order does not matter here — no two routers share a path — but reading
# order does, so they are listed the way the interface is used.
ROUTERS = [
    auth.router,
    dashboard.router,
    stories.router,
    generate.router,
    queue.router,
    preview.router,
]
