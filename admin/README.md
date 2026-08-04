# The [Context] backoffice

A private admin app: story CRUD, visibility control, and a six-agent research
team that drafts new stories for a human to approve.

## The constraint that shapes all of this

**GitHub Pages serves static files. It cannot host a login, a database, or an
API key.** So the backoffice is a *separate* application that you run somewhere
else. It edits the repository and pushes; Pages redeploys itself.

```
   you ──▶ backoffice (FastAPI, private)
              │  research team (Claude, server-side key)
              │  SQLite: drafts, queue, run logs
              ▼
           content/*.json  ──▶ git push ──▶ Actions ──▶ Pages
                                              │
                                        build.py reads content/
```

The site stays a zero-dependency static build. Nothing here changes that: if
the backoffice is switched off, the site is unaffected.

## Running it

```bash
pip install -r admin/requirements.txt

export CONTEXT_ADMIN_PASSWORD='a long random passphrase'   # required
export CONTEXT_ADMIN_PREFIX='/b-9f3a71c2e0'                # required, unguessable
export ANTHROPIC_API_KEY='sk-ant-...'                      # required to generate

uvicorn admin.app:app --host 127.0.0.1 --port 8800
```

Then open `http://127.0.0.1:8800/b-9f3a71c2e0/`.

The app refuses to serve anything without `CONTEXT_ADMIN_PASSWORD`. It will not
run open, even locally.

| Variable | Purpose |
|---|---|
| `CONTEXT_ADMIN_PASSWORD` | The password. Required. |
| `CONTEXT_ADMIN_PREFIX` | Secret URL prefix. Every route lives under it. |
| `ANTHROPIC_API_KEY` | Server-side only. Never sent to a browser. |
| `CONTEXT_DB` | SQLite path. Defaults to `admin/context.db`. |
| `CONTEXT_ADMIN_INSECURE_COOKIE` | Set to `1` **only** for local HTTP testing. |

### On the secret URL

The prefix keeps the door out of crawlers, referrer headers and access logs.
**It is not access control.** A URL leaks the moment it is pasted anywhere. The
password is what actually protects this, which is why both are mandatory and
why sessions expire after twelve hours.

If you expose this beyond localhost, put it behind HTTPS. A password over plain
HTTP is a password in the clear.

## The research team

Six agents, in order, each a separate Claude call with its own system prompt:

| Agent | Job | Tools |
|---|---|---|
| **Planner** | Decides the lens, title, candidate Turn, and the research questions. Can reject a goal here. | — |
| **Search** | Runs web search against those questions; reports sources and numbers. | `web_search` |
| **Reader** | Fetches the best sources in full; pulls exact figures and stated limitations. | `web_fetch` |
| **Fact checker** | Grades every claim `established` / `best current explanation` / `contested`. Discards what it cannot trace. Can drop the story. | — |
| **Writer** | Turns surviving findings into the six beats plus the paper. | — |
| **Editor** | Runs the `STYLE.md` checklist and fixes what fails. | — |

Six calls rather than one because each stage gets a clean context, and because
**every stage's full output is stored**. The approval screen shows you the
graded findings and — the useful part — what the fact checker threw away. You
are auditing a chain, not trusting a finished draft.

Two agents can stop the run: the Planner if the goal cannot carry a Turn, the
Fact checker if the premise did not survive the evidence. A dropped story is a
success.

**The pipeline never publishes.** It produces a queue entry. A person approves.

### Prompt-based editing

On the approval screen, say what to change in plain English. The Editor applies
it and returns the whole draft; every edit is stored with its before and after,
so you can see what a given instruction actually did.

## Visibility

`content/visibility.json` maps slug → false to take *any* story off the site —
generated or hand-written — without deleting it. Absent means visible. Hiding a
story hides its paper too, so no live paper links to a 404.

This is deliberately separate from publication. Un-publishing by deleting loses
the work; hiding keeps the file and its history.

## What is tested, and what is not

`python3 -m admin.test_pipeline` runs the whole orchestration against a stub
client: stage order, token accounting, `pause_turn` resumption, refusal
handling, draft expansion, and that both generated diagrams actually render. No
API key needed, nothing spent.

It does **not** test the quality of what the real agents write. That needs a key
and a live run — do that before trusting the first draft.

## Deploying

Anywhere that runs Python and holds a git checkout with push rights: a small VM,
Fly.io, Railway, Render. The app shells out to `git` in the repository root, so
the checkout must be writable and its credentials must work non-interactively.

Do not put it on GitHub Pages. It cannot go there — that is the whole point of
the first section.

## Files

```
admin/app.py             FastAPI: auth, CRUD, generation, queue, publish
admin/research.py        the six agents, their prompts and schemas
admin/publish.py         draft -> content/*.json -> build -> commit -> push
admin/store.py           SQLite: drafts, runs, stages, edits, audit, sessions
admin/test_pipeline.py   offline orchestration test
content/stories/*.json   published generated stories, read by build.py
content/visibility.json  slug -> false hides a story
```
