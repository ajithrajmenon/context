# -*- coding: utf-8 -*-
"""Assembles the published corpus: which stories exist, and which papers go with
them.

The site is built from four sources, and this is the one place that knows how
they combine:

    stories_data.FLAGSHIP   four stories built long, by hand
    library.BRIEFS          forty-six briefs, expanded to the same six beats
    content/stories/*.json  written by the research team, approved by a human
    content/visibility.json takes any story off the site without deleting it

This used to happen at import time, as a side effect of `import stories_data` —
the module appended to its own list, mutated it, read the filesystem, and
papers_data imported it back to filter itself. Two consequences. The build could
not be exercised on anything but the real content, because there was no way to
hand it different data. And the backoffice had to `importlib.reload()` the module
to see a story it had just approved, which is a way of saying that reading data
was entangled with executing it.

So: reading is a function call, and it returns a value.

    corpus.load()                     the live site, read fresh
    corpus.assemble(stories=..., ...) any corpus you like, for a test

Both return a `Corpus`. Nothing here is cached: the caller decides when to look,
and the answer is right at the moment it is asked.
"""
import glob
import json
import os

import beats
import library
import papers_data
import stories_data

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, 'content')


class Corpus:
    """Everything published, and the links between the two halves of it."""

    def __init__(self, stories, papers):
        self.stories = stories
        self.papers = papers
        self.by_slug = {p['slug']: p for p in papers}
        self._stories_by_slug = {s['slug']: s for s in stories}

    def __len__(self):
        return len(self.stories)

    def paper_for(self, slug):
        """The paper behind a story, or None. A story without one is legitimate —
        the card simply is not drawn."""
        return self.by_slug.get(slug)

    def story_for(self, slug):
        """The story a paper belongs to, or None."""
        return self._stories_by_slug.get(slug)

    def next_after(self, i):
        """The story the pager points at. Wraps, so the last one leads back to
        the first and no story is a dead end."""
        return self.stories[(i + 1) % len(self.stories)]

    def scenes(self):
        """Animated scenes on the site: one banner per story, plus the full-bleed
        panels inside them."""
        return sum(1 for s in self.stories
                   for b in s['blocks'] if b['type'] == 'scene') + len(self.stories)


def expand_library(briefs=None):
    """The briefs, expanded into full stories and papers.

    Kept separate from `assemble` because it is the expensive half — fifty briefs
    through the six-beat grammar — and because a test that only cares about
    visibility filtering should not have to pay for it.
    """
    briefs = library.BRIEFS if briefs is None else briefs
    stories, papers = [], []
    for i, brief in enumerate(briefs):
        story, paper = library.expand(brief, i)
        stories.append(story)
        papers.append(paper)
    return stories, papers


def _assign_lens(stories, lenses):
    """Every story sits under exactly one of the four lenses.

    The flagship four are written by hand and do not carry the field, so it is
    filled in from the same map the library uses — one classification, in one
    place. setdefault, not assignment: a generated story arrives with its own
    lens already chosen by the Planner and must keep it.
    """
    for s in stories:
        if 'lens' not in s:
            s['lens'] = lenses[s['slug']]


def _assign_variants(stories):
    """Give every story its own framing of its scene.

    Twelve stories share the `mind` scene and nine share `cell`, so a variant
    picked by hand in a brief was never going to be unique. Assigning by position
    within the scene means every story gets its own palette rotation and its own
    framing, and no two banners on the site are the same picture.

    Generated stories are numbered by the same counter, continuing after the
    library rather than restarting. They used to carry a fixed variant chosen in
    publish.py, on the reasoning that one generated story could not collide with
    itself — which was true and beside the point, because it collided with the
    library instead: a generated `mind` story rendered the identical banner to the
    second hand-written one. A variant is only unique with respect to the whole
    corpus, so it can only be assigned where the whole corpus is known, which is
    here.
    """
    used = {}
    for s in stories:
        scene = s['hero']['scene']
        used[scene] = used.get(scene, 0) + 1
        s['hero']['var'] = used[scene]
        for b in s['blocks']:
            if b['type'] == 'scene':
                b['var'] = used[scene] + beats.SCENE_VAR_OFFSET


def read_generated(content=None):
    """Stories written by the research team and approved by a human.

    They carry the same shape as everything else, so the build cannot tell the
    difference and does not need to. Sorted by filename for a stable order, and a
    file that will not parse is skipped rather than fatal — one bad record should
    not take the site down.
    """
    content = CONTENT if content is None else content
    stories, papers = [], []
    for path in sorted(glob.glob(os.path.join(content, 'stories', '*.json'))):
        try:
            with open(path, encoding='utf-8') as fh:
                rec = json.load(fh)
        except (OSError, ValueError):
            continue
        if rec.get('story'):
            stories.append(rec['story'])
        if rec.get('paper'):
            papers.append(rec['paper'])
    return stories, papers


def read_visibility(content=None):
    """{slug: bool}. Absent means visible."""
    content = CONTENT if content is None else content
    try:
        with open(os.path.join(content, 'visibility.json'), encoding='utf-8') as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return {}


def assemble(flagship=None, flagship_papers=None, library_stories=None,
             library_papers=None, generated=None, generated_papers=None,
             visibility=None, lenses=None):
    """Combine the sources into one corpus.

    Order is the reading order of the site and is deliberate: the four long ones
    first, then the library, then anything generated. Everything defaults to the
    real data, so `assemble()` and `load()` agree, and any one source can be
    replaced on its own.
    """
    flagship = stories_data.FLAGSHIP if flagship is None else flagship
    flagship_papers = (papers_data.FLAGSHIP if flagship_papers is None
                       else flagship_papers)
    lenses = library.LENS if lenses is None else lenses
    generated = [] if generated is None else generated
    generated_papers = [] if generated_papers is None else generated_papers
    visibility = {} if visibility is None else visibility
    if library_stories is None:
        library_stories, library_papers = expand_library()
    library_papers = [] if library_papers is None else library_papers

    _assign_lens(library_stories + flagship, lenses)
    # Library first, then generated, so that adding a generated story never
    # renumbers a published one. The flagship four are framed by hand and are
    # left alone.
    _assign_variants(library_stories + generated)

    stories = flagship + library_stories + generated
    papers = flagship_papers + library_papers + generated_papers

    hidden = {slug for slug, shown in visibility.items() if not shown}
    stories = [s for s in stories if s['slug'] not in hidden]

    # A hidden story's paper goes with it — a live paper linking to a 404 is
    # worse than no paper at all.
    live = {s['slug'] for s in stories}
    papers = [p for p in papers if p['slug'] in live]

    return Corpus(stories, papers)


def load(content=None):
    """The live site, read fresh from disk."""
    generated, generated_papers = read_generated(content)
    return assemble(generated=generated, generated_papers=generated_papers,
                    visibility=read_visibility(content))


def preview(story, paper=None, content=None):
    """The live corpus with an unapproved draft added, for the approval screen.

    A banner variant is a function of the whole corpus, so a draft rendered on its
    own would be framed differently from the page that eventually publishes — and
    the one promise the approval screen makes is that what you see is what goes
    out. Assembling the real corpus around the draft is what keeps that true.

    Any already-published copy of the same slug is dropped, so re-previewing an
    approved draft shows the draft rather than two of it.
    """
    generated, generated_papers = read_generated(content)
    slug = story['slug']
    generated = [s for s in generated if s['slug'] != slug] + [story]
    generated_papers = [p for p in generated_papers if p['slug'] != slug]
    if paper:
        generated_papers.append(paper)
    return assemble(generated=generated, generated_papers=generated_papers,
                    visibility=read_visibility(content))
