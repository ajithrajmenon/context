# [Context]

A storytelling team. We take something large and put it next to something you already
know, then publish the research behind it so you can check us.

Fifty stories. No dependencies, no framework, no build tooling beyond Python 3.

## The framework

**Every story asks exactly one of four questions.** The lens is decided before the title
is written, and the title obeys it.

| Lens | The question | Stories |
|---|---|---|
| **What** | What is this, actually? | 10 |
| **Why** | Why does it happen at all? | 23 |
| **How** | How does it work? | 11 |
| **What if** | What would happen? | 6 |

The **domain** — body, mind, kitchen, money, physics — is a separate label. What a story
is *about* and what it *asks* are two different things, and a reader looking for one is
not looking for the other.

**Scope is this planet.** Nothing beyond Earth. A story about a black hole ends in awe; a
story about antibiotic resistance ends in a decision, and we are in the second business.

Both rules, and the reasoning, live in `STYLE.md`. The full catalogue is `PIPELINE.md`.

## Two layers

Every story links to a paper. The **story** is short, illustrated and designed to be
finished. The **paper** is long, sourced, and honest about what is not known — findings
graded `established` / `best current explanation` / `contested`, the live disputes stated
as disputes, and a section for what we could not establish.

Nobody has to read the paper. Everybody has to be able to.

## Structure

```
build.py           takes a corpus, writes site/ — the only thing you run
corpus.py          assembles what is published, from the four sources below
beats.py           the six-beat grammar, shared by the library and the writer
stories_data.py    the four flagship stories, hand-built. Data only
papers_data.py     the four flagship papers. Data only
library.py         stories 5-50 as briefs, the expander, and the lens map
content/           stories written by the research team, plus visibility.json
diagram.py         labelled diagrams: 12 hand-composed, plus a 7-type grammar
illustrate.py      generated SVG scenes — the banners
preview.py         build and serve the site locally
bundle.py          folds site/ into one self-contained HTML file
assets/style.css   the design system
assets/motion.js   scroll reveals, parallax, the progress rail
assets/fonts/      self-hosted woff2 — no font CDN
site/              build output. Deploy this
```

`build.py` renders whatever corpus it is handed, and never reads content itself.
That is what lets the backoffice preview an unpublished draft through this exact
code rather than a second renderer that would drift away from it.

Four kinds of page: a homepage, a `stories` index that filters in place, one page per
story, and one per paper. Set `featured: True` to surface a story on the homepage.

### A story is a stack of cards

Every story is a list of blocks, rendered in order:

| block | what it is |
|-------|-----------|
| `text` | white card, a heading and a couple of short paragraphs |
| `diagram` | a labelled explanatory picture. Static — you are reading it |
| `scene` | full-bleed illustrated panel, one line over it |
| `turn` | the pivot, one line, big type on full colour |
| `steps` | a numbered checklist |
| `figure` | the one thing per story you operate yourself |

Because a story is a list, it is also a shot list: each block is roughly a beat of script
plus the picture that goes with it. These are meant to become videos.

### Six beats, in this order

Wrong Picture → Crack → Turn → Machinery → Cost → Long View. When a piece feels wrong it
is almost always because one of these is missing. `STYLE.md` section 3 has each of them.

### Flagship and library

Four stories are flagship builds: diagrams composed by hand for that story alone, plus an
interactive figure. The other 46 are library builds — same beats, same research standard,
same one-sentence Turn, at about a third the length, with diagrams built from a
parameterised grammar fed different data by every story.

What never varies: every story has its own banner, its own diagram data, its own numbers
and its own paper. Recycling artwork across stories is the failure this project corrected
twice; `illustrate.render()` takes a variant that reframes the composition — mirror, tilt,
zoom, offset — and every story is assigned its own variant within its scene, so no two
banners on the site are the same picture.

## The identity

**Context is what you get when you zoom out.** Every story takes one thing and puts
something bigger beside it, so the recurring motif is a small bright point in a large
field.

The name is written **[Context]**, brackets included, everywhere. Brackets are what an
editor puts around the thing they had to add so a quotation makes sense on its own. That
is the job. The wordmark animates the two brackets and nothing else.

On the influences: the obvious reference for this kind of work lives in the dark, in deep
space, everything glowing against black. Going there would have produced a copy with a
different logo. So the split is deliberate — **we live in daylight and the dark is where
the scenes happen.** White page, vivid glowing panel, a hard cut between the two.

### Three surfaces

| surface | job |
|---|---|
| white page | where you read |
| dark panel | atmosphere, and the only place anything moves |
| light card | where things are explained. Holds perfectly still |

Eight tones set a three-stop gradient for scenes and an accent for text on white — all
clear 4.5:1. Colour belongs to the card, not the story: a piece walks through several
tones as it goes, the way a film relights between acts.

Four lens colours sit on top of that, one per question, used on the chip, the card eyebrow
and the home grid so the same question always looks the same.

### Motion

Only the hero panel moves. Everything that explains something holds still — you cannot
read a diagram that is drifting.

- reveals use an `IntersectionObserver`; anything scrolled past without intersecting still
  reveals, or a jumped-over element stays invisible for good
- `prefers-reduced-motion` is honoured throughout
- scenes are seeded from the slug, so a page looks identical on every load
- animation timings are classes, not inline styles — a nonce-based `style-src` blocks
  inline style attributes, and the site must survive being embedded somewhere strict

## Running locally

To see the site — just the site, no login and no backoffice:

```
python preview.py
```

That builds `site/` and serves it at <http://127.0.0.1:8000/>, opening your
browser. Change a story, run it again, reload. `--port 9000` moves it;
`--no-build` serves what is already there.

Do not open `site/index.html` from the file manager. Pages link to each other
with paths like `../assets/style.css`, and a `file://` page is its own origin —
some of it works, some of it quietly does not. A local HTTP server behaves the
way GitHub Pages will, which is the only reason to look in the first place.

The long way is the same two steps:

```
python build.py
python -m http.server 8000 --directory site
```

## One file, no server

```bash
python3 bundle.py
```

Writes `context-site.html` — every page, fonts and all, in a single file you can open by
double-clicking or send to someone. It also writes `context-artifact.html`, the same
payload without the outer document, for hosts that supply their own `<head>`.

## Deploying

Any static host works.

**GitHub Pages** — `.github/workflows/deploy.yml` runs `build.py` and publishes `site/` on
every push. Set Settings → Pages → Source to **GitHub Actions** once, and the site is live
at https://ajithrajmenon.github.io/context/.

**Cloudflare Pages / Netlify / Vercel** — publish directory `site`, build command
`python3 build.py`.

## The backoffice

`admin/` is a separate private app — story CRUD, visibility control, and a
six-agent research team that drafts new stories for a human to approve. It is
**not** part of the static site and cannot be: GitHub Pages serves files, not
logins, databases or API keys. The backoffice runs elsewhere, edits this
repository, and pushes; Pages redeploys itself.

```
backoffice ──▶ content/*.json ──▶ git push ──▶ Actions ──▶ Pages
                                                  │
                                            build.py reads content/
```

The site stays dependency-free. Switch the backoffice off and nothing here
changes.

Start it from a terminal — the same command on Windows, macOS and Linux:

```
python admin/serve.py
```

It sets itself up on the first run and prints your login link. The research
team uses the Claude Code subscription you are already signed into, so there is
no API key to buy. See `admin/README.md`.

## Adding a story

1. Pick the lens first. If you cannot say which of the four it is, it is not ready.
2. Write the paper. The story is what survives the research, not the other way round.
3. Add a brief to `library.py` — `q(...)` for the compact form — and its slug to `LENS`.
4. `python3 build.py`.

Then run the checklist at the end of `STYLE.md`. Every number in a story has to be
traceable to the paper, with its error bar.
