---
format: 1080x1920
duration: 38.934s
message: "An AI agent isn't one big model call — it's a loop: perceive, decide, act, observe, repeat, until the goal is done."
arc: concept-explainer with process
audience: general tech-curious viewers, Shorts/TikTok
mode: autonomous
music: confident minimal tech underscore
---

## Video direction

- **Palette (from `frame.md`, blue-professional):** `bg` (cream `#fdfae7`) is the only ground. `primary` (cobalt `#1e2bfa`) is the single accent — every active node, drawn arrow, highlighted word, and key number is `primary`; nothing else touches color. Body/display type is `text`; secondary labels are `text-muted`; de-emphasized supporting copy is `text-light`. Cards (Frame 7) use `card-bg` (cobalt @4%) with a `border` (cobalt @20%) — no shadows anywhere (the preset is shadow-free by design).
- **Safe zone (explicit user spec, overrides the generic caption-band default — captions are skipped this build, no transcription provider available):** every text element and load-bearing diagram part stays inside **150px top / 170px bottom / 60px sides** on the 1080×1920 canvas. Centered heroes anchor around **y ≈ 620–650px** (upper-middle), not the raw canvas midpoint (960px), so nothing crowds the bottom margin.
- **Motion grammar + reveal model:** long-tail `power3` settles everywhere (→ `motion-language.md` doctrine #1) — no bounce, no overshoot except the ONE earned inner-edge badge pop in Frame 7 (comparison-split's signature). Every frame reveals **paced to its voiceover cue** — nothing front-loads before the VO says it; the back ~50% of each frame carries the payoff. Holds use **subtle jitter at most**, never lazy breathing, never a back-half pan/push.
- **The shared stage (Frames 3–6):** one self-drawing loop diagram — 4 nodes (Perceive · Reason · Act · Observe) at 12/3/6/9 o'clock on a ring centered at (540, 630), ring diameter ~520px (≈48% of canvas width). Each frame draws ONE new arc + highlights ONE new node via `svg-path-draw`; prior nodes/arcs stay visible but dim to ~65% opacity (supporting, not foreground) so the diagram visibly accumulates across the 4 frames — this is the continuity device (`visual-design.md` "consistent stage"), not 4 unrelated diagrams. Frame 6's final arc closes the ring back onto Perceive and the whole ring pulses once (a finite glow bloom, never a loop/repeat).
- **Rhythm / held-frame allocation:** Frame 8 (the thesis) is the video's deliberate breather — content resolves early in its shot and holds dead still for the back half (`titlecard-reveal`'s "allocated stillness"). Frame 1's final beat and Frame 9's final beat also hold on their landed line (kinetic-type-beats resolve-and-hold). Frames 3–6 stay in continuous, brisk sequential motion (the mechanism assembling) — the contrast between the busy middle and the two calm bookends (open beat / thesis) is intentional.
- **Framing variety (≥3 across the video, per Layout guidance):** Frame 1–2 = centered kinetic type; Frames 3–6 = centered ring diagram (a fixed "stage" framing, counted once); Frame 7 = split-screen comparison; Frame 8–9 = centered titlecard. That's 4 distinct framings.
- **Negative list:** no default-AI cliché (floating bokeh, purple-blue ambient gradients); no `back.out`/`bounce.out`/`elastic.out` outside Frame 7's one earned badge pop; no lazy breathing; no slow pan/push in any frame's back half; no `repeat`/`yoyo`/`Math.random`/`Date.now`; no browser chrome, cursors, or nav bars (nothing here is a UI reconstruction); no front-load-then-freeze (slideshow) and no everything-floating-independently (screensaver).

## Frame 1 — Hook

- scene: Bold centered type states the common belief, then a hard cut swaps it for the twist
- voiceover: "\"AI agent\" isn't one smart answer — it's a tiny loop, on repeat."
- duration: 4.651s
- transition_in: cut
- status: animated
- src: compositions/frames/01-hook.html
- type: hook
- persuasion: Common-belief vs reality
- beat: Puzzlement + intrigue
- blueprint: kinetic-type-beats

narrativeRole: Opens a gap between what people assume "AI agent" means (one smart answer) and the actual mechanism (a small repeating loop).
keyMessage: An AI agent is not one big clever response — it's a loop.

- blueprint: kinetic-type-beats (Adapt) — sub-shape B multi-beat statement build, 2 beats instead of the template's 3; keeps the hard-cut beat-swap signature
- focal: the words "one smart answer" (beat 1) → "a tiny loop, on repeat" (beat 2)
- roles: hook line = foreground subject (full-bleed centered type) · flat cream field = background
- sfx: whoosh-soft (the hard cut between beats)

Adapt: keep the fixed-center hard-cut beat-swap; compress to 2 beats to match the VO's two clauses.
Scene 1 (0.0–2.0s): flat `bg` field. Bold centered headline (display type) hard-cut FLASH-in, `text` color: **"AI agent" isn't one smart answer —**. Camera locked. Nothing else on screen — centered framing, ~55% of frame width.
Scene 2 (2.0–3.2s): as the VO lands "it's a tiny loop, on repeat," the beat-1 line hard-cuts away (no fade/slide) and beat-2 replaces it center: **"it's a tiny loop, on repeat."** — the word "loop" set in `primary` (cobalt) as the one accent word, rest in `text`.
Scene 3 (3.2–4.651s): beat 2 holds dead still — settle-and-hold, at most subtle jitter. No further motion; this is the video's cold open, resolve and let it read.

## Frame 2 — Name the loop

- scene: Four words punch in one at a time — perceive, reason, act, observe — then hold together as a labeled set
- voiceover: "Four moves — perceive, reason, act, observe — that's the whole engine."
- duration: 4.288s
- transition_in: crossfade
- status: animated
- src: compositions/frames/02-name-the-loop.html
- type: product_intro
- persuasion: Frame-then-fill (state the shape, then populate it)
- beat: Clarity + orientation
- blueprint: kinetic-type-beats

narrativeRole: Names the concept the rest of the video will unpack — the four-step loop is the "protagonist."
keyMessage: The whole agent engine is four repeating moves.

- blueprint: kinetic-type-beats (Adapt) — flat-field-kinetic-word-run variant: the sentence builds word-by-word, each of the four role-words earning its own small pop, ending held as a labeled set (no hero-word effect payoff, no finale scale chain — the naming itself is the payoff)
- focal: the four role-words — perceive · reason · act · observe
- roles: "Four moves —" = supporting lead-in (smaller, `text-muted`) · the four role-words = foreground subject (large, `primary`) · "that's the whole engine" = supporting close (`text-muted`, smaller, arrives last)
- sfx: tick ×4 (one per word landing)

Adapt: word-by-word build via `dynamic-content-sequencing`; kept the per-word pop signature, dropped the hero-word effect payoffs (too busy for a 4.3s naming beat).
Scene 1 (0.0–0.9s): flat `bg` field. "Four moves —" fades/scales in small, upper-center (`text-muted`, ~0.42×height), smooth `power3` settle. Nothing else yet.
Scene 2 (0.9–3.0s): as the VO names each word, **perceive**, **reason**, **act**, **observe** pop in one at a time (spring-pop entrance, smooth register — no overshoot), left-to-right in a single centered row, each in `primary` — four beats landing roughly every 0.5s, matched to the VO's own cadence naming them.
Scene 3 (3.0–4.288s): "that's the whole engine" fades up beneath the four words (`text-muted`, small) as all four hold together as one labeled set — settle and hold, subtle jitter only.

## Frame 3 — Perceive

- scene: A self-drawing circular loop diagram appears; the "Perceive" node lights up first and a small readout shows goal / context / last result flowing in
- voiceover: "First: perceive. It reads the goal, the context — and what just happened."
- duration: 4.523s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/03-perceive.html
- type: feature_showcase
- persuasion: Signposting (first… then… finally)
- beat: Comprehension
- blueprint: (none — bespoke diagram beat, composed from motion-language + SVG draw-on rules)

narrativeRole: Establishes the consistent loop-diagram stage and teaches the first step: the agent gathers everything it currently knows.
keyMessage: Perceive = read the goal, the context, and the last result.

- blueprint: compose (no blueprint fits a self-drawing cyclic diagram; built from the motion vocabulary — this frame opens the shared stage described in Video direction)
- focal: the Perceive node (12 o'clock on the ring)
- roles: ring diagram = foreground subject, centered at (540, 630), ~48% of canvas width · Perceive node + its readout card = foreground (full brightness, `primary`) · the other 3 ring positions = supporting (faint dotted placeholders, `text-light`, not yet drawn)
- sfx: svg-draw-tick (the ring outline stroking in)

Compose: first frame on the stage, so it also establishes the ring itself.
Scene 1 (0.0–1.0s): flat `bg` field, faint dotted full ring pre-sketched at ~15% opacity (`text-light`) so the viewer senses "4 positions" before anything is named — this is ambient staging, not a reveal. Nothing else on screen yet (VO hasn't started the first cue).
Scene 2 (1.0–2.6s): as the VO says "First: perceive," the Perceive node (top, 12 o'clock) draws on via **SVG self-draw** (`svg-path-draw`) — a solid `primary` ring outline strokes in around it, then the node fills and glows once (finite bloom, `ambient-glow-bloom`). Label "PERCEIVE" (mono/micro type) settles beside it.
Scene 3 (2.6–4.523s): as the VO names "the goal, the context — and what just happened," three small readout chips **stagger in** beside the node, one per phrase (`dynamic-content-sequencing`, per-word/per-chunk staggered reveal), each a short label: "goal" → "context" → "last result" — arriving left-to-right, timed to the three spoken cues, then holds. Camera locked throughout; no push/pan.

## Frame 4 — Reason / Plan

- scene: Same loop diagram; the arrow draws forward from Perceive to the Reason node, which lights up as a single question mark resolves into "next step"
- voiceover: "Then: reason. Given all that, what's the single best next step?"
- duration: 4.032s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/04-reason.html
- type: feature_showcase
- persuasion: Signposting (first… then… finally)
- beat: Focus + anticipation
- blueprint: (none — bespoke diagram beat, same stage as Frame 3)

narrativeRole: Second step on the same stage — the model decides the next single move rather than planning everything up front.
keyMessage: Reason = pick just the next best step, not the whole plan.

- blueprint: compose (same bespoke stage as Frame 3)
- focal: the Reason node (3 o'clock) + the arc connecting Perceive → Reason
- roles: Reason node + its arc = foreground (full brightness) · Perceive node/readout from Frame 3 = supporting (dims to ~65% opacity, stays visible — the accumulating diagram) · the other 2 ring positions = supporting (faint dotted, untouched)
- sfx: svg-draw-tick

Compose: continues the stage opened in Frame 3; Perceive's readout chips clear/dim as this node takes focus.
Scene 1 (0.0–0.8s): Perceive node + chips settle to ~65% opacity (a quick, smooth dim — not a hard cut) as the frame opens; ring otherwise unchanged from Frame 3's end state. Camera locked.
Scene 2 (0.8–2.2s): as the VO says "Then: reason," an arc **self-draws** clockwise from Perceive to the Reason position (3 o'clock, `svg-path-draw`), the Reason node fills solid `primary` and glows once.
Scene 3 (2.2–4.032s): as the VO asks "what's the single best next step?" a small "?" glyph appears inside the Reason node, then — timed to "next step" — **morphs/resolves** (`scale-swap-transition`, same-center handoff) into a short label "next step" beside it. Holds; subtle jitter only.

## Frame 5 — Act

- scene: Same loop diagram; the arrow draws to the Act node, which fans out into three small tool icons (search, code, API) as one is selected and fires
- voiceover: "Next: act. Call a tool — search, run code, hit an API."
- duration: 4.117s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/05-act.html
- type: feature_showcase
- persuasion: Concretization (abstract → tangible object)
- beat: Momentum
- blueprint: (none — bespoke diagram beat, same stage as Frames 3-4)

narrativeRole: Third step — makes "acting" concrete as a tool call with a real effect, not more talk.
keyMessage: Act = call a tool and touch the real world.

- blueprint: compose (same bespoke stage as Frames 3-4)
- focal: the Act node (6 o'clock) + the arc connecting Reason → Act
- roles: Act node + arc + the 3 tool chips = foreground · Perceive/Reason nodes = supporting (dimmed ~65%) · Observe position = supporting (faint dotted, untouched)
- sfx: svg-draw-tick, soft-click (the tool selection)

Compose: third step on the accumulating stage.
Scene 1 (0.0–0.7s): Reason node settles to ~65% opacity; ring otherwise as Frame 4 left it.
Scene 2 (0.7–2.0s): as the VO says "Next: act," an arc self-draws from Reason to Act (6 o'clock, `svg-path-draw`); Act node fills `primary` and glows once.
Scene 3 (2.0–4.117s): as the VO enumerates "search, run code, hit an API," three small tool-icon chips **fan out** from the Act node in a staggered reveal (`dynamic-content-sequencing`, one per named tool, matched to each word), then as the line ends, one chip **scales up and glows** (selected) while the other two settle dim — makes "calling a tool" concrete as a single decisive action, not a menu. Holds.

## Frame 6 — Observe, then repeat

- scene: Same loop diagram; the arrow draws to the Observe node, then one final arrow draws all the way back to Perceive, closing the circle, which pulses once
- voiceover: "Finally: observe what happened — then loop back to perceive, and go again."
- duration: 4.651s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/06-observe-repeat.html
- type: feature_showcase
- persuasion: Causal chain (A → B → C)
- beat: "Aha" + momentum
- blueprint: (none — bespoke diagram beat, closes the stage opened in Frame 3)

narrativeRole: Completes the loop diagram and makes the repetition itself visible — the mechanism that was named in Frame 2 is now fully shown.
keyMessage: Observe = check the result, then the whole loop runs again.

- blueprint: compose (closes the bespoke stage opened in Frame 3)
- focal: the Observe node (9 o'clock) + the closing arc back to Perceive
- roles: Observe node + both arcs (Act→Observe, Observe→Perceive) = foreground · all 4 nodes = full brightness by Scene 3 (the completed diagram) · tool chips from Frame 5 = supporting, dimmed
- sfx: svg-draw-tick, soft-chime (the ring closing)

Compose: the payoff frame for the whole diagram sequence — ends on the completed, closed ring.
Scene 1 (0.0–0.7s): Act node + tool chips settle to ~65% opacity; ring as Frame 5 left it (3 of 4 nodes lit, 3 arcs partial).
Scene 2 (0.7–2.2s): as the VO says "Finally: observe what happened," an arc self-draws from Act to Observe (9 o'clock); Observe node fills `primary` and glows once — all 4 nodes now lit.
Scene 3 (2.2–4.651s): as the VO says "then loop back to perceive, and go again," the FINAL arc self-draws from Observe back to Perceive, **closing the ring** — on landing, the whole ring pulses once with a finite glow bloom (`ambient-glow-bloom`, one-shot, never a repeat/loop animation) and the 4 nodes brighten together for a beat, then settle and hold. This is the diagram's resolved, completed state — the teaching payoff of Frames 3–6.

## Frame 7 — Why the loop wins

- scene: Screen splits — left card "One prompt" freezes and cracks on a wrong turn; right card "The loop" keeps adapting, tries again, and a small memory icon persists beside it
- voiceover: "One prompt can't recover from a wrong turn. A loop notices — and tries again."
- duration: 5.12s
- transition_in: crossfade
- status: animated
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

## Frame 8 — The thesis

- scene: One clean centered line settles on a calm, still frame — the whole idea distilled
- voiceover: "That's the whole trick — a model in a loop, with tools and memory."
- duration: 3.84s
- transition_in: crossfade
- status: animated
- src: compositions/frames/08-thesis.html
- type: branding
- persuasion: Distillation (compress to one line)
- beat: Clarity + satisfaction, "now I get it"
- blueprint: titlecard-reveal

narrativeRole: Lands the video's one-sentence takeaway as a calm, quotable landing beat.
keyMessage: A model, a loop, tools, and memory — that's an agent.

- blueprint: titlecard-reveal (Reproduce) — Benefits variant (calm empty-to-text open, one slide-up crossfade, held read)
- focal: the thesis line
- roles: thesis line = foreground subject (centered, ~55% of frame width) · flat cream field = background, no supporting elements — deliberately empty, this is the held breather
- sfx: none (this frame is the video's quiet beat)

Reproduce: template's single restrained move, applied directly — no adaptation needed.
Scene 1 (0.0–0.5s): empty flat `bg` field — no busy open, matching the template's Benefits variant.
Scene 2 (0.5–1.6s): the thesis line fades in centered while scaling slightly (~95%→100%, smooth `power3` ease-out): **"That's the whole trick —"** (`text`).
Scene 3 (1.6–3.84s): the ONE move — the line slides up and fades as the second half **"a model in a loop, with tools and memory"** slides up from below-center and fades in to take its place (loop/tools/memory in `primary`); holds to the end. No second development phase — this is the video's designated stillness (Video direction).

## Frame 9 — Close

- scene: Closing line types/settles in, camera holds still, fade to end
- voiceover: "Next time you see \"AI agent\" — look for the loop underneath."
- duration: 3.712s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/09-close.html
- type: cta
- persuasion: Generalization (specific → principle)
- beat: Inspiration + resolve
- blueprint: kinetic-type-beats

narrativeRole: Converts the explanation into a lasting habit of mind — a call to notice the mechanism, not just recall the definition.
keyMessage: Look for the loop underneath any "AI agent" claim.

- blueprint: kinetic-type-beats (Adapt) — CTA variant, 2 value-line beats clearing to a held final line; no logo/URL lockup (faceless — nothing to brand)
- focal: "Next time you see 'AI agent'" (beat 1) → "look for the loop underneath" (beat 2, held)
- roles: both lines = foreground subject, centered · flat cream field = background
- sfx: soft-chime (the final line landing)

Adapt: CTA template's line-clears-to-brand-lockup becomes line-clears-to-held-line (no brand mark exists in a faceless explainer) — signature kept: each value line clears by hard cut/fade, final line holds as the video's last frame.
Scene 1 (0.0–1.8s): centered line fades/scales in: **"Next time you see \"AI agent\" —"** (`text`, quote marks in `text-muted`).
Scene 2 (1.8–3.712s): as the VO lands "look for the loop underneath," the first line clears (fade + slight scale-down) and the closing line fades/scales in to take its place: **"look for the loop underneath."** — "loop" in `primary`. This is the video's final frame: it holds to the very last frame (real exit, no further transition) — settle only, subtle jitter at most.
