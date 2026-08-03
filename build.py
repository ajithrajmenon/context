#!/usr/bin/env python3
"""Builds Context into site/.

No dependencies and no framework — read topics_data.py, write HTML.
Adding a topic means appending one dict to TOPICS and running this again.
"""
import os
import shutil

from topics_data import TOPICS

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, 'site')
ASSETS = os.path.join(ROOT, 'assets')

TAGLINE = 'Everyday things, properly explained'


def head(title, desc, css, hue):
    return f'''<!DOCTYPE html>
<html lang="en" class="hue-{hue}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{css}">
</head>
<body>
<div class="shell">
'''


def masthead(home, note):
    return f'''<header class="masthead">
  <a class="wordmark" href="{home}">Context<span>.</span></a>
  <p class="masthead-note">{note}</p>
</header>
'''


FOOT = '''<footer class="site-foot">
  <p>Context &#183; questions from ordinary life, answered without the hand-waving.</p>
</footer>
</div>
</body>
</html>
'''


def build_index():
    cards = []
    for t in TOPICS:
        cards.append(f'''<li class="hue-{t['hue']}"><a class="card" href="topics/{t['slug']}.html">
  <span class="card-art">{t['icon']}</span>
  <span class="card-body">
    <span class="card-kicker">{t['kicker']}</span>
    <span class="card-title">{t['title']}</span>
    <span class="card-teaser">{t['teaser']}</span>
  </span>
</a></li>''')

    return (
        head(f'Context &#8212; {TAGLINE}',
             'Clear answers to the everyday questions people actually ask, '
             'with something to play with in each one.',
             'assets/style.css', 'blue')
        + masthead('index.html', f'{len(TOPICS)} questions')
        + f'''<div class="hero">
  <h1>Everyday things, <em>properly</em> explained.</h1>
  <p>Why the fridge ruins bread. Why your phone dies in the cold. Why the shower curtain
  always comes for you. Short answers you can trust, and something to play with in each one.</p>
</div>

<ol class="grid">
{chr(10).join(cards)}
</ol>
'''
        + FOOT
    )


def build_topic(t, prev_t, next_t):
    secs = []
    for s in t['sections']:
        body = ''
        if 'p' in s:
            body += ''.join(f'<p>{p}</p>' for p in s['p'])
        if 'tips' in s:
            body += '<ul class="tips">' + ''.join(f'<li>{x}</li>' for x in s['tips']) + '</ul>'
        secs.append(f'''<section class="section">
  <h2>{s['h']}</h2>
  {body}
</section>''')

    pager = [
        '<a href="../index.html">&#8592; All questions</a>',
        f'<a href="{next_t["slug"]}.html">{next_t["title"]} &#8594;</a>',
    ]

    n = TOPICS.index(t) + 1
    return (
        head(f'{t["title"]} &#8212; Context', t['answer'], '../assets/style.css', t['hue'])
        + masthead('../index.html', f'{n} of {len(TOPICS)}')
        + f'''<article>
  <div class="topic-head">
    <p class="eyebrow">{t['kicker']}</p>
    <h1>{t['title']}</h1>
  </div>

  <div class="answer">
    <b>Short answer</b>
    <p>{t['answer']}</p>
  </div>

  <figure class="figure">
    <div class="figure-stage">
{t['svg']}
    </div>
    <div class="controls">
{t['controls']}
    </div>
    <figcaption class="caption">{t['caption']}</figcaption>
  </figure>

{chr(10).join(secs)}
</article>

<nav class="pager">
{chr(10).join(pager)}
</nav>

<script>
{t['js']}
</script>
'''
        + FOOT
    )


def main():
    if os.path.isdir(SITE):
        shutil.rmtree(SITE)
    os.makedirs(os.path.join(SITE, 'topics'))

    shutil.copytree(ASSETS, os.path.join(SITE, 'assets'))
    # tells GitHub Pages to serve the directory verbatim
    open(os.path.join(SITE, '.nojekyll'), 'w').close()

    with open(os.path.join(SITE, 'index.html'), 'w') as f:
        f.write(build_index())

    for i, t in enumerate(TOPICS):
        # the last topic points back at the first, so "next" always goes forward
        prev_t = TOPICS[i - 1]
        next_t = TOPICS[(i + 1) % len(TOPICS)]
        with open(os.path.join(SITE, 'topics', f'{t["slug"]}.html'), 'w') as f:
            f.write(build_topic(t, prev_t, next_t))

    print(f'built {len(TOPICS)} topics + index into {SITE}')


if __name__ == '__main__':
    main()
