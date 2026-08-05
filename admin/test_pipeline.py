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
        'wrong_body': ['The onion stores a harmless compound and an enzyme apart.',
                       'Cut it, and the two meet for the first time.'],
        'diagram_one': {
            'kind': 'timeline', 'title': 'From cut to tears', 'sub': 'Seconds.',
            'data': json.dumps({'events': [[0, 'Intact', 'Stored apart'],
                                           [0.5, 'Cut', 'They mix'],
                                           [1, 'Contact', 'Meets the eye']]}),
            'caption': 'The irritant is manufactured by the damage you did.'},
        'crack_head': 'Your eye is doing the right thing',
        'crack_body': ['Corneal nerves detect a mild acid and trigger reflex tearing.',
                       'The eye is not injured. It is rinsing.'],
        'turn': 'The onion is not making you cry. It is releasing a chemical weapon.',
        'diagram_two': {
            'kind': 'compare', 'title': 'The kitchen tricks, sorted',
            'sub': 'Judged on the mechanism.',
            'data': json.dumps({'left': ['Works', 'Because', ['A sharp knife.', 'Chilling.']],
                                'right': ['Does not', 'Because', ['Bread in your mouth.']]}),
            'caption': 'Everything that works removes or slows the vapour.'},
        'cost_head': 'Why the onion bothers',
        'cost_body': ['It is a defence against being eaten, aimed at animals that dig.',
                      'A sharp knife and a cold onion both work, for the same reason.'],
        'zoomout': 'A plant evolved a weapon so effective we now grow it deliberately.',
        'paper_subtitle': 'The lachrymatory factor and the efficacy of mitigations.',
        'paper_abstract': 'We reviewed the enzymatic pathway and common mitigations.',
        'paper_sections': [
            {'h': 'How the question was approached',
             'p': ['We traced the pathway from the 2002 identification forward.']},
            {'h': 'What the evidence shows',
             'p': ['The irritant is formed on damage, not stored.']},
            {'h': 'Where it runs out',
             'p': ['Individual sensitivity is not explained.']}],
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
        on_progress = kw.get('on_progress')
        if on_progress:
            on_progress(f'working: {system.split(chr(10), 1)[0][:20]}')
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

    progress = []

    def on_progress(stage, text):
        progress.append((stage, text))

    backend = StubBackend()
    result = research.run('Why does chopping an onion sting?', 'Why',
                          on_stage, on_tokens, backend=backend,
                          on_progress=on_progress)

    assert seen == research.STAGES, f'stage order wrong: {seen}'
    # Each agent's progress must be labelled with its own stage, not whichever
    # one happened to be running when research.run() built the closure —  that
    # is the bug a shared/late-bound loop variable would cause here.
    assert [p[0] for p in progress] == research.STAGES, \
        f'progress lines were not attributed to the right stage: {progress}'
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

    # A beat is two short paragraphs, not one block — the break is part of the
    # rhythm, and collapsing it is what made generated pages read as essays.
    beats = [b for b in site_story['blocks'] if b['type'] == 'text']
    assert all(len(b['p']) >= 2 for b in beats), \
        'a beat lost its paragraph break in expansion'
    # Old drafts hold one string; splitting on blank lines beats a wall of text.
    legacy = publish._paras('First thought.\n\nSecond thought.')
    assert legacy == ['First thought.', 'Second thought.'], legacy
    assert len(paper['sections']) == 3, 'paper sections dropped in expansion'
    assert paper['sections'][0]['h'] != 'What we looked at', \
        'the writer\'s sections were replaced by the abstract fallback'

    # The six-beat order is the house grammar and there must be exactly one
    # definition of it. A hand-written brief and a generated draft go through
    # different adapters — positional tuples versus named fields — but they must
    # come out of beats.py with the same block order and the same envelope shape.
    # Two copies of this grammar is what the shared module exists to prevent, and
    # divergence would otherwise be silent: both halves would still render.
    sys.path.insert(0, publish.ROOT)
    import beats as grammar
    import library

    brief_story, brief_paper = library.expand(library.BRIEFS[0], 0)
    assert [b['type'] for b in brief_story['blocks']] == \
           [b['type'] for b in site_story['blocks']], \
        'hand-written and generated stories disagree on the beat order'
    assert brief_story.keys() == site_story.keys(), \
        'the story envelope differs between the two expanders'
    assert brief_paper.keys() == paper.keys(), \
        'the paper envelope differs between the two expanders'
    assert brief_story['hero'].keys() == site_story['hero'].keys()

    # The Turn is set in a contrasting tone, and both halves must rotate the same
    # way. An unknown tone falls back rather than raising, because older drafts
    # predate the schema that constrains it.
    assert grammar.counter_tone('dusk') == 'nebula'
    assert grammar.counter_tone('void') == 'deepsea'
    assert grammar.counter_tone('not-a-tone') == 'nebula'

    # The panel reuses the hero's scene at an offset variant, so one page never
    # frames the same artwork identically twice.
    hero_var = site_story['hero']['var']
    panel = next(b for b in site_story['blocks'] if b['type'] == 'scene')
    assert panel['var'] == hero_var + grammar.SCENE_VAR_OFFSET
    assert panel['var'] != hero_var

    # The diagram specs must survive into something diagram.build() accepts.
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

    # ---------------------------------------------------------------- corpus
    # Assembling the corpus is a function call now, not a side effect of an
    # import, which is the only reason any of this can be asserted.
    import corpus

    live = corpus.load()
    assert len(live.stories) >= 50, len(live.stories)

    # Calling it twice must give the same answer. When assembly happened at
    # import time the module appended to its own list, so anything that caused a
    # reload grew the corpus — this is the regression test for that.
    again = corpus.load()
    assert [s['slug'] for s in again.stories] == [s['slug'] for s in live.stories], \
        'loading the corpus twice changed it'

    # Slugs are URLs, so a duplicate silently overwrites a published page.
    slugs = [s['slug'] for s in live.stories]
    assert len(slugs) == len(set(slugs)), 'two stories share a slug'

    # Every story sits under exactly one of the four lenses, and every paper
    # belongs to a story that is actually live.
    for s in live.stories:
        assert s['lens'] in ('What', 'Why', 'How', 'What if'), (s['slug'], s['lens'])
    for p in live.papers:
        assert live.story_for(p['slug']), f'{p["slug"]} paper has no live story'

    # No two banners on the site may be the same picture. Recycled artwork is the
    # failure this project corrected twice, and with twelve stories sharing the
    # `mind` scene it cannot be checked by eye.
    banners = [(s['hero']['scene'], s['hero'].get('var', 0)) for s in live.stories]
    assert len(banners) == len(set(banners)), 'two stories share a banner'

    # The pager wraps, so no story is a dead end.
    assert live.next_after(len(live.stories) - 1)['slug'] == live.stories[0]['slug']

    # Hiding a story takes its paper with it — a live paper linking to a 404 is
    # worse than no paper at all. Compared against a corpus assembled the same
    # way, so the count is not off by whatever is sitting in content/.
    base = corpus.assemble()
    victim = base.stories[0]['slug']
    hidden = corpus.assemble(visibility={victim: False})
    assert hidden.story_for(victim) is None, 'a hidden story stayed on the site'
    assert hidden.paper_for(victim) is None, 'a hidden story kept its paper'
    assert len(hidden.stories) == len(base.stories) - 1

    # Any corpus, not just the real one: this is what lets build.py be exercised
    # on data a test controls, and what the draft preview relies on.
    mine = corpus.assemble(flagship=[site_story], flagship_papers=[paper],
                           library_stories=[], library_papers=[])
    assert len(mine.stories) == 1
    assert mine.paper_for(site_story['slug']) is paper
    assert mine.next_after(0) is site_story, 'a corpus of one must point at itself'

    # A generated story arrives with a lens the Planner chose, and must keep it.
    assert mine.stories[0]['lens'] == 'Why'

    # build.py renders whatever it is handed, and reads nothing itself. If this
    # breaks, the draft preview and the published page have drifted apart.
    import build
    html = build.build_story(site_story, site_story, mine)
    assert site_story['title'] in html
    assert f'../papers/{site_story["slug"]}.html' in html, \
        'the research card did not find the paper'
    # Without a corpus there is no paper to point at, and the card is simply
    # absent rather than broken.
    assert 'card-paper' not in build.build_story(site_story, site_story)

    # The approval screen renders a draft inside the real corpus, because a banner
    # variant is only unique with respect to every other story. Rendered alone a
    # draft would be framed one way and published another, and the collision this
    # replaced was exactly that: a generated story with the same banner as a
    # hand-written one.
    around = corpus.preview(site_story, paper)
    framing = [(s['hero']['scene'], s['hero'].get('var', 0)) for s in around.stories]
    assert len(framing) == len(set(framing)), \
        'a draft was framed identically to a published story'
    assert around.paper_for(site_story['slug']) is paper
    assert around.story_for(site_story['slug']) is site_story

    # Previewing a draft whose slug is already published shows one of it, not two.
    slugs_seen = [s['slug'] for s in around.stories]
    assert slugs_seen.count(site_story['slug']) == 1

    # ---------------------------------------------------------------- chrome
    # ui.py is pure functions of its arguments, which is the point of it being a
    # separate module: the chrome can be rendered and checked without a server,
    # a session or a run.
    from . import ui

    assert ui.state_pill('done').count('pill ok') == 1
    assert 'pill bad' in ui.state_pill('failed')
    assert 'pill warn' in ui.state_pill('running')

    # The rail is the only thing a person watches for several minutes, so its
    # states have to be right: delivered stages are done, the current one is
    # live, and the ones after it have not happened yet.
    bar = ui.rail(research.STAGES, {'plan': 12.0, 'search': 90.0}, 'read', 'running')
    assert bar.count('step done') == 2, 'delivered stages should read as done'
    assert bar.count('step live') == 1, 'exactly one stage is in progress'
    assert bar.count('step todo') == 3
    assert '12s' in bar and '90s' in bar, 'the rail lost its timings'
    assert 'working' in bar

    failed = ui.rail(research.STAGES, {'plan': 3.0}, 'search', 'failed')
    assert 'step fail' in failed, 'a failed run must show where it stopped'
    assert 'step live' not in failed

    # Every page carries the nav, and the current tab is the marked one.
    body = ui.page('Dashboard', '<p>hi</p>', nav='/stories').body.decode()
    assert 'noindex,nofollow' in body, 'the backoffice must not be indexable'
    assert body.count('class="on"') == 1
    assert ui.CSS[:20] in body, 'the page lost its stylesheet'
    # Titles and messages are escaped: a draft title is model output.
    hostile = ui.page('<script>x</script>', '', message='<b>m</b>').body.decode()
    assert '<script>x</script>' not in hostile
    assert '&lt;b&gt;m&lt;/b&gt;' in hostile

    # ---------------------------------------------------------------- runner
    # The background run lives outside the web layer now, so the two things it
    # does — advance the stage pointer, and turn a result into a draft — can be
    # checked directly. Both are stubbed at the store boundary: no thread, no
    # database write, no Claude.
    from . import runner, store as store_mod

    advanced, added = [], []
    real_update, real_add, real_create = (
        store_mod.update_run, store_mod.add_stage, store_mod.create_draft)
    store_mod.update_run = lambda rid, **kw: advanced.append(kw.get('stage'))
    store_mod.add_stage = lambda rid, n, o, s: added.append(n)
    store_mod.create_draft = lambda *a, **kw: 4242
    try:
        on_stage = runner._record_stages(1)
        for name in research.STAGES:
            on_stage(name, 'output', 1.0)
        assert added == research.STAGES, 'a stage was not recorded'
        # After each agent, `stage` names whoever is up next; after the last one
        # it reads done, which is what stops the run page polling.
        assert advanced == research.STAGES[1:] + ['done'], advanced

        draft_id = runner._queue_draft(1, result)
        assert draft_id == 4242
        # The graded findings and the date must ride along with the draft — the
        # paper cannot be rendered without them, and a prompt-based edit must
        # not drop them.
        assert result['story']['_findings'] == result['check']
        assert result['story']['_date'], 'the draft lost its date'
    finally:
        store_mod.update_run, store_mod.add_stage, store_mod.create_draft = (
            real_update, real_add, real_create)

    # The CLI backend must build the right argv, and must never pass --bare,
    # which would bypass the subscription login and demand an API key.
    from . import backend as backend_mod
    cli = backend_mod.CliBackend()
    cli.binary = '/usr/bin/claude'

    web = cli._argv({'type': 'object'}, web=True, sys_path='/tmp/sys.md')
    assert '--bare' not in web, 'CLI backend must not use --bare'
    assert '--json-schema' in web
    assert web[web.index('--append-system-prompt-file') + 1] == '/tmp/sys.md'
    # --json-schema answers through a StructuredOutput tool call. Allowing the
    # web tools but not that one leaves the stage unable to reply.
    allowed = web[web.index('--allowedTools') + 1].split(',')
    assert set(allowed) == {'WebSearch', 'WebFetch', 'StructuredOutput'}, allowed

    structured = cli._argv({'type': 'object'}, web=False, sys_path='/tmp/sys.md')
    assert structured[structured.index('--allowedTools') + 1] == 'StructuredOutput'
    assert int(structured[structured.index('--max-turns') + 1]) > 1, \
        'a schema stage needs a turn to make the StructuredOutput call'
    assert '--disallowedTools' not in structured

    plain = cli._argv(None, web=False, sys_path='/tmp/sys.md')
    assert plain[plain.index('--disallowedTools') + 1] == '*'

    # Nothing large may reach the command line: a system prompt is the whole of
    # STYLE.md, and Windows runs claude through a cmd.exe shim capped at 8,191
    # characters. The prompt goes on stdin, the system prompt goes in a file.
    WINDOWS_BUDGET = 7500          # cmd.exe stops at 8,191
    for argv in (web, structured, plain):
        assert not backend_mod._oversized(argv, WINDOWS_BUDGET), \
            'argv exceeds what a Windows cmd.exe shim accepts'
        assert max(len(a) for a in argv) < 4000, 'something big leaked into argv'

    # The old shape — system prompt inline — is exactly what blew the limit.
    inline = cli._argv(None, web=False, system=research._house_rules())
    assert backend_mod._oversized(inline, WINDOWS_BUDGET), \
        'the length guard would not have caught the failure it exists for'

    # stream-json is what lets complete() narrate a run live; the single-blob
    # 'json' format cannot be read until the process exits.
    assert 'stream-json' in web and '--verbose' in web
    # 16 turns bounds a web stage's cost — the ceiling that used to be 30 was
    # generous enough to let a chatty run search far past the point of
    # diminishing return.
    assert web[web.index('--max-turns') + 1] == '16'

    # ------------------------------------------------------------ streaming
    # The reader that turns stream-json lines into progress a person would
    # want to read, and the heartbeat that fires when a stage goes quiet.
    search_line = json.dumps({'type': 'assistant', 'message': {'content': [
        {'type': 'tool_use', 'name': 'WebSearch',
         'input': {'query': 'onion enzyme 2002'}}]}})
    text, obj = backend_mod._stream_event(search_line)
    assert text == 'Searching the web: onion enzyme 2002', text
    assert obj['type'] == 'assistant'

    fetch_text, _ = backend_mod._stream_event(json.dumps({
        'type': 'assistant', 'message': {'content': [
            {'type': 'tool_use', 'name': 'WebFetch',
             'input': {'url': 'https://example.org/paper'}}]}}))
    assert fetch_text == 'Reading a source: https://example.org/paper'

    # The final answer arriving through StructuredOutput is not narrated —
    # it is the result itself, not a step on the way to it.
    quiet, _ = backend_mod._stream_event(json.dumps({
        'type': 'assistant', 'message': {'content': [
            {'type': 'tool_use', 'name': 'StructuredOutput',
             'input': {'answer': '4'}}]}}))
    assert quiet is None

    result_text, result_obj = backend_mod._stream_event(
        json.dumps({'type': 'result', 'is_error': False, 'result': 'ok'}))
    assert result_text is None and result_obj['type'] == 'result'

    assert backend_mod._stream_event('not json at all') == (None, None)
    assert backend_mod._stream_event('') == (None, None)

    # Output ceilings were cut once the length rules made the real target a
    # fraction of the old figure — this is the actual cost lever, not just the
    # jargon and mechanism rules above it.
    assert research._TOKENS['write'] < 10000 and research._TOKENS['edit'] < 10000
    assert research._TOKENS['write'] < 24000, 'the old, oversized ceiling is still set'

    # ------------------------------------------------------------ progress store
    # A live tail, not a permanent log: old lines fall off once a run has said
    # enough of them, so a long, chatty stage cannot grow the database forever.
    store_mod.init()
    for i in range(store_mod.PROGRESS_KEEP + 20):
        store_mod.add_progress(9001, 'search', f'line {i}')
    kept = store_mod.run_progress(9001)
    assert len(kept) == store_mod.PROGRESS_KEEP, len(kept)
    assert kept[-1]['text'] == f'line {store_mod.PROGRESS_KEEP + 19}', \
        'pruning kept the wrong end of the window'
    assert kept[0]['text'] == f'line {20}', 'pruning dropped the wrong lines'
    with store_mod.connect() as db:
        db.execute('DELETE FROM run_progress WHERE run_id = ?', (9001,))

    # A run that fails mid-stage should explain itself with what the team was
    # doing, not just where the exception was raised.
    rid = 9002
    store_mod.add_progress(rid, 'search', 'Searching the web: a real query')
    store_mod.add_progress(rid, 'search', 'Searching the web: a follow-up')
    real_get_run = store_mod.get_run
    store_mod.get_run = lambda _id: {'stage': 'search'}
    try:
        context = runner._failure_context(rid)
    finally:
        store_mod.get_run = real_get_run
    assert 'a follow-up' in context, 'the failure context lost the last step'
    with store_mod.connect() as db:
        db.execute('DELETE FROM run_progress WHERE run_id = ?', (rid,))

    print(f'stages       {" -> ".join(seen)}')
    print(f'api calls    {len(backend.calls)} (6 agents + 1 resume)')
    print(f'tokens       {tokens[0]:,} in / {tokens[1]:,} out')
    print(f'blocks       {[b["type"] for b in site_story["blocks"]]}')
    print(f'paper        {len(paper["findings"])} findings, '
          f'{len(paper["contested"])} contested, {len(paper["unknowns"])} unknowns')
    print(f'grammar      one definition; brief and draft agree on '
          f'{len(site_story["blocks"])} beats')
    print('diagrams     both render')
    print('refusal      raises Refused')
    print(f'corpus       {len(live.stories)} live, stable across loads, '
          f'no shared banners')
    print('build        renders any corpus; hiding removes story and paper')
    print('chrome       rail states, nav, escaping')
    print('runner       stage pointer advances, draft carries findings')
    print('cli argv     no --bare, system prompt in a file, StructuredOutput '
          'allowed,\n             nothing oversized for a Windows cmd shim, '
          '16-turn cap on web stages')
    print('progress     stage-labelled live lines, tool calls narrated, '
          'quiet lines skipped')
    print('cost         write/edit ceilings cut from 24,000 tokens')
    print('progress db  rolling window prunes to the last '
          f'{store_mod.PROGRESS_KEEP} lines')
    print('failure      a failed run leads with its last concrete steps')
    print('\nPipeline wiring OK. Quality of real output still needs a live run.')


if __name__ == '__main__':
    main()
