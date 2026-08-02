# Errata

Ten interactive science explainers. Each plate states the wrong model you probably
carry, then hands you the mechanism and lets you operate it.

## The plates

| № | Title | Corrects |
|---|---|---|
| 01 | The moon does not pull the sea toward it | one tidal bulge → two |
| 02 | Summer is not when Earth is closer to the sun | distance → axial tilt |
| 03 | The sunset is red for the same reason the sky is blue | dust → Rayleigh scattering |
| 04 | Air does not have to meet up at the back of the wing | equal transit → circulation |
| 05 | Atoms do not get old before they decay | ageing → memoryless probability |
| 06 | Entropy is not messiness | disorder → counting microstates |
| 07 | Moving clocks are not malfunctioning | mechanical fault → longer light path |
| 08 | Exponential growth looks like nothing until everything | linear intuition → doubling time |
| 09 | Evolution is not random | chance → chance plus a non-random filter |
| 10 | Electrons crawl through a wire slower than you walk | electron speed → field propagation |

## Design language

The identity is the two-state figure. Every plate carries the same switch: the
drained dusty blue (`#5E7F8C`) is always the assumption, the correction rose
(`#F2557A`) is always the mechanism, and rose appears nowhere else on the site.
You learn by flipping between the wrong picture and the right one and watching the
wrong one fail.

- Ink `#0C1B1F` · bone `#EDE7DA` · assume `#5E7F8C` · correct `#F2557A`
- Fraunces (display) · IBM Plex Sans (body) · IBM Plex Mono (figure labels, readouts)
- Every figure is hand-built SVG driven by real physics — the sky colours are
  computed from exp(−τ·airmass), the seasons readout uses actual solar declination,
  the drift velocity is I/(nAe) for copper.

## Structure

```
build.py          generates the site
plates_data.py    all content and figures — one dict per plate
assets/style.css  the design system
site/             build output, deploy this
```

Adding a plate means appending one dict to `PLATES` with `svg`, `controls`, `js`
and `modules`, then re-running `python3 build.py`. Nothing else changes.

## Running locally

```bash
python3 build.py
python3 -m http.server 8000 --directory site
```

## Deploying

No build tooling, no dependencies, no framework. Any static host works.

**GitHub Pages** — already wired up. `.github/workflows/deploy.yml` publishes
`site/` on every push. Set Settings → Pages → Source to **GitHub Actions** once,
and the site goes live at https://ajithrajmenon.github.io/context/.

The workflow runs `python3 build.py` first if that file is present, and
otherwise publishes the committed `site/` as-is — so it keeps working whether or
not the generator lives in the repo.

**Cloudflare Pages / Netlify / Vercel** — push the repo, set the publish
directory to `site` and the build command to `python3 build.py`. Or just drag the
`site` folder onto Netlify Drop for an instant URL.

## Wiring it to Claude later

The generator is deliberately data-driven so an MCP server has an obvious
surface. Four tools, writing to `plates_data.py` via the GitHub API:

- `create_draft` — append a plate dict with `status: draft`
- `list_drafts`
- `update_draft`
- `publish` — flip status, commit, let the host rebuild

Keep `publish` as a separate human-triggered call. Accuracy is the product here,
and a wrong explanation costs more trust than a right one earns.
