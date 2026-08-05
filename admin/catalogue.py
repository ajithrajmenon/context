# -*- coding: utf-8 -*-
"""What is actually on the site, and where each story came from.

The database is the workshop and git is the record, so neither of them is the
answer to "what is published". The answer is what build.py would read right now:
the data modules plus content/. This module is the one place that asks, so the
dashboard and the stories table cannot disagree.

    live()        the stories build.py would publish this minute
    generated()  slugs that came from the research team
    counts()      the four dashboard numbers
    rows()        one entry per story, for the visibility table
"""
import os

from . import publish
from .config import ROOT


def live():
    """The live story list, read fresh.

    Read on every call, not cached: approving a draft changes the answer, and a
    server that reported the catalogue it saw at boot would be wrong for the rest
    of the day. This used to need `importlib.reload()` because assembling the
    corpus was a side effect of importing it; corpus.load() is a function, so it
    can simply be called again.
    """
    import sys
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    import corpus
    return corpus.load().stories


def generated():
    """Slugs written by the research team, from content/stories/."""
    if not os.path.isdir(publish.STORIES):
        return set()
    return {f[:-5] for f in os.listdir(publish.STORIES) if f.endswith('.json')}


def counts(queued=0):
    vis = publish.read_visibility()
    return {
        'live': len(live()),
        'queued': queued,
        'generated': len(generated()),
        'hidden': sum(1 for shown in vis.values() if not shown),
    }


def rows():
    """Every story the backoffice can act on, visible or not.

    A hidden story is absent from the live list by design, so the union of the
    live list, the visibility file and content/ is what has to be walked — read
    only the live list and the hidden ones become unreachable, with no way left
    in the interface to bring them back.
    """
    vis = publish.read_visibility()
    made = generated()
    live_by_slug = {s['slug']: s for s in live()}

    out = []
    for slug in sorted(set(live_by_slug) | set(vis) | made):
        s = live_by_slug.get(slug)
        out.append({
            'slug': slug,
            'title': s['title'] if s else slug,
            'lens': s.get('lens', '\u2014') if s else '\u2014',
            'origin': 'generated' if slug in made else 'hand-written',
            'visible': vis.get(slug, True),
        })
    return out
