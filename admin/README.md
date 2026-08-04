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

On your own machine, in a clone of this repository. **From a terminal** —
PowerShell on Windows, Terminal on macOS, a shell on Linux:

```
python admin/serve.py
```

That is the whole command, and it is the same on all three. Use `python3` if
`python` is not on your PATH.

`admin/serve.sh` does the same thing and is there for Unix habit — but it is a
bash script, so it only runs from a shell, and on Windows there is no bash to
run it at all. Double-clicking a `.sh` file gets you Explorer asking which
application to open it with. `serve.py` exists so there is one answer.

First run: it generates a secret URL prefix, asks for an admin password, finds
Claude Code or takes an API key, writes `admin/.env` (mode 600, gitignored),
installs dependencies, and prints your login link. Every run after that just
starts and prints the link.

The long way, if you would rather set it up by hand:

```
pip install -r admin/requirements.txt
cp admin/.env.example admin/.env      # then fill it in
python -m uvicorn admin.app:app --host 127.0.0.1 --port 8800
```

**Where is the login link?** There is no fixed one — it is
`http://127.0.0.1:8800` plus whatever `CONTEXT_ADMIN_PREFIX` you chose.
`serve.py` prints it. If you lose it, it is the `CONTEXT_ADMIN_PREFIX` line in
`admin/.env`.

The app refuses to serve anything without `CONTEXT_ADMIN_PASSWORD`. It will not
run open, even locally.

### Reaching Claude: two backends

The research team can run either way, and the six agents cannot tell the
difference.

| Backend | Auth | Cost |
|---|---|---|
| **`cli`** (default) | The Claude Code login you already have | Draws on your subscription's usage allowance |
| **`api`** | `ANTHROPIC_API_KEY` | Billed per token |

**Use the CLI if you have a Claude subscription.** Install Claude Code, run
`claude` once and sign in, and that is the whole setup — no key, no separate
credit to buy:

```bash
npm install -g @anthropic-ai/claude-code
claude          # sign in, then quit with /exit
```

`serve.py` detects it and checks the login before starting, so a missing sign-in
shows up immediately rather than four minutes into a research run.

Set `CONTEXT_LLM_BACKEND` to `cli` or `api` to force one. Left blank it prefers
the CLI, because the CLI costs nothing extra.

**Keep Claude Code current** — `claude update`. Two things the backoffice needs
arrived in recent versions: `--append-system-prompt-file`, and `--json-schema`.
Without the first, a 14 KB system prompt has to travel on the command line,
which Windows will not accept; the backoffice falls back to folding it into the
message, but that is a worse prompt. Without the second, structured stages
degrade to scraping JSON out of prose.

**Two honest caveats about the CLI backend.** A six-agent run with web search is
heavy, so on a Pro plan a couple of runs in an afternoon may hit your usage
window — the backoffice reports that as a usage-limit error rather than failing
oddly. And this is your own subscription driving your own tool with a human
approving every output; if this ever became an always-on service generating for
other people, the API is the right home for it.

Everything except **Generate** works with neither backend: story CRUD,
visibility, publishing, and the approval queue.

An API key, if you want one: <https://platform.claude.com/settings/keys>. Note
it is billed separately from a Pro or Max subscription — a subscription does not
include API usage, which is the surprise this whole section exists to avoid.

| Variable | Purpose |
|---|---|
| `CONTEXT_ADMIN_PASSWORD` | The password. Required. |
| `CONTEXT_ADMIN_PREFIX` | Secret URL prefix. Every route lives under it. |
| `CONTEXT_LLM_BACKEND` | `cli`, `api`, or blank to auto-detect (CLI first). |
| `ANTHROPIC_API_KEY` | Only for the `api` backend. Server-side; never sent to a browser. |
| `CONTEXT_CLI_MODEL` | Model for the CLI backend, e.g. `opus`. Blank uses your default. |
| `CONTEXT_CLI_CWD` | Where the CLI runs. Defaults to `~`, away from this repo's CLAUDE.md. |
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
| **Search** | Runs web search against those questions; reports sources and numbers. | web search |
| **Reader** | Fetches the best sources in full; pulls exact figures and stated limitations. | web fetch |
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

`python -m admin.test_pipeline` runs the whole orchestration against a stub
backend: stage order, token accounting, refusal handling, draft expansion, and
that both generated diagrams render. Nothing needed, nothing spent.

It also pins down the CLI backend's command line, where two bugs have already
lived:

- nothing large may reach argv — the prompt goes on stdin and the system prompt
  goes in a file, because npm's `claude` on Windows is a `.cmd` shim and cmd.exe
  stops at 8,191 characters;
- a stage given a JSON schema must be allowed the `StructuredOutput` tool and
  more than one turn, because that tool call *is* how the CLI returns structured
  output. Denying all tools looks like the safe choice and silently guarantees
  failure;
- and `--bare` is never passed, since it bypasses the subscription login and
  demands an API key.

It does **not** test the quality of what the real agents write. That needs a live
run through either backend — do that before trusting the first draft.

## Deploying

**Start on your own laptop.** It already has your GitHub credentials, there is
nothing to provision, and the loop is complete: approve a story here, it pushes,
Actions rebuilds, the public site updates. Only move it to a host when you want
to reach it from a phone or from away from your desk.

When you do, it needs three things a static host cannot give you: a writable git
checkout, non-interactive push credentials (a deploy key), and a persistent disk
for `admin/context.db`. A small VM, Fly.io with a volume, Railway, or Render all
work. Put it behind HTTPS — a password over plain HTTP is a password in the
clear, and that is also when you drop `CONTEXT_ADMIN_INSECURE_COOKIE`.

Do not put it on GitHub Pages. It cannot go there — that is the whole point of
the first section.

## Files

```
admin/app.py             FastAPI: auth, CRUD, generation, queue, publish
admin/backend.py         two ways to reach Claude — CLI or API — one interface
admin/research.py        the six agents, their prompts and schemas
admin/publish.py         draft -> content/*.json -> build -> commit -> push
admin/store.py           SQLite: drafts, runs, stages, edits, audit, sessions
admin/test_pipeline.py   offline orchestration test
admin/serve.py           first-run setup, then starts — Windows, macOS, Linux
admin/serve.sh           the same thing in bash, for Unix habit
admin/.env.example       the settings, documented
content/stories/*.json   published generated stories, read by build.py
content/visibility.json  slug -> false hides a story
```
