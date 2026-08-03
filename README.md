# Context

Everyday things, properly explained. Ten questions people actually ask, each with a
short answer up front and something you can operate.

## The questions

| № | Question | Category |
|---|----------|----------|
| 01 | Why does a year feel faster every time? | Your head |
| 02 | Why do onions make you cry? | Kitchen |
| 03 | Is the big box actually cheaper? | Money |
| 04 | Why does your phone die in the cold? | Tech |
| 05 | Why is the fridge the worst place for bread? | Kitchen |
| 06 | How does a little money turn into a lot? | Money |
| 07 | Why does the shower curtain attack you? | Home |
| 08 | Why are yawns contagious? | Your head |
| 09 | Why does food taste like nothing with a cold? | Food |
| 10 | Why is the wifi terrible in one room? | Tech |

Every page follows the same shape: the question, the answer immediately, then a figure
you can play with, then the explanation. Nobody has to read to the bottom to find out.

## Design

The palette is built on colour-preference research rather than taste. Blue leads, because
it reliably tops adult preference. Six saturated hues span warm and cool so the page reads
bright to children as well as considered to adults. The layout stays deliberately
conventional and uncluttered — first impressions of a page form in well under 100ms, and
visual complexity costs more than novelty gains.

Every hue carries three tiers, because a saturated colour that looks right on white
usually fails contrast on it:

| tier | used for | requirement |
|------|----------|-------------|
| `wash` | card and panel grounds | decorative only |
| `bright` | figures, fills, controls | ≥ 3:1 on white |
| `ink` | text and labels | ≥ 4.5:1 on white |

All six hues pass at every tier; the check lives in the commit history. Backgrounds were
chosen first and text colours derived from them, not the other way round.

- Page `#FFFFFF` · surface `#F6F8FB` · ink `#16202B` · muted `#5A6875`
- Nunito (display) · Source Sans 3 (body), both self-hosted — no font CDN, no third-party
  request, nothing to leak
- The page commits to a light ground on purpose, so the tokens are theme-independent

## Structure

```
build.py         generates the site
topics_data.py   all content and figures — one dict per topic
assets/style.css the design system
assets/fonts/    self-hosted woff2
site/            build output, deploy this
```

Adding a question means appending one dict to `TOPICS` with `svg`, `controls`, `js` and
`sections`, then re-running `python3 build.py`. Nothing else changes.

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
tools, writing to `topics_data.py` via the GitHub API:

- `create_draft` — append a topic dict with `status: draft`
- `list_drafts`
- `update_draft`
- `publish` — flip status, commit, let the host rebuild

Keep `publish` as a separate human-triggered call. Accuracy is the product here, and a
wrong explanation costs more trust than a right one earns.
