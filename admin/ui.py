# -*- coding: utf-8 -*-
"""How the backoffice looks. No routes, no database, no business logic.

This is the private tool, not the published site — the site's design system is
assets/style.css and has nothing to do with this file. What the two share is the
principle: hold still, say one thing per card, and never make a reader guess
whether something worked.

Split out of app.py because a routing module that also carries seventy lines of
CSS is doing two jobs, and the CSS was the part nobody could find. Everything
here is a pure function of its arguments, so it can be rendered and eyeballed
without a server, a session or a run.

    e()      escape a value for HTML
    page()   the full document: bar, heading, body
    rail()   the six-agent progress rail
"""
import html

from fastapi.responses import HTMLResponse

from .config import PREFIX

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

/* The run rail. Six agents hand work to each other in one direction, so the
   progress reads left to right along a single line — the connector between
   two steps is the handover, and it fills in only once the earlier agent has
   actually delivered. A vertical list of dots showed the same facts and none
   of the movement. */
.rail{display:flex;align-items:flex-start;overflow-x:auto;padding:.4rem 0 .2rem}
.step{flex:1 1 0;min-width:5.6rem;text-align:center;position:relative}
.step .mark{width:1.6rem;height:1.6rem;border-radius:50%;margin:0 auto .45rem;
border:2px solid var(--border);background:var(--page);color:var(--muted);
font-size:.72rem;font-weight:700;line-height:1.35rem;position:relative;z-index:1}
.step .name{font-size:.78rem;font-weight:600;letter-spacing:.02em}
.step .t{font-size:.7rem;color:var(--muted);display:block;min-height:1em}
/* The connector is drawn from each step back to the one before it, so the
   first step has nothing to its left and the line never overhangs the rail. */
.step+.step:before{content:"";position:absolute;top:.8rem;right:50%;left:-50%;
height:2px;background:var(--border)}
.step.done+.step:before,.step.done+.step.live:before{background:#16A34A}
.step.done .mark{border-color:#16A34A;background:#16A34A;color:#fff}
.step.live .mark{border-color:var(--accent);color:var(--accent);
animation:p 1.1s ease-in-out infinite}
.step.live .name{color:var(--accent)}
.step.todo .name{color:var(--muted)}
.step.fail .mark{border-color:#B91C1C;background:#B91C1C;color:#fff}

/* The live tail of what the current agent is doing. A run can sit on one
   stage for several minutes with nothing else on the page to look at, so this
   is deliberately terminal-shaped and auto-scrolled: it is the one place on
   the run page that is supposed to look like something is happening. */
.live-log{font:.84rem/1.6 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
max-height:14rem;overflow-y:auto;display:flex;flex-direction:column-reverse}
.live-log .pline{padding:.1rem 0;color:var(--muted)}
.live-log .pline:last-child{color:var(--ink);font-weight:600}

/* The draft preview is the live page in a frame, so give it room and a phone
   width to switch to — most readers will arrive on one. */
.frame{border:1px solid var(--border);border-radius:var(--r);overflow:hidden;
background:var(--surface);margin-bottom:.6rem}
.frame iframe{display:block;width:100%;height:min(78vh,54rem);border:0;
background:var(--page)}
.frame.phone{max-width:26rem;margin-inline:auto}
"""

TABS = [('', 'Dashboard'), ('/stories', 'Stories'), ('/generate', 'Generate'),
        ('/queue', 'Queue'), ('/runs', 'Runs')]

# The six agents pass work along in one direction, so the run reads as one
# line left to right rather than a column of dots. Each step carries the name
# of the agent doing the work and, once it has delivered, how long it took —
# the two things you want while waiting.
RAIL = {'plan': 'Planner', 'search': 'Search', 'read': 'Reader',
        'check': 'Fact check', 'write': 'Writer', 'edit': 'Editor'}


def e(x):
    return html.escape(str(x if x is not None else ''))


def page(title, body, nav='', message=''):
    links = ''.join(
        f'<a class="{"on" if nav == p else ""}" href="{PREFIX}{p or "/"}">{n}</a>'
        for p, n in TABS)
    msg = f'<div class="card"><b>{e(message)}</b></div>' if message else ''
    return HTMLResponse(f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>{e(title)} — [Context]</title>
<style>{CSS}</style></head><body>
<div class="bar"><b>[Context]</b>{links}
<span class="sp"></span>
<a href="{PREFIX}/logout">Sign out</a></div>
<div class="wrap"><h1>{e(title)}</h1>{msg}{body}</div></body></html>""")


def state_pill(state):
    """Run state as a coloured pill. One mapping, so the dashboard and the runs
    list cannot disagree about what green means."""
    cls = 'ok' if state == 'done' else 'bad' if state == 'failed' else 'warn'
    return f'<span class="pill {cls}">{e(state)}</span>'


def preview_panel(lens, domain, draft_id):
    """The draft's own page, framed. Not a summary of it — the thing itself."""
    return f"""
<div class="row" style="margin-bottom:.6rem">
<span class="pill go">{e(lens)}</span>
<span class="pill">{e(domain)}</span>
<span class="sp" style="margin-left:auto"></span>
<a class="btn ghost" target="_blank"
   href="{PREFIX}/preview/{draft_id}/story.html">Open full size &#8599;</a></div>
<div class="frame"><iframe src="{PREFIX}/preview/{draft_id}/story.html"
  title="The page as it will be published"></iframe></div>
<p class="muted">This is the page itself, rendered by <code>build.py</code> —
the same code that writes the live site. What you see here is what publishes.</p>"""


def progress_log(rows):
    """The live tail of what the current agent is doing.

    Rendered only while a run is in flight — once a stage is done, run_stage
    already holds its real, complete output, and this rolling window has
    nothing left to add. `column-reverse` in the CSS keeps the newest line at
    the top of the box without any script: the DOM order is oldest-first, the
    layout direction is reversed, and a box scrolled to its default position
    shows what just happened rather than what happened first.
    """
    if not rows:
        return ''
    lines = ''.join(f'<div class="pline">{e(r["text"])}</div>' for r in rows[-24:])
    return f'<div class="card"><div class="live-log">{lines}</div></div>'


def rail(stages, seconds, current, state):
    """The run's progress, as one left-to-right line of handovers."""
    steps = ''
    for i, name in enumerate(stages):
        if name in seconds:
            cls, mark = 'done', '&#10003;'
        elif name == current and state == 'running':
            cls, mark = 'live', str(i + 1)
        elif name == current and state == 'failed':
            cls, mark = 'fail', '!'
        else:
            cls, mark = 'todo', str(i + 1)
        took = f'{seconds[name]:.0f}s' if name in seconds else (
            'working' if cls == 'live' else '')
        steps += (f'<div class="step {cls}"><div class="mark">{mark}</div>'
                  f'<div class="name">{RAIL.get(name, name.title())}</div>'
                  f'<span class="t">{took}</span></div>')
    return f'<div class="card"><div class="rail">{steps}</div></div>'
