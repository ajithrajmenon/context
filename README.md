# Context

A storytelling team. We take the things that are too large, too old or too strange to
picture, put them next to something you already know, and then hand you the controls.

## What this is

Not an encyclopedia and not a course. Every piece is built as a story — a hook, a build,
a turn, and a landing — because people remember what happened to somebody, in what order,
and why it mattered. The mechanism goes in only once you care about the answer.

The library grows. Subjects are not fixed: space, time, matter, life, minds, bodies,
people, Earth, and whatever else turns out to be worth being curious about. New categories
cost nothing — the nav and the filters build themselves from the stories.

## Structure

```
build.py          generates the site
stories_data.py   every story — one dict each (imports the second shelf)
stories_more.py   stories 11-20, same shape
assets/style.css  the design system
assets/motion.js  reveals and the canvas scenes
assets/fonts/     self-hosted woff2
site/             build output, deploy this
```

Three kinds of page: a homepage, a `stories` index that filters in place, and one page per
story. Adding a story means appending one dict to `STORIES` and re-running `build.py`.
Set `featured: True` to surface it on the homepage.

### A story is a stack of cards

Every story is a list of blocks, rendered in order. Five kinds:

| block | what it is |
|-------|-----------|
| `scene` | full animated panel, one short line of words over it |
| `text` | white card, a heading and a couple of short paragraphs |
| `steps` | a numbered checklist — what a thing needs in order to work |
| `turn` | the pivot, one line, big type on full colour |
| `figure` | the interactive |

The shape follows how the best explainer video essays are built: an opening image you can
see before you understand it, the question asked plainly, named chapters, a checklist where
something has requirements, the blocker, the turn, something you operate yourself, and a
landing that stays humble.

Because a story is a list, it is also a shot list. Each block is roughly a beat of script
plus the picture that goes with it, which is the point — these are meant to become videos.

**Colour belongs to the card, not the story.** Each piece walks through four to six tones
as it goes, the way a film relights between acts. Nothing is one colour all the way down.

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

Eight tones. Each sets a three-stop gradient for its scenes and an accent used for text
and links on white, which is the one that has to clear 4.5:1 — they all do.

| tone | gradient | accent |
|------|----------|--------|
| nebula | violet → magenta | `#6D28D9` |
| deepsea | navy → cyan | `#0E7490` |
| ember | wine → orange | `#BE123C` |
| forest | pine → emerald | `#047857` |
| dusk | indigo → violet | `#1D4ED8` |
| solar | brown → amber | `#B45309` |
| void | near-black → slate | `#334155` |
| rose | plum → coral | `#A21CAF` |

- Page `#FFFFFF` · surface `#F7F9FC` · ink `#101828` · muted `#5A6875`
- Gabarito (display) · Source Sans 3 (body), both self-hosted — no font CDN
- Text over a scene sits on a gradient scrim, so contrast never depends on where a
  particle happens to drift

### Motion

`assets/motion.js` handles scroll reveals and the canvas scenes. Two rules govern all of
them:

**Multicolour.** A scene carries many hues at once, from a shared palette — cyan, lime,
magenta, violet, amber, emerald, coral, sky, orchid, teal. The card's gradient is the
lighting; the scene is the life on top of it. One flat hue per panel reads as decoration,
which is why the tones above stay dark: they exist so the scene's colours can glow.

**Literal.** Every scene draws its own subject. No scene is picked because it looks nice.

| scene | what it draws |
|-------|---------------|
| `stars` | a star field in real stellar colours, blue giants through red dwarfs |
| `orbit` | a star with planets, each its own world |
| `expand` | galaxies drifting apart, with no centre |
| `dying` | stars going out; the cool red ones outlast the rest |
| `grid` | space as a sheet, dented by something heavy |
| `beam` | light split into the colours it is made of |
| `entropy` | coloured blocks in a tidy row, scattering and never returning |
| `atom` | a speck of nucleus in an enormous gap, electrons far out |
| `flicker` | matter and antimatter, borrowed from nothing and paid back |
| `bloom` | rings pushing outward, each a different colour |
| `waves` | layered bands, motion without particles |
| `swarm` | a crowd of microbes, no two the same |
| `cells` | immune cells hunting invaders and swallowing them |
| `virus` | virus particles docking onto a cell |
| `colony` | ant trails between nests, traffic both ways |
| `telomere` | cells dividing, their protective caps shortening |
| `replace` | every piece swapped out, the shape still holding |
| `depths` | the ocean in zones, bioluminescence below the light |
| `crowd` | a crowd where most of the figures are the people already gone |
| `overgrow` | plants taking a city back |
| `sleepcycle` | a night of sleep, cycling through its stages |
| `attention` | focus sliding off the thing it is meant to be on |
| `pulse` | a rhythm slowing, and the pieces drifting free |
| `timewarp` | the same stretch of time, felt at two speeds |

Rules the file keeps:

- nothing animates off-screen; an `IntersectionObserver` parks each scene
- `prefers-reduced-motion` gets one composed static frame, never a frozen blank panel
- scenes are seeded from the slug, so a card looks identical on every load
- anything scrolled past without intersecting still reveals — a jumped-over element must
  never stay invisible
- point counts have a floor as well as a ceiling; a small card is a fraction of a hero's
  area, and without one a sparse scene reads as a broken panel

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
