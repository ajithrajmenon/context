# -*- coding: utf-8 -*-
"""What can be done to a draft: preview it, edit it, approve it, reject it.

The decisions live here rather than in the routes, because they are the part
worth testing and the part that must not change quietly. A route should read the
request and render the answer; whether approving a draft writes before it commits
is not a routing question.

    pages()     the draft as real HTML — story page and paper page
    revise()    apply a plain-English instruction
    approve()   write it into content/, rebuild, commit, push
    reject()    take it out of the queue without losing it
"""
import json
import sys

from . import publish, research, store
from .config import ROOT


def _site():
    """The site's own renderer, imported lazily.

    On demand rather than at module scope so that the backoffice still starts if a
    data module is briefly broken — which is exactly when you want to be able to
    log in and look.
    """
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    import build, corpus, illustrate
    return build, corpus, illustrate


def story_of(draft_id):
    d = store.get_draft(draft_id)
    return json.loads(d['story_json']) if d else None


# The point of the approval screen is to answer one question: is this good enough
# to publish? A bulleted outline of the beats cannot answer it. Banners,
# illustrations, diagrams and typography are most of what a reader meets, and they
# are exactly what an outline leaves out.
#
# So the preview is the real page, rendered by build.py — the same function that
# writes site/stories/*.html. Not a mock-up, and not a second renderer that can
# drift away from it: if the preview looks right, the published page looks right,
# because they are the same code.

def pages(draft_id):
    """The draft as (story page, paper page) — real HTML, not an outline."""
    s = story_of(draft_id)
    if s is None:
        return None, None
    story, paper = publish.expand(s)
    build, corpus, _ = _site()
    # The real corpus with this draft added, rather than a corpus of one. Two
    # reasons. The renderer needs somewhere to look up the paper behind the story
    # to draw the "research behind this" card, and an unpublished draft is in no
    # index yet. And the banner's framing depends on how many other stories share
    # its scene, so a draft rendered alone would be framed differently from the
    # page that eventually publishes — which would make the preview a lie about
    # the one thing it exists to show.
    around = corpus.preview(story, paper)
    # Its own "next story" — the pager has nowhere else to point yet.
    return (build.build_story(story, story, around),
            build.build_paper(paper, around))


def preview_css():
    """The site stylesheet plus the classes build.py appends when it writes the
    site. Without them every animation runs at its default duration and the page
    moves wrong, which would make the preview lie."""
    import os
    _, _, illustrate = _site()
    with open(os.path.join(ROOT, 'assets', 'style.css'), encoding='utf-8') as fh:
        return fh.read() + '\n\n' + illustrate.anim_css() + '\n'


def revise(draft_id, instruction):
    """Apply a plain-English instruction. Returns the list of changes.

    The graded findings and the date are carried across by hand: they are not
    the writer's output, the Editor is not asked to reproduce them, and the paper
    cannot be rendered without them. Losing them here is how a revised draft ends
    up with an empty findings table.
    """
    before = story_of(draft_id)
    if before is None:
        return None
    after, changes = research.revise(before, instruction)
    after['_findings'] = before.get('_findings', {})
    after['_date'] = before.get('_date', '')
    store.record_edit(draft_id, instruction, before, after)
    store.update_draft(draft_id, story_json=json.dumps(after),
                       title=after.get('title', ''))
    store.log('draft.revise', f'{draft_id}: {instruction[:120]}')
    return changes


def approve(draft_id):
    """Publish. Returns (ok, log, story) or (False, message, None).

    Written to content/ *before* the push is attempted, and marked `approved`
    rather than `published` if the push fails — the work is on disk and committed
    either way, so a network failure costs a retry and never the draft.
    """
    s = story_of(draft_id)
    if s is None:
        return False, 'No such draft.', None
    story, paper = publish.expand(s)
    publish.write_story(story, paper)
    ok, log = publish.commit_and_push(f'Publish: {story["title"]}')
    store.update_draft(draft_id, status='published' if ok else 'approved')
    store.log('draft.approve', f'{draft_id} {story["slug"]} ok={ok}')
    return ok, log, story


def reject(draft_id):
    """Out of the queue, still in the database. Rejecting is not deleting."""
    store.update_draft(draft_id, status='rejected')
    store.log('draft.reject', str(draft_id))


def pending():
    """The queue: everything neither published nor rejected."""
    return [d for d in store.list_drafts()
            if d['status'] not in ('published', 'rejected')]
