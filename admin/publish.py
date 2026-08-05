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
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, 'content')
STORIES = os.path.join(CONTENT, 'stories')
VISIBILITY = os.path.join(CONTENT, 'visibility.json')

# beats.py lives at the repository root and is the shared definition of the six
# beats. It reads nothing and holds no state, so unlike build.py it is safe to
# import at module scope — there is no content/ to go stale underneath us.
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import beats  # noqa: E402

TONES = beats.TONES

# A placeholder framing, overwritten by corpus.py when the story takes its place
# in the corpus. It has to be *something* for the story dict to be complete, but
# nothing should read it: a variant is only unique with respect to every other
# story, and this file can only see one. Choosing it here is what once gave a
# generated story the same banner as a hand-written one.
GENERATED_VAR = 2


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
    hand-written stories use.

    An adapter, and only an adapter. The six-beat order and the envelopes live in
    beats.py, shared with library.expand(), so a generated story and a
    hand-written one cannot end up with different grammars. What belongs here is
    the writer's own vocabulary: `wrong_head`/`wrong_body` field pairs, diagram
    data arriving as a JSON string, findings as dicts rather than tuples, and the
    tolerance for older drafts that the queue still has to render.
    """
    tone = s.get('tone') or 'dusk'
    slug = s.get('slug') or slugify(s.get('title'))

    blocks = beats.stack(
        wrong=(s['wrong_head'], _paras(s['wrong_body'])),
        crack=(s['crack_head'], _paras(s['crack_body'])),
        cost=(s['cost_head'], _paras(s['cost_body'])),
        turn=s['turn'],
        teaser=s['teaser'],
        scene=s['scene'],
        scene_var=GENERATED_VAR + beats.SCENE_VAR_OFFSET,
        diagram_one=(_spec(s['diagram_one']), s['diagram_one'].get('caption', '')),
        diagram_two=(_spec(s['diagram_two']), s['diagram_two'].get('caption', '')),
        turn_tone=beats.counter_tone(tone),
    )

    story = beats.story_envelope(
        slug=slug, kicker=s.get('domain', 'General'), lens=s['lens'], tone=tone,
        title=s['title'], teaser=s['teaser'], takeaway=s['takeaway'],
        scene=s['scene'], hero_var=GENERATED_VAR, standfirst=s['standfirst'],
        blocks=blocks, zoomout=s['zoomout'])

    findings = s.get('_findings') or {}
    paper = beats.paper_envelope(
        slug=slug,
        title=beats.research_title(s['title']),
        subtitle=s['paper_subtitle'],
        date=s.get('_date', ''),
        abstract=s['paper_abstract'],
        sections=[{'h': sec['h'], 'p': _paras(sec['p'])}
                  for sec in s.get('paper_sections') or []],
        findings=[(f['claim'], f['confidence'], f['basis'])
                  for f in findings.get('findings', [])],
        contested=[(c['question'], c['dispute'])
                   for c in findings.get('contested', [])],
        unknowns=list(findings.get('unknowns', [])),
        method=s['method'],
        reading=[(r['source'], r['why']) for r in s.get('reading', [])])

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

class Repo:
    """Everything the backoffice does to the repository, behind one seam.

    `run` is the subprocess runner, and it is a constructor argument rather than
    a hard call to subprocess so that a test can drive a whole publish — build,
    add, commit, push, and each way they fail — without a git remote, without a
    network, and without committing anything. This module was previously
    untestable for exactly that reason: the only way to find out what happened on
    a failed push was to have one.
    """

    def __init__(self, root=ROOT, run=subprocess.run, python=None):
        self.root = root
        self.run = run
        # sys.executable, not 'python3': on Windows there is usually no python3
        # on PATH, and the name is an App Execution Alias that opens the
        # Microsoft Store instead of running anything. It also guarantees the
        # build uses the same interpreter the server is running under.
        self.python = python or sys.executable

    def git(self, *args, check=False):
        return self.run(['git', '-C', self.root, *args], capture_output=True,
                        text=True, timeout=120, check=check)

    def build(self):
        """Rebuild so a publish fails here, in front of the editor, rather than
        in CI after the push."""
        return self.run([self.python, 'build.py'], cwd=self.root,
                        capture_output=True, text=True, timeout=600)

    def branch(self):
        head = self.git('rev-parse', '--abbrev-ref', 'HEAD')
        return (head.stdout or 'main').strip() or 'main'

    def commit_and_push(self, message, branch=None):
        """Returns (ok, log). Never raises — the caller shows the log to a human,
        and a half-finished publish that reports itself is worth more than a
        stack trace in a terminal nobody is watching."""
        lines = []
        build = self.build()
        lines.append((build.stdout or '') + (build.stderr or ''))
        if build.returncode != 0:
            return False, '\n'.join(lines) + '\nBuild failed. Nothing was committed.'

        self.git('add', '-A', 'content', 'site')
        status = self.git('status', '--porcelain', 'content', 'site')
        if not status.stdout.strip():
            return True, '\n'.join(lines) + '\nNothing to commit — content already current.'

        commit = self.git('commit', '-m', message)
        lines.append(commit.stdout + commit.stderr)
        if commit.returncode != 0:
            return False, '\n'.join(lines)

        branch = branch or self.branch()
        push = self.git('push', 'origin', branch)
        lines.append(push.stdout + push.stderr)
        if push.returncode != 0:
            lines.append('Push failed. The commit is local — push it by hand, or fix '
                         'the GitHub credentials and use Retry push.')
            return False, '\n'.join(lines)
        return True, '\n'.join(lines) + f'\nPushed to {branch}. Pages rebuilds on its own.'


# The one the app uses. Tests build their own with a stub runner.
repo = Repo()


def build_site():
    return repo.build()


def commit_and_push(message, branch=None):
    return repo.commit_and_push(message, branch)
