# Frame packet: 07-why-the-loop-wins

## Project inputs

- Project: /home/user/context/videos/how-ai-agents-work
- Design tokens: /home/user/context/videos/how-ai-agents-work/frame.md
- RULES_DIR: /root/.claude/skills/hyperframes-animation/rules

## Assigned storyboard block

## Frame 7 — Why the loop wins

- scene: Screen splits — left card "One prompt" freezes and cracks on a wrong turn; right card "The loop" keeps adapting, tries again, and a small memory icon persists beside it
- voiceover: "One prompt can't recover from a wrong turn. A loop notices — and tries again."
- duration: 5.12s
- transition_in: crossfade
- status: outline
- src: compositions/frames/07-why-the-loop-wins.html
- type: benefit_highlight
- persuasion: Before/after
- beat: Confidence + relief
- blueprint: comparison-split

narrativeRole: States the payoff of the mechanism just taught — why looping (with memory carried across iterations) beats a single best-effort answer.
keyMessage: A loop can notice a mistake and correct it; one shot can't.

- blueprint: comparison-split (Adapt) — the template's side-by-side wings don't fit a 9:16 canvas (portrait guidance: stack, don't split horizontally), so the two cards stack TOP/BOTTOM instead of left/right; keeps the signature mirrored book-open tilt entry + inner-edge badge pop
- focal: the two comparison cards — "One prompt" (top) and "The loop" (bottom)
- roles: both cards = foreground subject (equal weight, stacked) · title line = supporting lead-in · small memory icon on the loop card = supporting detail
- sfx: crack-tick (the "One prompt" card fracturing), soft-chime (the badge pop)

Adapt: `split-tilt-cards`' left/right wings become top/bottom wings for portrait; mirrored tilt becomes `rotateX` (top card tilts as if hinged open downward, bottom card hinged open upward) instead of `rotateY`; badges land at each card's inner edge (bottom of top card, top of bottom card) instead of left/right inner edges. Signature kept: opposite-wing entry with mirrored tilt, inner-edge badge pop as the one earned overshoot.
Scene 1 (0.0–1.0s): centered title "Why the loop wins" (`text`, with "loop" in `primary`) slides down into place from just above — short smooth settle. Two faint `card-bg` glow blooms establish top/bottom zones.
Scene 2 (1.0–2.8s): as the VO says "One prompt can't recover from a wrong turn," the **top card** ("One prompt") arrives from above with a mirrored `rotateX` book-open tilt, scaling ~0.85→1; a thin crack-line draws across it (`svg-path-draw`) as it settles — freezing on the fracture.
Scene 3 (2.8–5.12s): as the VO says "A loop notices — and tries again," the **bottom card** ("The loop") arrives from below ~0.2s behind with the opposing tilt, a small memory-icon chip persists beside it (still visible, not fading), and a pill badge spring-pops at each card's facing inner edge (top card's bottom edge, bottom card's top edge) — the one earned overshoot in the video. Settles and holds.

## Selected blueprint: comparison-split

# comparison-split — Comparison Split-Cards

**intent**: Two paired items of equal weight shown side-by-side with mirrored 3D "book-open" tilts — the eye reads them as a balanced comparison, then a pill badge lands at each card's inner edge to punctuate. The motion IS the symmetry: two cards arriving from opposite wings into a held spread.

**roles served**

- Key_Feature (from `comparison-split-cards`): when two complementary features / capabilities of equal weight should be presented **simultaneously, not sequentially** — an A/B, a "X + Y together," paired concepts the viewer must weigh side-by-side. Not for >2 items (use `grid-card-assemble`) or sequential steps.

**duration**: 4–6s

**shot structure** (a `[bg]` canvas carrying two faint ambient glow blooms — `[accent A]` near 30%, `[accent B]` near 70% — so each side owns a color identity across a 50% symmetry axis; equal-width cards under one shared perspective parent)

- **Scene 1 (0.0–~0.8s) — title sets the concept.** A centered `[title line]` with an `[accent keyword]` slides DOWN into place from just above (a short smooth settle). The downward arrival is deliberate: it forms a non-conflicting T-shape against the cards, which arrive from the sides next.
- **Scene 2 (~0.4–1.9s) — the split-tilt entry (signature move).** Two equal-width feature cards arrive from opposite wings — `[left card]` from the left, `[right card]` from the right ~0.2s behind — each carrying a **mirrored 3D `rotateY` tilt** (left faces right, right faces left, opening like a book) and scaling ~0.85→1 as it lands. The entry overlaps the title's tail so the whole thing reads as ONE arrival, not two beats. Each card holds `[image / label / subtitle]`; box-shadows fall **outward** from the tilt (left shadow right, right shadow left).
- **Scene 3 (~1.9–end) — badges punctuate, then hold.** A pill `[badge]` lands at each card's **inner edge** (left then right, ~0.3s apart), overlapping its card ~15% so it reads as attached, not orbiting. This is the lone overshoot in the shot — it earns the punctuation. Settles and holds.

**motion vocabulary**: title slide-down from above; mirrored opposite-wing card entry; static book-open `rotateY` tilt (`+tilt` left, `−tilt` right); tilt-matched outward box-shadow; inner-edge badge spring-pop; gentle phase-opposed idle float (left vs right, never synchronized) registered as subtle jitter; dual side-glow ambient.

**rule mapping**

- two cards entering from opposite wings with mirrored `rotateY` tilts + tilt-matched shadow → `split-tilt-cards` (the signature; keep the two-layer split so the entry `x`/`scale` and the idle never collide on one alias)
- title slide-down settle → `gsap-effects` (translate + opacity on a long-tail `power3`)
- inner-edge pill badge pop (the one overshoot) → `spring-pop-entrance` (overshoot register — earns the punctuation)
- phase-opposed idle float on the pair → `sine-wave-loop` (low-amplitude register — subtle jitter, NOT lazy breathing; left `sin(t)`, right `sin(t+π)` so they never conveyor-belt)
- the two faint side glows behind the cards → `ambient-glow-bloom` (un-triggered soft bloom, one per accent)

**camera modifier**: camera-static by default — the symmetry is the subject and a move would break the balance.

## Selected motion rule: split-tilt-cards

---
name: split-tilt-cards
description: Two cards side-by-side with opposing Y-rotation creating a symmetric 3D split-screen layout for comparisons or feature pairs.
metadata:
  tags: 3d, cards, split, tilt, comparison, symmetric, layout
---

# Split Tilt Cards

Two cards side-by-side with opposing `rotateY` (left `+TILT`, right `−TILT`) — a symmetric "book-open" 3D split for comparisons, before/after, feature pairs. Each card slides in from its own side (reinforcing "they came from their own worlds and met here"), then the pair idles in counter-phase.

## How It Works

`perspective` on the scene root (REQUIRED — without it `rotateY` flattens to a 2D layout) and `transform-style: preserve-3d` on the stage and both cards. Entry starts each card off-axis with `TILT + TILT_OVERSHOOT`, settling to `TILT` — a pivot-into-place. Idle is a gentle counter-phase y-bob (the two yoyo tweens run in opposite directions); copy fades up during the cards' settle, not after.

## Recipe

```html
<!-- inside a standard scene clip (hyperframes-core) -->
<div class="split-stage">
  <div class="card card-left">
    <div class="card-eyebrow">{leftEyebrow}</div>
    <div class="card-headline">{leftHeadline}</div>
    <div class="card-body">{leftBody}</div>
  </div>
  <div class="card card-right">…</div>
</div>
```

```css
.scene-root {
  display: grid;
  place-items: center;
  perspective: SCENE_PERSPECTIVE; /* REQUIRED */
}
.split-stage {
  display: flex;
  gap: STAGE_GAP;
  transform-style: preserve-3d;
}
.card {
  width: CARD_WIDTH;
  transform-style: preserve-3d;
  will-change: transform;
}
/* Shadow falls WITH the facing direction: left card faces right → shadow right. */
.card-left {
  box-shadow: -CARD_SHADOW_OFFSET CARD_SHADOW_DROP CARD_SHADOW_BLUR {shadowColor};
}
.card-right {
  box-shadow: CARD_SHADOW_OFFSET CARD_SHADOW_DROP CARD_SHADOW_BLUR {shadowColor};
}
```

```js
// Entry — from outside, opposing tilts settle with a small pivot
tl.fromTo(
  ".card-left",
  { x: -ENTRY_SLIDE_DIST, rotateY: TILT + TILT_OVERSHOOT, opacity: 0 },
  { x: 0, rotateY: TILT, opacity: 1, duration: ENTRY_DUR, ease: "power3.out" },
  LEFT_AT,
);
tl.fromTo(
  ".card-right",
  { x: ENTRY_SLIDE_DIST, rotateY: -TILT - TILT_OVERSHOOT, opacity: 0 },
  { x: 0, rotateY: -TILT, opacity: 1, duration: ENTRY_DUR, ease: "power3.out" },
  RIGHT_AT,
);

// Counter-phase idle bob — opposite signs = alive; synchronized = conveyor belt
tl.to(
  ".card-left",
  { y: -FLOAT_AMP, duration: FLOAT_DURATION / 2, ease: "sine.inOut", yoyo: true, repeat: 1 },
  IDLE_START,
);
tl.to(
  ".card-right",
  { y: FLOAT_AMP, duration: FLOAT_DURATION / 2, ease: "sine.inOut", yoyo: true, repeat: 1 },
  IDLE_START,
);

// Copy fades up during the settle
tl.from(
  ".card-eyebrow, .card-headline, .card-body",
  { opacity: 0, y: COPY_RISE, stagger: COPY_STAGGER, duration: COPY_DUR, ease: "power2.out" },
  COPY_REVEAL_AT,
);
```

## Variations

- **Badges / floating labels**: position them on the PARENT, never inside a card — inside they inherit the `rotateY` and tilt off-axis.
- **3+ cards**: center card stays flat (`rotateY: 0`), outer two tilt inward — "old way / nothing / our way."
- **Zoom-through**: a separate camera tween scaling `.split-stage` reads as the viewer crossing the gap between the tilted pair.

## Values

| token             | range                            | notes                                                   |
| ----------------- | -------------------------------- | ------------------------------------------------------- |
| SCENE_PERSPECTIVE | 1000–2400px                      | lower exaggerates the tilt; higher reads near-isometric |
| TILT              | 10–18°                           | < 10 reads almost flat; > 18 folds shut and copy blurs  |
| TILT_OVERSHOOT    | 4–12°                            | the pivot-into-place feel                               |
| STAGE_GAP         | 40–120px (~0.06–0.15×CARD_WIDTH) | small = fused pair; large = compared-but-separate       |
| CARD_WIDTH        | 480–820px @1920                  | `2×CARD_WIDTH + STAGE_GAP ≤ 0.95×stage` at full tilt    |
| ENTRY_SLIDE_DIST  | 200–500px (~0.3–0.6×CARD_WIDTH)  |                                                         |
| ENTRY_DUR         | 0.6–1.2s                         |                                                         |
| RIGHT_AT          | LEFT_AT + 0–0.3s                 | zero feels mechanical; large fragments the pair         |
| FLOAT_AMP         | 3–8px                            | subtle is the point                                     |
| FLOAT_DURATION    | 1.6–3.2s round trip              | breathing cadence; IDLE_START ≥ entry end               |
| COPY_REVEAL_AT    | during the entry tail            | copy popping in after cards are idle reads disconnected |

## Critical Constraints

- **`perspective` on the scene root is REQUIRED**; `preserve-3d` on the stage AND each card.
- **Shadow direction matches tilt** — left card faces right → shadow falls right (and mirrored). Wrong sign reads as broken 3D.
- **Counter-phase idle** — the two bobs run with opposite signs at the same position.
- **Badges outside the card divs** (they'd inherit the rotation).
- **Body copy ≤ 2 lines per card** — tilted long paragraphs collapse into perspective blur.
- **Symmetric weight** — same width, same vertical center, similar line counts; asymmetry breaks the comparison metaphor.

## See also

`card-morph-anchor` (the pair can morph into one unified shape afterward) · `counting-dynamic-scale` (numbers as each side's headline) · `sine-wave-loop` (the idle form).

## Selected motion rule: svg-path-draw

---
name: svg-path-draw
description: Animate SVG paths drawing progressively using stroke-dasharray and stroke-dashoffset.
metadata:
  tags: svg, stroke, draw, path, reveal, icon, vector
---

# SVG Path Draw

Reveals an SVG shape by animating its stroke as if a pen were tracing it. Two stroke properties together: **`stroke-dasharray = <pathLength>`** makes the entire path one dash; **`stroke-dashoffset`** starts at the path length (dash shifted fully out of view → invisible) and tweens to `0` (fully drawn). The length comes from the DOM API `path.getTotalLength()` — measured, never guessed.

Works on anything with a stroke: `<path>`, `<circle>`, `<rect>`, `<line>`, `<polyline>`, `<polygon>`, `<ellipse>`.

## Recipe

```html
<!-- inside a standard scene clip -->
<svg class="logo-mark" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <path id="bar-left" d="M 60 40 L 60 160" />
  <path id="bar-right" d="M 140 40 L 140 160" />
  <path id="bar-mid" d="M 60 100 L 140 100" />
</svg>
```

```css
.logo-mark path {
  fill: none; /* outline-only draw — a fill would appear immediately and ruin the reveal */
  stroke: {accentColor};
  stroke-width: 12;
  stroke-linecap: round; /* softer endpoints */
  stroke-linejoin: round;
}
```

```js
// Setup: measure each path and set its dash pattern. Real measured geometry, not a magic number.
document.querySelectorAll(".logo-mark path").forEach((p) => {
  const len = p.getTotalLength();
  p.style.strokeDasharray = `${len}`;
  p.style.strokeDashoffset = `${len}`;
});

// Stagger draws so the eye reads continuous motion — each segment starts at
// ~70-80% of the previous segment's duration, before it finishes.
tl.to(
  "#bar-left",
  { strokeDashoffset: 0, duration: SEGMENT_DRAW_DUR, ease: "power2.out" },
  SEG_1_START,
);
tl.to(
  "#bar-right",
  { strokeDashoffset: 0, duration: SEGMENT_DRAW_DUR, ease: "power2.out" },
  SEG_2_START,
);
tl.to(
  "#bar-mid",
  { strokeDashoffset: 0, duration: FINAL_SEGMENT_DUR, ease: "power2.out" },
  SEG_3_START,
);

// Companion wordmark fades in only after the last stroke settles.
tl.to(
  ".brand-line",
  { opacity: 1, duration: BRAND_FADE_DUR, ease: "power1.out" },
  BRAND_FADE_START,
);
```

## Variations

- **Ring starting at 12 o'clock** — `<circle>` / `<rect>` strokes start at 3 o'clock by default; rotate the element `-90deg` so a progress ring draws from the top:

```html
<circle
  cx="100"
  cy="100"
  r="60"
  id="ring"
  style="transform-origin: 100px 100px; transform: rotate(-90deg)"
/>
```

- **Linear (constant-speed) draw** — `ease: "none"` for a steady-rate "real pen" trace.
- **Draw then fill** — for filled shapes, tween `fillOpacity: 0 → 1` AFTER the stroke completes (requires `fill-opacity: 0` initially and a real `fill` in CSS):

```js
tl.to(
  "#path",
  { strokeDashoffset: 0, duration: SEGMENT_DRAW_DUR, ease: "power2.out" },
  SEG_1_START,
);
tl.to(
  "#path",
  { fillOpacity: 1, duration: FILL_FADE_DUR, ease: "power1.out" },
  SEG_1_START + SEGMENT_DRAW_DUR,
);
```

## Values

| token             | range                                   | notes                                                                                              |
| ----------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------- |
| SEGMENT_DRAW_DUR  | 0.3–0.8s                                | fast snap vs deliberate pen trace; >~1s feels sluggish for a logo reveal                           |
| FINAL_SEGMENT_DUR | 60–80% of SEGMENT_DRAW_DUR              | proportional to segment length — a short connector at full duration reads slower than its siblings |
| SEG_N_START       | previous start + 70–80% of its duration | reads as continuous motion, not N isolated animations                                              |
| SEG_1_START       | 0–0.4s                                  | a small ~0.2s lead-in lets the viewer settle before motion                                         |
| BRAND_FADE_START  | ≥ last stroke end (+ ~0.2s beat)        | earlier and the wordmark competes with the draw                                                    |
| BRAND_FADE_DUR    | 0.3–0.8s                                | snap (urgent) vs glide (premium)                                                                   |

Ease families are discrete choices: **stroke draws** use `power2.out` (a hand lifting at end of stroke) or `none` for constant speed — never `back.out` / `elastic.out` (pens don't bounce). **Fades** use `power1.out`.

## Critical Constraints

- **`fill: none`** for outline-only draws — otherwise the fill appears immediately.
- **Dasharray/dashoffset = the measured `getTotalLength()`**, set at setup; requires the SVG in the DOM (inline SVG is fine; a loaded `<image>` SVG is not).
- **Complex paths**: if `getTotalLength()` looks wrong, overestimate slightly (`len * 1.05`) — too large is invisible at animation start; too small clips the end.
- **Stagger multi-path draws at ~70–80%** of the previous segment's duration.

## See also

`svg-icon-enrichment` (internal parts animate after the outline draws) · `counting-dynamic-scale` (stroke draws an icon while a number counts up) · `hacker-flip-3d` (logo draws, wordmark decodes beneath).
