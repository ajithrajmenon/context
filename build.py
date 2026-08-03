#!/usr/bin/env python3
"""Builds Context into site/.

No dependencies and no framework — read stories_data.py, write HTML.

    site/index.html          the homepage
    site/stories.html        every story, filterable
    site/stories/<slug>.html one story

A story is a stack of cards, and colour belongs to the card rather than
the page, so a piece walks through several tones as it goes. Adding a
story means appending one dict to STORIES and running this again.
Categories are derived from the stories, so a new subject needs no other
change.
"""
import os
import shutil

import diagram
import illustrate
from stories_data import STORIES

# The stories name scenes in the old vocabulary; each maps onto one of the
# generated illustrations. Keeping the map here means story data never had
# to be rewritten when the artwork changed medium.
ART = {
    'entropy': 'time',
    'expand': 'cosmos', 'stars': 'cosmos', 'dying': 'cosmos', 'orbit': 'cosmos',
    'atom': 'matter', 'flicker': 'matter', 'bloom': 'matter', 'grid': 'matter',
    'beam': 'sun',
    'waves': 'ocean', 'depths': 'ocean',
    'cells': 'cell', 'swarm': 'cell', 'virus': 'cell',
    'telomere': 'cell', 'replace': 'cell',
    'crowd': 'crowd', 'overgrow': 'city', 'colony': 'colony',
    'sleepcycle': 'mind', 'attention': 'mind', 'timewarp': 'mind', 'pulse': 'mind',
}


def art(scene, seed, light=False):
    """Ambient artwork. Only the hero panels use it — everything that has to
    teach something uses a labelled diagram instead, and holds still."""
    return illustrate.render(ART.get(scene, 'cosmos'), seed, light=light)

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, 'site')
ASSETS = os.path.join(ROOT, 'assets')

TAGLINE = 'Big ideas, told as stories'


def head(title, desc, prefix, tone):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{prefix}assets/style.css">
<script src="{prefix}assets/motion.js" defer></script>
</head>
<body class="t-{tone}">
'''


def masthead(prefix, current):
    def mark(p):
        return ' aria-current="page"' if p == current else ''
    return f'''<div class="shell">
<header class="masthead">
  <a class="wordmark" href="{prefix}index.html">Context<i></i></a>
  <nav class="nav">
    <a href="{prefix}index.html"{mark('home')}>Home</a>
    <a href="{prefix}stories.html"{mark('stories')}>Stories</a>
  </nav>
</header>
</div>
'''


def foot(prefix):
    return f'''<div class="shell">
<footer class="site-foot">
  <span>Context &#183; a storytelling team. We take something large and put it next to something you already know.</span>
  <a href="{prefix}stories.html">All stories</a>
</footer>
</div>
</body>
</html>
'''


def card(s, prefix, delay=0):
    return f'''<li class="t-{s['card_tone']}" data-kicker="{s['kicker']}" data-reveal="{delay}">
  <a class="card" href="{prefix}stories/{s['slug']}.html">
    <span class="card-art">{diagram.thumb(s['thumb'])}</span>
    <span class="card-body">
      <span class="card-kicker">{s['kicker']}</span>
      <span class="card-title">{s['title']}</span>
      <span class="card-teaser">{s['teaser']}</span>
    </span>
  </a>
</li>'''


# ---------------------------------------------------------------- blocks

def block_scene(b, i, story):
    return f'''<li class="t-{b['tone']}" data-reveal="0">
  <div class="scene card-scene">{art(b['scene'], story['slug'] + b['scene'] + str(i))}
    <div class="scene-pad">
      <h2>{b['h']}</h2>
      <p>{b['p']}</p>
    </div>
  </div>
</li>'''


def block_diagram(b, i, story):
    return f'''<li data-reveal="0">
  <figure class="card-dia">
    <div class="dia-stage">{diagram.render(b['name'])}</div>
    <figcaption class="caption">{b['caption']}</figcaption>
  </figure>
</li>'''


def block_text(b, i, story):
    ps = ''.join(f'<p>{p}</p>' for p in b['p'])
    return f'''<li data-reveal="0">
  <div class="card-text">
    <h2>{b['h']}</h2>
    {ps}
  </div>
</li>'''


def block_turn(b, i, story):
    return f'''<li class="t-{b['tone']}" data-reveal="0">
  <div class="card-turn">
    <p>{b['text']}</p>
  </div>
</li>'''


def block_steps(b, i, story):
    items = ''.join(f'''<li class="step">
      <span class="step-n">{n + 1}</span>
      <div>
        <h3>{it['h']}</h3>
        <p>{it['p']}</p>
      </div>
    </li>''' for n, it in enumerate(b['items']))
    return f'''<li class="t-{b['tone']}" data-reveal="0">
  <div class="card-steps">
    <h2>{b['h']}</h2>
    <ol class="steps">{items}</ol>
  </div>
</li>'''


def block_figure(b, i, story):
    return f'''<li class="t-{b['tone']}" data-reveal="0">
  <figure class="card-figure">
    <div class="figure-stage">
{b['svg']}
    </div>
    <div class="controls">
{b['controls']}
    </div>
    <figcaption class="caption">{b['caption']}</figcaption>
  </figure>
</li>'''


BLOCKS = {
    'diagram': block_diagram,
    'scene': block_scene,
    'text': block_text,
    'turn': block_turn,
    'steps': block_steps,
    'figure': block_figure,
}


# ---------------------------------------------------------------- pages

PILLARS = [
    ('One idea at a time',
     'Every card carries a single thought. You are never asked to hold two new '
     'things at once.'),
    ('Show it before you explain it',
     'The picture comes first and the words caption it. Where words run out, you '
     'get the controls instead.'),
    ('Simple, not dumbed down',
     'Ordinary vocabulary and short sentences, with nothing quietly made untrue '
     'to get there.'),
]


def build_home():
    featured = [s for s in STORIES if s.get('featured')]
    kickers = []
    for s in STORIES:
        if s['kicker'] not in kickers:
            kickers.append(s['kicker'])

    pillars = ''.join(f'''<li class="pillar t-{t}" data-reveal="{i * 90}">
  <span class="pillar-mark"><svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="{3 + i}" fill="#fff"/></svg></span>
  <h3>{h}</h3>
  <p>{p}</p>
</li>''' for i, ((h, p), t) in enumerate(zip(PILLARS, ['nebula', 'deepsea', 'ember'])))

    chips = ''.join(f'<li><a class="filter" href="stories.html">{k}</a></li>' for k in kickers)

    return (
        head(f'Context &#8212; {TAGLINE}',
             'A storytelling team. We break the biggest ideas down into stories '
             'anyone can follow, with something to operate in every one.', '', 'nebula')
        + masthead('', 'home')
        + f'''<div class="shell">
<section class="hero">
  <div class="scene">{art("orbit", "home")}
    <div class="hero-pad">
      <p class="eyebrow" data-reveal="0">A storytelling team</p>
      <h1 data-reveal="80">Big ideas, small enough to hold.</h1>
      <p data-reveal="160">We take the things that are too large, too old or too strange to picture,
      and turn them into stories you can walk through. Then we hand you the controls.</p>
      <a class="cta" href="stories.html" data-reveal="240">Read the stories &#8594;</a>
    </div>
  </div>
</section>

<section class="band">
  <div class="band-head" data-reveal="0">
    <h2>Understanding is a story problem</h2>
    <p>Most explanations fail because they open with the mechanism. People remember what
    happened, in what order, and why it mattered &#8212; so that is how we build them.</p>
  </div>
  <ul class="pillars">{pillars}</ul>
</section>

<section class="band">
  <div class="band-head" data-reveal="0">
    <h2>Start here</h2>
    <p>A few we are proud of. There are more, and there will keep being more.</p>
  </div>
  <ul class="grid">
{chr(10).join(card(s, '', (i % 3) * 90) for i, s in enumerate(featured))}
  </ul>
</section>

<section class="band">
  <div class="band-head" data-reveal="0">
    <h2>What we cover</h2>
    <p>Anything worth being curious about. The list grows whenever something catches us.</p>
  </div>
  <ul class="filters" data-reveal="60">{chips}</ul>
</section>
</div>
'''
        + foot('')
    )


def build_stories():
    kickers = []
    for s in STORIES:
        if s['kicker'] not in kickers:
            kickers.append(s['kicker'])
    chips = ''.join(
        f'<li><button class="filter" data-filter="{k}" aria-pressed="false">{k}</button></li>'
        for k in kickers)

    return (
        head('Stories &#8212; Context',
             'Every story we have told so far, across space, time, matter, life and mind.',
             '', 'dusk')
        + masthead('', 'stories')
        + f'''<div class="shell">
<section class="band">
  <div class="band-head" data-reveal="0">
    <h2>Stories</h2>
    <p>Everything we have published. Filter by subject, or just scroll.</p>
  </div>
  <ul class="filters" data-reveal="60">
    <li><button class="filter" data-filter="" aria-pressed="true">Everything</button></li>
    {chips}
  </ul>
  <ul class="grid" id="storyGrid">
{chr(10).join(card(s, '', (i % 3) * 90) for i, s in enumerate(STORIES))}
  </ul>
</section>
</div>

<script>
// filter the grid in place; no routing, no reload
var grid = document.getElementById('storyGrid');
var buttons = document.querySelectorAll('.filter[data-filter]');
buttons.forEach(function (b) {{
  b.addEventListener('click', function () {{
    var want = b.getAttribute('data-filter');
    buttons.forEach(function (o) {{ o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); }});
    Array.prototype.forEach.call(grid.children, function (li) {{
      li.hidden = !(!want || li.getAttribute('data-kicker') === want);
    }});
  }});
}});
</script>
'''
        + foot('')
    )


def build_story(s, nxt):
    hero = s['hero']
    stack = '\n'.join(BLOCKS[b['type']](b, i, s) for i, b in enumerate(s['blocks']))
    scripts = '\n'.join(b['js'] for b in s['blocks'] if b['type'] == 'figure')
    zoom = s['zoomout']

    return (
        head(f"{s['title']} &#8212; Context", s['teaser'], '../', hero['tone'])
        + masthead('../', 'stories')
        + f'''<div class="shell">
<section class="story-hero t-{hero['tone']}">
  <div class="scene">{art(hero['scene'], s['slug'])}
    <div class="hero-pad">
      <p class="eyebrow" data-reveal="0">{s['kicker']}</p>
      <h1 data-reveal="80">{s['title']}</h1>
      <p class="standfirst" data-reveal="160">{hero['standfirst']}</p>
    </div>
  </div>
</section>

<ol class="stack">
{stack}
<li class="t-{zoom['tone']}" data-reveal="0">
  <div class="card-zoom">
    <h2>Zoom out</h2>
    <p>{zoom['text']}</p>
  </div>
</li>
</ol>

<nav class="pager">
  <a href="../stories.html">&#8592; All stories</a>
  <a href="{nxt['slug']}.html">{nxt['title']} &#8594;</a>
</nav>
</div>

<script>
{scripts}
</script>
'''
        + foot('../')
    )


def main():
    if os.path.isdir(SITE):
        shutil.rmtree(SITE)
    os.makedirs(os.path.join(SITE, 'stories'))

    shutil.copytree(ASSETS, os.path.join(SITE, 'assets'))
    open(os.path.join(SITE, '.nojekyll'), 'w').close()

    with open(os.path.join(SITE, 'index.html'), 'w') as fh:
        fh.write(build_home())
    with open(os.path.join(SITE, 'stories.html'), 'w') as fh:
        fh.write(build_stories())

    for i, s in enumerate(STORIES):
        nxt = STORIES[(i + 1) % len(STORIES)]
        with open(os.path.join(SITE, 'stories', f"{s['slug']}.html"), 'w') as fh:
            fh.write(build_story(s, nxt))

    scenes = sum(1 for s in STORIES for b in s['blocks'] if b['type'] == 'scene') + len(STORIES)
    print(f'built home + stories index + {len(STORIES)} stories '
          f'({scenes} animated scenes) into {SITE}')


if __name__ == '__main__':
    main()
