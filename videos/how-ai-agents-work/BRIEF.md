---
workflow: faceless-explainer
flow: automation
storyboard: no
message: "An AI agent isn't one big model call — it's a loop: perceive, decide, act, observe, repeat, until the goal is done."
destination: shorts
aspect: 1080x1920
language: en
length: 45s
angle: concept
narration: yes
---

## Intent

A 9:16, ~45s faceless explainer that teaches a general audience how AI agents
work — the perceive → reason/plan → act → observe loop, tool use, memory, and
why that loop (not a single prompt) is what makes an agent "agentic." Visuals
are invented: animated typography and simple, self-drawing SVG diagrams
(the agent loop, a tool-call arrow, a memory store) rather than any real
product or footage. Clean, modern, technical-but-approachable tone — closer
to a well-produced tech-explainer short than a lecture.

## Customizations

- Voiceover + background music (both to be generated).
- Animated typography and simple SVG diagrams that draw themselves on-screen.
- Smooth transitions between sections.
- Strict safe-zone compliance: 150px top, 170px bottom, 60px sides — all text
  and key diagram elements must stay inside this band on the 1080x1920 canvas.

## Notes

- Run `lint`, `check` (and inspect the snapshot contact sheet) before
  rendering; render only after those pass.
- One user-requested checkpoint: pause and show the narrator script (Step 3)
  for explicit approval before generating any audio or visuals. This is a
  user override of the normal autonomous "post and continue" checkpoint
  behavior for this one gate only; all other checkpoints in this run proceed
  autonomously with a posted summary, per the request's own instructions.
