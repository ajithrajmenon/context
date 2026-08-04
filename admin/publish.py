# -*- coding: utf-8 -*-
"""Approved draft -> content/*.json -> git -> Pages.

The site generator never reads the database. It reads `content/`, which is
committed to the repository, so every published change is a commit somebody can
read, revert, or diff. The database is the workshop; git is the record.

Two files matter:

    content/stories/<slug>.json   a generated story, in the shape build.py wants
    content/visibility.json       {slug: bool} — hides any story from the site,
                                  including the fifty hand-written ones

Visibility is separate from publication on purpose. Un-publishing by deleting a
file loses the work; setting a slug false in visibility.json takes it off the
site and keeps everything.
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, 'content')
STORIES = os.path.join(CONTENT, 'stories')
VISIBILITY = os.path.join(CONTENT, 'visibility.json')

TONES = ['dusk', 'ember', 'deepsea', 'nebula', 'forest', 'solar', 'rose', 'void']


def slugify(text):
    s = re.sub(r'[^a-z0-9]+', '-', (text or '').lower()).strip('-')
    return s or 'untitled'


def _spec(d):
    """Writer diagram -> diagram.build() spec. `data` arrives as a JSON string
    because the schema keeps the shape flat; the kind decides what is in it."""
    spec = {'kind': d['kind'], 'title': d['title'], 'sub': d.get('sub', '')}
    try:
        body = json.loads(d.get('data') or '{}')
    except (ValueError, TypeError):
        body = {}
    if isinstance(body, dict):
        spec.update(body)
    # The grammar takes tuples; JSON gives lists. Everything downstream indexes
    # positionally, so lists are fine — except `axis`, which is unpacked.
    if 'axis' in spec and isinstance(spec['axis'], list):
        spec['axis'] = tuple(spec['axis'][:2])
    return spec


def _paras(value):
    """A beat's body as a list of paragraphs.

    The writer returns a list — two or three short paragraphs, which is the
    rhythm the hand-written stories have. Older drafts hold one long string,
    and a string that has been split on blank lines is closer to the intent
    than a wall of text, so accept both rather than breaking the queue.
    """
    if isinstance(value, (list, tuple)):
        return [p.strip() for p in value if p and p.strip()]
    return [p.strip() for p in re.split(r'\n\s*\n', value or '') if p.strip()]


def expand(s):
    """One writer output -> (story dict, paper dict), in the same shape the
    hand-written stories use. This is library.expand() for generated content."""
    tone = s.get('tone') or 'dusk'
    alt = TONES[(TONES.index(tone) + 3) % len(TONES)] if tone in TONES else 'nebula'
    slug = s.get('slug') or slugify(s.get('title'))

    blocks = [
        {'type': 'text', 'h': s['wrong_head'], 'p': _paras(s['wrong_body'])},
        {'type': 'scene', 'tone': 'void', 'scene': s['scene'], 'var': 9,
         'h': s['teaser']},
        {'type': 'diagram', 'spec': _spec(s['diagram_one']),
         'caption': s['diagram_one'].get('caption', '')},
        {'type': 'text', 'h': s['crack_head'], 'p': _paras(s['crack_body'])},
        {'type': 'turn', 'tone': alt, 'text': s['turn']},
        {'type': 'diagram', 'spec': _spec(s['diagram_two']),
         'caption': s['diagram_two'].get('caption', '')},
        {'type': 'text', 'h': s['cost_head'], 'p': _paras(s['cost_body'])},
    ]

    story = {
        'slug': slug, 'kicker': s.get('domain', 'General'), 'lens': s['lens'],
        'card_tone': tone, 'thumb': None, 'featured': False,
        'title': s['title'], 'teaser': s['teaser'], 'takeaway': s['takeaway'],
        'hero': {'tone': tone, 'scene': s['scene'], 'var': 2,
                 'standfirst': s['standfirst']},
        'blocks': blocks,
        'zoomout': {'tone': tone, 'text': s['zoomout']},
    }

    findings = s.get('_findings') or {}
    paper = {
        'slug': slug,
        'title': s['title'].rstrip('?') + ': the research',
        'subtitle': s['paper_subtitle'],
        'date': s.get('_date', ''),
        'minutes': max(4, 3 + len(findings.get('findings', []))),
        'abstract': s['paper_abstract'],
        # A paper whose only section restates its own abstract is not a paper.
        # The writer supplies real sections; the fallback is for older drafts.
        'sections': ([{'h': sec['h'], 'p': _paras(sec['p'])}
                      for sec in s.get('paper_sections') or []]
                     or [{'h': 'What we looked at', 'p': [s['paper_abstract']]}]),
        'findings': [(f['claim'], f['confidence'], f['basis'])
                     for f in findings.get('findings', [])],
        'contested': [(c['question'], c['dispute'])
                      for c in findings.get('contested', [])],
        'unknowns': list(findings.get('unknowns', [])),
        'method': s['method'],
        'reading': [(r['source'], r['why']) for r in s.get('reading', [])],
    }
    return story, paper


# ---------------------------------------------------------------- files

def read_visibility():
    try:
        with open(VISIBILITY, encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def write_visibility(vis):
    os.makedirs(CONTENT, exist_ok=True)
    with open(VISIBILITY, 'w', encoding='utf-8') as fh:
        json.dump(vis, fh, indent=1, sort_keys=True)
        fh.write('\n')


def set_visible(slug, visible):
    vis = read_visibility()
    if visible:
        vis.pop(slug, None)          # absent means visible; keeps the file small
    else:
        vis[slug] = False
    write_visibility(vis)


def write_story(story, paper):
    os.makedirs(STORIES, exist_ok=True)
    path = os.path.join(STORIES, story['slug'] + '.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump({'story': story, 'paper': paper}, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    return path


def remove_story(slug):
    path = os.path.join(STORIES, slug + '.json')
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


# ---------------------------------------------------------------- git

def _git(*args, check=True):
    return subprocess.run(['git', '-C', ROOT, *args], capture_output=True,
                          text=True, timeout=120, check=check)


def build_site():
    """Rebuild so a publish fails here, in front of the editor, rather than in
    CI after the push."""
    return subprocess.run(['python3', 'build.py'], cwd=ROOT, capture_output=True,
                          text=True, timeout=600)


def commit_and_push(message, branch=None):
    """Returns (ok, log). Never raises — the caller shows the log to a human."""
    lines = []
    build = build_site()
    lines.append((build.stdout or '') + (build.stderr or ''))
    if build.returncode != 0:
        return False, '\n'.join(lines) + '\nBuild failed. Nothing was committed.'

    _git('add', '-A', 'content', 'site', check=False)
    status = _git('status', '--porcelain', 'content', 'site', check=False)
    if not status.stdout.strip():
        return True, '\n'.join(lines) + '\nNothing to commit — content already current.'

    commit = _git('commit', '-m', message, check=False)
    lines.append(commit.stdout + commit.stderr)
    if commit.returncode != 0:
        return False, '\n'.join(lines)

    if branch is None:
        head = _git('rev-parse', '--abbrev-ref', 'HEAD', check=False)
        branch = (head.stdout or 'main').strip() or 'main'

    push = _git('push', 'origin', branch, check=False)
    lines.append(push.stdout + push.stderr)
    if push.returncode != 0:
        lines.append('Push failed. The commit is local — push it by hand, or fix '
                     'the GitHub credentials and use Retry push.')
        return False, '\n'.join(lines)
    return True, '\n'.join(lines) + f'\nPushed to {branch}. Pages rebuilds on its own.'
