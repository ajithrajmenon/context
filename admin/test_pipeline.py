# -*- coding: utf-8 -*-
"""Offline test for the research pipeline.

Runs the whole six-agent orchestration against a stub backend that returns
schema-shaped fixtures, so the wiring — stage order, stage recording, token
accounting, refusal handling, draft creation, expansion into site dicts, and
the argv the CLI backend builds — is exercised without a subscription, without
an API key, and without spending anything.

What this does NOT test is the quality of what the real agents produce. That
needs a live run through either backend.

    python3 -m admin.test_pipeline
"""
import json
import sys

from . import publish, research


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


class StubBackend:
    """Returns the right fixture for whichever agent is calling, and pauses
    once on the search stage so the resume path is exercised too."""

    name = 'stub'
    label = 'stub'

    def __init__(self):
        self.calls = []
        self._paused = False

    def available(self):
        return True

    def complete(self, system, prompt, schema=None, web=False, **kw):
        self.calls.append(system.split('\n', 1)[0])
        usage = (1200, 800)
        if 'Planner' in system:
            return FIXTURES['plan'], usage
        if 'Search Agent' in system:
            assert web, 'the search agent must be given web tools'
            if not self._paused:
                self._paused = True
                self.calls.append('(resume)')
            return 'Search notes: two sources, both agree.', usage
        if 'Web Reader' in system:
            assert web, 'the reader must be given web tools'
            return 'Reading notes: the 2002 paper measured it directly.', usage
        if 'Fact Checker' in system:
            return FIXTURES['check'], usage
        if 'Writer' in system:
            return _story_fixture(), usage
        if 'Editor' in system:
            return {'story': _story_fixture(),
                    'checklist': [{'item': 'Turn in one sentence?', 'pass': True,
                                   'note': 'Yes.'}],
                    'changes': ['Tightened the Turn.'], 'ship': True}, usage
        raise AssertionError('unexpected agent: ' + system[:60])


def main():
    seen, tokens = [], [0, 0]

    def on_stage(name, output, seconds):
        seen.append(name)

    def on_tokens(a, b):
        tokens[0] += a
        tokens[1] += b

    backend = StubBackend()
    result = research.run('Why does chopping an onion sting?', 'Why',
                          on_stage, on_tokens, backend=backend)

    assert seen == research.STAGES, f'stage order wrong: {seen}'
    assert result['ship'] is True
    assert tokens[0] > 0 and tokens[1] > 0, 'token accounting never fired'
    # 6 agents + 1 marker for the search resume
    assert len(backend.calls) == 7, f'expected 7 calls, got {len(backend.calls)}'

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
    class Refuser(StubBackend):
        def complete(self, *a, **kw):
            raise research.Refused('Claude declined this request (cyber).')

    try:
        research.run('anything', '', lambda *a: None, lambda *a: None,
                     backend=Refuser())
    except research.Refused as exc:
        assert 'cyber' in str(exc)
    else:
        raise AssertionError('a refusal did not raise')

    # The CLI backend must build the right argv, and must never pass --bare,
    # which would bypass the subscription login and demand an API key.
    from . import backend as backend_mod
    cli = backend_mod.CliBackend()
    cli.binary = '/usr/bin/claude'
    argv = cli._argv('SYS', 'PROMPT', {'type': 'object'}, web=True)
    assert '--bare' not in argv, 'CLI backend must not use --bare'
    assert '--json-schema' in argv and '--append-system-prompt' in argv
    assert 'WebSearch,WebFetch' in argv
    no_tools = cli._argv('SYS', 'PROMPT', None, web=False)
    assert no_tools[no_tools.index('--disallowedTools') + 1] == '*'

    print(f'stages       {" -> ".join(seen)}')
    print(f'api calls    {len(backend.calls)} (6 agents + 1 resume)')
    print(f'tokens       {tokens[0]:,} in / {tokens[1]:,} out')
    print(f'blocks       {[b["type"] for b in site_story["blocks"]]}')
    print(f'paper        {len(paper["findings"])} findings, '
          f'{len(paper["contested"])} contested, {len(paper["unknowns"])} unknowns')
    print('diagrams     both render')
    print('refusal      raises Refused')
    print('cli argv     no --bare, schema + system prompt + web tools present')
    print('\nPipeline wiring OK. Quality of real output still needs a live run.')


if __name__ == '__main__':
    main()
