# Context

A storytelling team. We take the things that are too large, too old or too strange to
picture, put them next to something you already know, and then hand you the controls.

## What this is

Not an encyclopedia and not a course. Every piece is built as a story — a hook, a build,
a turn, and a landing — because people remember what happened to somebody, in what order,
and why it mattered. The mechanism goes in only once you care about the answer.

The library grows. Subjects are not fixed: space, bodies, time, Earth, the numbers that
break intuition, and whatever else turns out to be worth being curious about. New
categories cost nothing — the nav and the filters build themselves from the stories.

## Structure

```
build.py          generates the site
stories_data.py   every story — one dict each
assets/style.css  the design system
assets/motion.js  reveals and the canvas scenes
assets/fonts/     self-hosted woff2
site/             build output, deploy this
```

Three kinds of page: a homepage, a `stories` index that filters in place, and one page per
story. Adding a story means appending one dict to `STORIES` and re-running `build.py`.
Set `featured: True` to surface it on the homepage.

## The identity

The idea the whole thing hangs on: **context is what you get when you zoom out**. Every
story takes one thing and puts something bigger beside it, so the recurring motif is a
small bright point inside a large field — which is also the wordmark, and also the `orbit`
scene.

On the influences: the obvious reference for this kind of work lives in the dark, in deep
space, with everything glowing against black. Going there would have produced a copy with
a different logo. So the split is deliberate — **we live in daylight and the dark is where
the scenes happen.** White page, vivid glowing panel, a hard cut between the two. Same
appetite for scale and wonder, different room.

What carries over: saturated multi-hue colour, rounded geometry, ambient motion, and the
zoom-out that reframes the subject. What does not: dark chrome, mascots, and the void as a
default background.

### Tokens

Six tones. Each sets a three-stop gradient for its scenes and an accent used for text and
links on white, which is the one that has to clear 4.5:1 — all six do.

| tone | gradient | accent |
|------|----------|--------|
| nebula | violet → magenta | `#6D28D9` |
| deepsea | navy → cyan | `#0E7490` |
| ember | wine → orange | `#BE123C` |
| forest | pine → emerald | `#047857` |
| dusk | indigo → violet | `#1D4ED8` |
| solar | brown → amber | `#B45309` |

- Page `#FFFFFF` · surface `#F7F9FC` · ink `#101828` · muted `#5A6875`
- Gabarito (display) · Source Sans 3 (body), both self-hosted — no font CDN
- Text over a scene sits on a gradient scrim, so contrast never depends on where a
  particle happens to drift

### Motion

`assets/motion.js` handles scroll reveals and five canvas scenes — `stars`, `orbit`,
`swarm`, `waves`, `bloom`. A story picks one with `scene`.

Rules the file keeps:

- nothing animates off-screen; an `IntersectionObserver` parks each scene
- `prefers-reduced-motion` gets one static frame, never a frozen blank panel
- scenes are seeded from the slug, so a card looks identical on every load
- anything scrolled past without intersecting still reveals — a jumped-over element must
  never stay invisible

## Running locally

```bash
python3 build.py
python3 -m http.server 8000 --directory site
```

## Deploying

No build tooling, no dependencies, no framework. Any static host works.

**GitHub Pages** — already wired up. `.github/workflows/deploy.yml` runs `build.py` and
publishes `site/` on every push. Set Settings → Pages → Source to **GitHub Actions** once,
and the site goes live at https://ajithrajmenon.github.io/context/.

**Cloudflare Pages / Netlify / Vercel** — publish directory `site`, build command
`python3 build.py`. Or drag `site/` onto Netlify Drop for an instant URL.

## Wiring it to Claude later

The generator is deliberately data-driven so an MCP server has an obvious surface. Four
tools, writing to `stories_data.py` via the GitHub API:

- `create_draft` — append a story dict with `status: draft`
- `list_drafts`
- `update_draft`
- `publish` — flip status, commit, let the host rebuild

Keep `publish` as a separate human-triggered call. Accuracy is the product here, and a
wrong explanation costs more trust than a right one earns.
