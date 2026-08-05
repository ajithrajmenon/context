# -*- coding: utf-8 -*-
"""The house grammar: the six beats, in the one order they are allowed to be in.

Wrong Picture -> Crack -> Turn -> Machinery -> Cost -> Long View. STYLE.md
section 3 argues for that order; this module is the single place it is encoded.

It used to be encoded twice — once in `library.expand()` for the hand-written
briefs and once in `admin/publish.py:expand()` for what the research team
generates. Two copies of one grammar is a correctness problem, not an untidiness
problem: changing the order in one place would have made generated stories
silently disagree with hand-written ones, and nothing would have failed loudly.

So the order, the block shapes and the story/paper envelopes live here, and the
two callers are reduced to what they actually differ in — where the words come
from. A brief carries positional tuples; the writer returns named fields. Both
normalise into the same arguments and get back the same dicts.

Nothing in here reads a file, imports a data module or holds state, so it is
safe to import from either half at module scope.

    TONES              the eight card tones, in rotation order
    counter_tone()     the contrasting tone the Turn is set in
    stack()            the six beats as a list of blocks
    story_envelope()   the story dict build.py renders
    paper_envelope()   the paper dict build.py renders
"""

TONES = ['dusk', 'ember', 'deepsea', 'nebula', 'forest', 'solar', 'rose', 'void']

# The Turn is the pivot, so it is set in a tone three steps around the rotation
# from the story's own — far enough to read as a deliberate cut rather than a
# gradient, close enough to still belong to the same piece.
TURN_TONE_STEP = 3

# The full-bleed panel reuses the hero's artwork, offset into a different
# variant so the same scene is not framed identically twice on one page.
SCENE_VAR_OFFSET = 7


def counter_tone(tone, fallback='nebula'):
    """The tone the Turn is set in. `fallback` covers a tone we do not know —
    generated drafts are schema-constrained but older ones are not."""
    if tone not in TONES:
        return fallback
    return TONES[(TONES.index(tone) + TURN_TONE_STEP) % len(TONES)]


def stack(wrong, crack, cost, turn, teaser, scene, scene_var,
          diagram_one, diagram_two, turn_tone):
    """The six beats as blocks, in the house order.

    Each of `wrong`, `crack` and `cost` is (heading, [paragraphs]) — already
    normalised by the caller, because a brief and a generated draft carry them
    differently and that is the caller's problem, not the grammar's.

    `diagram_one` and `diagram_two` are (spec, caption). The Machinery beat is
    carried by the second diagram rather than by prose, which is why there is no
    separate text block for it.
    """
    wrong_head, wrong_body = wrong
    crack_head, crack_body = crack
    cost_head, cost_body = cost
    one_spec, one_caption = diagram_one
    two_spec, two_caption = diagram_two

    return [
        # Wrong Picture: what a thoughtful person already believes.
        {'type': 'text', 'h': wrong_head, 'p': list(wrong_body)},
        # The panel sits early, holding the teaser over the artwork as a
        # pull-quote, and sets up the Crack. It used to sit just before the Turn
        # and repeat the story's own title, which put the title on the page
        # twice and stacked two big statements back to back.
        {'type': 'scene', 'tone': 'void', 'scene': scene, 'var': scene_var,
         'h': teaser},
        {'type': 'diagram', 'spec': one_spec, 'caption': one_caption},
        # Crack: the observation that does not fit.
        {'type': 'text', 'h': crack_head, 'p': list(crack_body)},
        # Turn: the reversal, one sentence, on full colour.
        {'type': 'turn', 'tone': turn_tone, 'text': turn},
        # Machinery: carried by the picture, not by prose.
        {'type': 'diagram', 'spec': two_spec, 'caption': two_caption},
        # Cost: what follows, and what a reader can act on.
        {'type': 'text', 'h': cost_head, 'p': list(cost_body)},
    ]


def story_envelope(slug, kicker, lens, tone, title, teaser, takeaway,
                   scene, hero_var, standfirst, blocks, zoomout):
    """The story dict build.py renders. Key order is the shape generated stories
    are serialised in, so it is kept stable deliberately."""
    return {
        'slug': slug, 'kicker': kicker, 'lens': lens,
        'card_tone': tone, 'thumb': None, 'featured': False,
        'title': title, 'teaser': teaser, 'takeaway': takeaway,
        'hero': {'tone': tone, 'scene': scene, 'var': hero_var,
                 'standfirst': standfirst},
        'blocks': blocks,
        # Long View: the landing. No moral.
        'zoomout': {'tone': tone, 'text': zoomout},
    }


def research_title(title):
    """The paper's title. A story title ends in a question mark; the paper
    behind it answers the question, so the mark comes off."""
    return title.rstrip('?') + ': the research'


def paper_minutes(findings):
    """Time on the paper. Three minutes of frame plus one per finding, floored
    at four — a paper shorter than that is not carrying its story."""
    return max(4, 3 + len(findings))


def paper_envelope(slug, title, subtitle, date, abstract, findings, contested,
                   unknowns, method, reading, sections=None):
    """The paper dict build.py renders.

    `sections` is the long layer. A paper whose only section restates its own
    abstract is not a paper, so real sections are strongly preferred — but the
    briefs in library.py do not carry any, and neither do older generated
    drafts, so the abstract stands in rather than the page breaking.
    """
    return {
        'slug': slug,
        'title': title,
        'subtitle': subtitle,
        'date': date,
        'minutes': paper_minutes(findings),
        'abstract': abstract,
        'sections': list(sections or []) or [{'h': 'What we looked at', 'p': [abstract]}],
        'findings': findings, 'contested': contested,
        'unknowns': unknowns, 'method': method, 'reading': reading,
    }
