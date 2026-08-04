# -*- coding: utf-8 -*-
"""Offline test for the research pipeline.

Runs the whole six-agent orchestration against a stub client that returns
schema-shaped fixtures, so the wiring — stage order, stage recording, token
accounting, refusal handling, pause_turn resumption, draft creation and the
expansion into site dicts — is exercised without an API key and without
spending anything.

What this does NOT test is the quality of what the real agents produce. That
needs a key and a live run.

    python3 -m admin.test_pipeline
"""
import json
import sys
import types

from . import publish, research


class _Block:
    def __init__(self, text):
        self.type = 'text'
        self.text = text


class _Usage:
    input_tokens = 1200
    output_tokens = 800
    cache_read_input_tokens = 0
    cache_creation_input_tokens = 0


class _Response:
    def __init__(self, text, stop_reason='end_turn'):
        self.content = [_Block(text)]
        self.stop_reason = stop_reason
        self.stop_details = None
        self.usage = _Usage()


FIXTURES = {
    'plan': {
        'lens': 'Why', 'domain': 'Kitchen', 'slug': 'why-onions-sting',
        'title': 'Why does chopping an onion sting?',
        'candidate_turn': 'The onion manufactures the irritant when you cut it.',
        'why_it_matters': 'It decides which kitchen tricks can possibly work.',
        'questions': ['What compound causes the irritation?',
                      'Is it present before cutting?'],
        'earth_check': 'On this planet, and the reversal looks real.',
    },
    'check': {
        'verdict': 'proceed', 'verdict_reason': 'Two established findings carry it.',
        'turn': 'The onion manufactures the irritant at the moment you cut it.',
        'findings': [
            {'claim': 'The irritant forms enzymatically on tissue damage.',
             'confidence': 'established', 'basis': 'Pathway characterised.'},
            {'claim': 'A dedicated enzyme controls its formation.',
             'confidence': 'established', 'basis': 'Identified in 2002.'}],
        'contested': [{'question': 'Do low-tear cultivars keep their flavour?',
                       'dispute': 'Taste panel results are mixed.'}],
        'unknowns': ['Why individual sensitivity varies so widely.'],
        'discarded': ['"Holding a spoon in your mouth helps" — no support.'],
    },
}


def _story_fixture():
    return {
        'slug': 'why-onions-sting', 'lens': 'Why', 'domain': 'Kitchen',
        'title': 'Why does chopping an onion sting?',
        'teaser': 'The onion is defending itself, and most kitchen tricks do nothing.',
        'takeaway': 'The two things that work, and why the rest are theatre.',
        'tone': 'forest', 'scene': 'matter',
        'standfirst': 'An intact onion is harmless. The weapon does not exist until you cut.',
        'wrong_head': 'It is not in the onion',
        'wrong_body': 'The onion stores a harmless compound and an enzyme apart.',
        'diagram_one': {
            'kind': 'timeline', 'title': 'From cut to tears', 'sub': 'Seconds.',
            'data': json.dumps({'events': [[0, 'Intact', 'Stored apart'],
                                           [0.5, 'Cut', 'They mix'],
                                           [1, 'Contact', 'Meets the eye']]}),
            'caption': 'The irritant is manufactured by the damage you did.'},
        'crack_head': 'Your eye is doing the right thing',
        'crack_body': 'Corneal nerves detect a mild acid and trigger reflex tearing.',
        'turn': 'The onion is not making you cry. It is releasing a chemical weapon.',
        'diagram_two': {
            'kind': 'compare', 'title': 'The kitchen tricks, sorted',
            'sub': 'Judged on the mechanism.',
            'data': json.dumps({'left': ['Works', 'Because', ['A sharp knife.', 'Chilling.']],
                                'right': ['Does not', 'Because', ['Bread in your mouth.']]}),
            'caption': 'Everything that works removes or slows the vapour.'},
        'cost_head': 'Why the onion bothers',
        'cost_body': 'It is a defence against being eaten, aimed at animals that dig.',
        'zoomout': 'A plant evolved a weapon so effective we now grow it deliberately.',
        'paper_subtitle': 'The lachrymatory factor and the efficacy of mitigations.',
        'paper_abstract': 'We reviewed the enzymatic pathway and common mitigations.',
        'reading': [{'source': 'Imai et al. (2002)', 'why': 'Identified the enzyme.'}],
        'method': 'Synthesis of food chemistry research.',
    }


class StubClient:
    """Returns the right fixture for whichever agent is calling, and pauses once
    on the search stage so the pause_turn path is exercised too."""

    def __init__(self):
        self.calls = []
        self.messages = types.SimpleNamespace(create=self._create)
        self._paused = False

    def _create(self, **kw):
        system = kw.get('system', '')
        self.calls.append(system.split('\n', 1)[0])
        if 'Planner' in system:
            return _Response(json.dumps(FIXTURES['plan']))
        if 'Search Agent' in system:
            if not self._paused:            # exercise the server-tool pause path
                self._paused = True
                return _Response('partial search notes', stop_reason='pause_turn')
            return _Response('Search notes: two sources, both agree.')
        if 'Web Reader' in system:
            return _Response('Reading notes: the 2002 paper measured it directly.')
        if 'Fact Checker' in system:
            return _Response(json.dumps(FIXTURES['check']))
        if 'Writer' in system:
            return _Response(json.dumps(_story_fixture()))
        if 'Editor' in system:
            return _Response(json.dumps({
                'story': _story_fixture(),
                'checklist': [{'item': 'Turn in one sentence?', 'pass': True, 'note': 'Yes.'}],
                'changes': ['Tightened the Turn.'], 'ship': True}))
        raise AssertionError('unexpected agent: ' + system[:60])


def main():
    seen, tokens = [], [0, 0]

    def on_stage(name, output, seconds):
        seen.append(name)

    def on_tokens(a, b):
        tokens[0] += a
        tokens[1] += b

    client = StubClient()
    result = research.run('Why does chopping an onion sting?', 'Why',
                          on_stage, on_tokens, client=client)

    assert seen == research.STAGES, f'stage order wrong: {seen}'
    assert result['ship'] is True
    assert tokens[0] > 0 and tokens[1] > 0, 'token accounting never fired'
    # 6 agents + 1 extra call for the pause_turn resume
    assert len(client.calls) == 7, f'expected 7 calls, got {len(client.calls)}'

    story = dict(result['story'])
    story['_findings'] = result['check']
    story['_date'] = 'August 2026'
    site_story, paper = publish.expand(story)

    assert site_story['lens'] == 'Why'
    assert [b['type'] for b in site_story['blocks']] == [
        'text', 'scene', 'diagram', 'text', 'turn', 'diagram', 'text']
    assert len(paper['findings']) == 2
    assert len(paper['contested']) == 1
    assert paper['unknowns'], 'unknowns dropped in expansion'

    # The diagram specs must survive into something diagram.build() accepts.
    sys.path.insert(0, publish.ROOT)
    import diagram
    for block in site_story['blocks']:
        if block['type'] == 'diagram':
            svg = diagram.build(block['spec'])
            assert svg.startswith('<svg'), 'diagram did not render'

    # Refusals must raise rather than returning a half-formed draft.
    class Refuser(StubClient):
        def _create(self, **kw):
            r = _Response('')
            r.stop_reason = 'refusal'
            r.stop_details = types.SimpleNamespace(category='cyber')
            return r

    try:
        research.run('anything', '', lambda *a: None, lambda *a: None, client=Refuser())
    except research.Refused as exc:
        assert 'cyber' in str(exc)
    else:
        raise AssertionError('a refusal did not raise')

    print(f'stages       {" -> ".join(seen)}')
    print(f'api calls    {len(client.calls)} (6 agents + 1 pause_turn resume)')
    print(f'tokens       {tokens[0]:,} in / {tokens[1]:,} out')
    print(f'blocks       {[b["type"] for b in site_story["blocks"]]}')
    print(f'paper        {len(paper["findings"])} findings, '
          f'{len(paper["contested"])} contested, {len(paper["unknowns"])} unknowns')
    print('diagrams     both render')
    print('refusal      raises Refused')
    print('\nPipeline wiring OK. Quality of real output still needs a live run.')


if __name__ == '__main__':
    main()
