#!/usr/bin/env python3
"""Builds Context into site/.

No dependencies and no framework — read stories_data.py, write HTML.

    site/index.html          the homepage
    site/stories.html        every story, filterable
    site/stories/<slug>.html one story

Adding a story means appending one dict to STORIES and running this again.
Categories are derived from the stories themselves, so a new subject area
needs no other change.
"""
import os
import shutil

from stories_data import STORIES

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
    def mark(page):
        return ' aria-current="page"' if page == current else ''
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
    return f'''<li class="t-{s['tone']}" data-kicker="{s['kicker']}" data-reveal="{delay}">
  <a class="card" href="{prefix}stories/{s['slug']}.html">
    <span class="card-art" data-scene="{s['scene']}" data-seed="{s['slug']}"></span>
    <span class="card-body">
      <span class="card-kicker">{s['kicker']}</span>
      <span class="card-title">{s['title']}</span>
      <span class="card-teaser">{s['teaser']}</span>
    </span>
  </a>
</li>'''


PILLARS = [
    ('Start where curiosity does',
     'Not with a syllabus. With the question you would actually ask out loud, '
     'phrased the way you would actually ask it.'),
    ('Show the thing, not a diagram of it',
     'Every story hands you the controls at the point where words stop working. '
     'You move it yourself and watch what happens.'),
    ('Keep the numbers honest',
     'The wonder has to survive being checked. Where a figure is contested or a '
     'famous version is wrong, we say so.'),
]


def build_home():
    featured = [s for s in STORIES if s.get('featured')][:3]
    kickers = []
    for s in STORIES:
        if s['kicker'] not in kickers:
            kickers.append(s['kicker'])

    pillars = ''.join(f'''<li class="pillar" data-reveal="{i * 90}">
  <span class="pillar-mark"><svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="{3 + i}" fill="#fff"/></svg></span>
  <h3>{h}</h3>
  <p>{p}</p>
</li>''' for i, (h, p) in enumerate(PILLARS))

    chips = ''.join(
        f'<li><a class="filter" href="stories.html">{k}</a></li>' for k in kickers)

    return (
        head(f'Context &#8212; {TAGLINE}',
             'A storytelling team. We break big ideas down into stories anyone can '
             'follow, with something to operate in every one.', '', 'nebula')
        + masthead('', 'home')
        + f'''<div class="shell">
<section class="hero">
  <div class="stage" data-scene="orbit" data-seed="home" data-focus="0.74,0.5">
    <div class="stage-pad">
      <p class="eyebrow" data-reveal="0">A storytelling team</p>
      <h1 data-reveal="80">Big ideas, small enough to hold.</h1>
      <p data-reveal="160">We take the things that are too large, too old or too strange to picture,
      and put them next to something you already know. Then we hand you the controls.</p>
      <a class="cta" href="stories.html" data-reveal="240">Read the stories &#8594;</a>
    </div>
  </div>
</section>

<section class="band">
  <div class="band-head" data-reveal="0">
    <h2>Understanding is a story problem</h2>
    <p>Most explanations fail because they start with the mechanism. People remember what
    happened to somebody, in what order, and why it mattered &#8212; so that is how we build them.</p>
  </div>
  <ul class="pillars">{pillars}</ul>
</section>

<section class="band">
  <div class="band-head" data-reveal="0">
    <h2>Start here</h2>
    <p>A few we are proud of. There are more, and there will keep being more.</p>
  </div>
  <ul class="grid">
{chr(10).join(card(s, '', i * 90) for i, s in enumerate(featured))}
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
        head(f'Stories &#8212; Context',
             'Every story we have told so far, across space, bodies, time, Earth and '
             'the numbers that break intuition.', '', 'dusk')
        + masthead('', 'stories')
        + f'''<div class="shell">
<section class="band">
  <div class="band-head" data-reveal="0">
    <h2>Stories</h2>
    <p>Everything we have published, newest thinking first. Filter by subject, or just scroll.</p>
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
    buttons.forEach(function (o) {{
      o.setAttribute('aria-pressed', o === b ? 'true' : 'false');
    }});
    Array.prototype.forEach.call(grid.children, function (li) {{
      var show = !want || li.getAttribute('data-kicker') === want;
      li.hidden = !show;
    }});
  }});
}});
</script>
'''
        + foot('')
    )


def build_story(s, nxt):
    def beats(items):
        return ''.join(f'''<section class="beat" data-reveal="0">
  <h2>{b['h']}</h2>
  {''.join(f'<p>{p}</p>' for p in b['p'])}
</section>''' for b in items)

    f = s['figure']
    return (
        head(f"{s['title']} &#8212; Context", s['teaser'], '../', s['tone'])
        + masthead('../', 'stories')
        + f'''<div class="shell">
<section class="story-hero">
  <div class="stage" data-scene="{s['scene']}" data-seed="{s['slug']}">
    <div class="stage-pad">
      <p class="eyebrow" data-reveal="0">{s['kicker']}</p>
      <h1 data-reveal="80">{s['title']}</h1>
      <p class="standfirst" data-reveal="160">{s['standfirst']}</p>
    </div>
  </div>
</section>

<article class="narrow">
{beats(s['beats'])}

  <p class="turn" data-reveal="0">{s['turn']}</p>

{beats(s['after'])}
</article>

<div class="wide">
  <figure class="figure" data-reveal="0">
    <div class="figure-stage">
{f['svg']}
    </div>
    <div class="controls">
{f['controls']}
    </div>
    <figcaption class="caption">{f['caption']}</figcaption>
  </figure>
</div>

<div class="narrow">
  <section class="zoomout" data-reveal="0">
    <h2>Zoom out</h2>
    <p>{s['zoomout']}</p>
  </section>

  <nav class="pager">
    <a href="../stories.html">&#8592; All stories</a>
    <a href="{nxt['slug']}.html">{nxt['title']} &#8594;</a>
  </nav>
</div>
</div>

<script>
{f['js']}
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

    print(f'built home + stories index + {len(STORIES)} stories into {SITE}')


if __name__ == '__main__':
    main()
