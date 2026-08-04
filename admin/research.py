# -*- coding: utf-8 -*-
"""The research team.

Six agents in a fixed order, each one a separate Claude call with its own
system prompt and its own job:

    Planner      decides the lens, the working title, the candidate Turn,
                 and the questions the research has to answer
    Searcher     runs web search against those questions
    Reader       fetches the best sources and pulls out specific numbers
    Fact checker grades every claim, and throws out what it cannot support
    Writer       turns surviving claims into a story brief and a paper
    Editor       runs the STYLE.md checklist and fixes what fails

Why six calls and not one: each stage gets a clean context containing only
what it needs, and each stage's output is stored so a human can audit the
chain rather than trusting a finished draft on faith. That is the same
argument as the papers behind the stories — being checkable is the product.

The pipeline never publishes. It produces a draft in the queue, and a person
approves it. That gate is deliberate: a wrong explanation costs more trust
than a right one earns.
"""
import json
import os
import time

import anthropic

MODEL = 'claude-opus-5'

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _house_rules():
    """STYLE.md is the brief. Load it rather than paraphrasing it here, so the
    agents and the humans are working from one document."""
    try:
        with open(os.path.join(ROOT, 'STYLE.md'), encoding='utf-8') as fh:
            return fh.read()
    except OSError:
        return ''


class Refused(RuntimeError):
    """Claude's safety classifiers declined the request."""


class Stage:
    """One agent. Wraps the call so every stage handles refusals, server-tool
    pauses, and token accounting the same way."""

    def __init__(self, client, on_tokens=None):
        self.client = client
        self.on_tokens = on_tokens or (lambda a, b: None)

    def _account(self, response):
        u = response.usage
        self.on_tokens(
            (u.input_tokens or 0) + (getattr(u, 'cache_read_input_tokens', 0) or 0)
            + (getattr(u, 'cache_creation_input_tokens', 0) or 0),
            u.output_tokens or 0)

    def call(self, system, prompt, schema=None, tools=None, effort='high',
             max_tokens=16000):
        messages = [{'role': 'user', 'content': prompt}]
        kwargs = {
            'model': MODEL,
            'max_tokens': max_tokens,
            'system': system,
            'thinking': {'type': 'adaptive'},
            'output_config': {'effort': effort},
        }
        if schema:
            kwargs['output_config']['format'] = {'type': 'json_schema', 'schema': schema}
        if tools:
            kwargs['tools'] = tools

        # A server-side tool loop can hit its iteration limit and come back with
        # stop_reason "pause_turn". Re-sending the same conversation resumes it;
        # the cap stops a runaway from billing forever.
        for _ in range(6):
            response = self.client.messages.create(messages=messages, **kwargs)
            self._account(response)
            if response.stop_reason == 'refusal':
                detail = getattr(response.stop_details, 'category', None)
                raise Refused(f'Claude declined this request ({detail or "no category"}).')
            if response.stop_reason != 'pause_turn':
                break
            messages = [messages[0], {'role': 'assistant', 'content': response.content}]
        else:
            raise RuntimeError('Server tool loop did not settle after 6 continuations.')

        text = '\n'.join(b.text for b in response.content if b.type == 'text')
        if schema:
            return json.loads(text)
        return text


# ---------------------------------------------------------------- schemas

PLAN_SCHEMA = {
    'type': 'object',
    'properties': {
        'lens': {'type': 'string', 'enum': ['What', 'Why', 'How', 'What if']},
        'domain': {'type': 'string'},
        'slug': {'type': 'string'},
        'title': {'type': 'string'},
        'candidate_turn': {'type': 'string'},
        'why_it_matters': {'type': 'string'},
        'questions': {'type': 'array', 'items': {'type': 'string'}},
        'earth_check': {'type': 'string'},
    },
    'required': ['lens', 'domain', 'slug', 'title', 'candidate_turn',
                 'why_it_matters', 'questions', 'earth_check'],
    'additionalProperties': False,
}

CHECK_SCHEMA = {
    'type': 'object',
    'properties': {
        'verdict': {'type': 'string', 'enum': ['proceed', 'revise', 'drop']},
        'verdict_reason': {'type': 'string'},
        'turn': {'type': 'string'},
        'findings': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'claim': {'type': 'string'},
                    'confidence': {'type': 'string', 'enum': [
                        'established', 'best current explanation', 'contested']},
                    'basis': {'type': 'string'},
                },
                'required': ['claim', 'confidence', 'basis'],
                'additionalProperties': False,
            },
        },
        'contested': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'question': {'type': 'string'},
                    'dispute': {'type': 'string'},
                },
                'required': ['question', 'dispute'],
                'additionalProperties': False,
            },
        },
        'unknowns': {'type': 'array', 'items': {'type': 'string'}},
        'discarded': {'type': 'array', 'items': {'type': 'string'}},
    },
    'required': ['verdict', 'verdict_reason', 'turn', 'findings', 'contested',
                 'unknowns', 'discarded'],
    'additionalProperties': False,
}

# Mirrors the brief shape in library.py. The writer fills this and the expander
# in publish.py turns it into the same dicts the hand-written stories use.
DIAGRAM_SCHEMA = {
    'type': 'object',
    'properties': {
        'kind': {'type': 'string', 'enum': [
            'timeline', 'ranked', 'curves', 'layers', 'compare', 'parts', 'field']},
        'title': {'type': 'string'},
        'sub': {'type': 'string'},
        'data': {'type': 'string', 'description':
                 'JSON object of the kind-specific fields, as a string.'},
        'caption': {'type': 'string'},
    },
    'required': ['kind', 'title', 'sub', 'data', 'caption'],
    'additionalProperties': False,
}

STORY_SCHEMA = {
    'type': 'object',
    'properties': {
        'slug': {'type': 'string'},
        'lens': {'type': 'string', 'enum': ['What', 'Why', 'How', 'What if']},
        'domain': {'type': 'string'},
        'title': {'type': 'string'},
        'teaser': {'type': 'string'},
        'takeaway': {'type': 'string'},
        'tone': {'type': 'string', 'enum': [
            'dusk', 'ember', 'deepsea', 'nebula', 'forest', 'solar', 'rose', 'void']},
        'scene': {'type': 'string', 'enum': [
            'earth', 'cell', 'night', 'fading', 'dividing', 'cosmos', 'crowd',
            'city', 'ocean', 'mind', 'colony', 'matter', 'time', 'sun']},
        'standfirst': {'type': 'string'},
        'wrong_head': {'type': 'string'},
        'wrong_body': {'type': 'string'},
        'diagram_one': DIAGRAM_SCHEMA,
        'crack_head': {'type': 'string'},
        'crack_body': {'type': 'string'},
        'turn': {'type': 'string'},
        'diagram_two': DIAGRAM_SCHEMA,
        'cost_head': {'type': 'string'},
        'cost_body': {'type': 'string'},
        'zoomout': {'type': 'string'},
        'paper_subtitle': {'type': 'string'},
        'paper_abstract': {'type': 'string'},
        'reading': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'source': {'type': 'string'},
                    'why': {'type': 'string'},
                },
                'required': ['source', 'why'],
                'additionalProperties': False,
            },
        },
        'method': {'type': 'string'},
    },
    'required': ['slug', 'lens', 'domain', 'title', 'teaser', 'takeaway', 'tone',
                 'scene', 'standfirst', 'wrong_head', 'wrong_body', 'diagram_one',
                 'crack_head', 'crack_body', 'turn', 'diagram_two', 'cost_head',
                 'cost_body', 'zoomout', 'paper_subtitle', 'paper_abstract',
                 'reading', 'method'],
    'additionalProperties': False,
}

EDIT_SCHEMA = {
    'type': 'object',
    'properties': {
        'story': STORY_SCHEMA,
        'checklist': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'item': {'type': 'string'},
                    'pass': {'type': 'boolean'},
                    'note': {'type': 'string'},
                },
                'required': ['item', 'pass', 'note'],
                'additionalProperties': False,
            },
        },
        'changes': {'type': 'array', 'items': {'type': 'string'}},
        'ship': {'type': 'boolean'},
    },
    'required': ['story', 'checklist', 'changes', 'ship'],
    'additionalProperties': False,
}

WEB_TOOLS = [
    {'type': 'web_search_20260209', 'name': 'web_search', 'max_uses': 12},
    {'type': 'web_fetch_20260209', 'name': 'web_fetch', 'max_uses': 10},
]


# ---------------------------------------------------------------- the agents

PLANNER = """You are the Planner on the [Context] research team.

[Context] publishes short illustrated stories about this planet, each backed by
a sourced paper. Your job is the first and most important one: decide whether a
research goal can become a story, and if so, what question it asks.

Every story asks exactly one of four questions — What, Why, How, What if — and
the title must ask that question in those words. Every story turns on a Turn: a
one-sentence reversal between what a thoughtful person believes and what is
actually the case. No Turn, no story.

Scope is Earth. Nothing beyond this planet.

You do not research. You decide what must be researched, and you say plainly in
`earth_check` whether the subject is on-scope and whether a real reversal looks
likely. If it does not, say so — a goal that cannot carry a Turn should be
rejected here rather than three agents later.

The house style bible follows. Read it; it is the brief.

---
%s"""

SEARCHER = """You are the Search Agent on the [Context] research team.

You have web search. Work through the research questions you are given and
report what the literature actually says. For each question:

  - name the specific sources you found and what each one claims
  - give the numbers, with their units and their error bars where stated
  - say plainly where sources disagree, and who is on each side
  - say plainly where you found nothing solid

Do not write prose for a reader. You are writing notes for a colleague who will
check them. Be specific, be attributable, and do not smooth over a gap. If the
popular claim about this subject turns out to be unsupported, that is the single
most valuable thing you can report."""

READER = """You are the Web Reader on the [Context] research team.

You have web fetch. Take the search notes you are given, pick the sources most
worth reading in full, and fetch them. Your job is depth, not breadth.

For each source you read, report:
  - what it actually measured or argued, in its own terms
  - the specific figures, with sample sizes and confidence intervals if given
  - what its own authors say its limitations are
  - whether it supports, complicates, or contradicts the search notes

Quote figures exactly. If a widely repeated number traces back to one study with
a narrow sample, say so — that is exactly the kind of thing the next agent needs
in order to grade it honestly."""

CHECKER = """You are the Fact Checker on the [Context] research team, and you
are the last honest gate before anything gets written.

Take the search notes and the reading notes. Produce a graded finding list.
Every finding gets exactly one confidence level:

  established                — uncontroversial, replicated, safe to state plainly
  best current explanation   — well supported, not settled
  contested                  — serious people disagree

Rules you do not bend:
  - a claim you cannot trace to something in the notes goes in `discarded`,
    with the reason. Do not repair it, do not soften it, drop it.
  - `contested` entries state the disagreement as a disagreement, naming what
    each side holds. Never resolve one by picking a winner.
  - `unknowns` is for what the research could not establish. An empty unknowns
    list on a real subject means you did not look hard enough.
  - state the Turn in one sentence, and only if the graded findings support it.

Set `verdict` to `proceed` only if there is a real reversal resting on findings
that are at least "best current explanation". Use `revise` if the subject is
sound but the Turn is wrong. Use `drop` if the premise did not survive contact
with the evidence — that is a success, not a failure."""

WRITER = """You are the Writer on the [Context] research team.

Take the graded findings and write the story and the paper. You may use only
what the fact checker passed. If a sentence you want to write is not supported
by a finding, you do not write it.

The story is six beats in this order — Wrong Picture, Crack, Turn, Machinery,
Cost, Long View — mapped to the fields you are filling:

  wrong_head/wrong_body   the Wrong Picture: what a thoughtful person believes
  diagram_one             the picture that makes the wrong picture concrete
  crack_head/crack_body   the Crack: the observation that does not fit
  turn                    the reversal, one sentence, no hedging
  diagram_two             the picture that carries the machinery
  cost_head/cost_body     the Cost: what follows, what a reader can act on
  zoomout                 the Long View: the landing. No moral.

Voice: clarity does not come from short words, it comes from correct order.
Write for an intelligent adult who does not know this subject. No exclamation
marks, no rhetorical questions to the reader, no "imagine that". Never end on an
instruction to feel something.

Diagram `data` is a JSON object encoded as a string, matching the kind:
  timeline  {"events": [[0.0, "name", "note"], ...]}
  ranked    {"rows": [["label", 0.0-1.0, "note"], ...]}
  curves    {"series": [["name", [[x,y], ...]]], "marks": [[x,"label"]],
             "axis": ["left", "right"]}
  layers    {"rows": [["name", "what", "meta"], ...]}
  compare   {"left": ["kicker", "head", ["line", ...]],
             "right": ["kicker", "head", ["line", ...]]}
  parts     {"centre": "name", "callouts": [["name", "note"], ...]}
  field     {"share": 0.0-1.0, "lit_label": "...", "dim_label": "..."}

Keep every label under 26 characters — they are drawn into a fixed viewBox and
longer strings run off the edge.

`reading` is real sources described so a reader knows what each is for. `method`
says how the work was done and names its own biases."""

EDITOR = """You are the Editor on the [Context] research team, and nothing
ships without passing you.

Run this checklist against the draft, item by item, and record a pass or fail
with a note for each:

  1. Which of the four questions is this? Does the title ask it in those words?
  2. Is the reader still standing on this planet at the end?
  3. Can you state the Turn in one sentence?
  4. Does the Wrong Picture describe what a thoughtful person actually believes?
  5. Is the Crack an observation, not an argument?
  6. Is every diagram label under 26 characters?
  7. Is there a number the reader can act on?
  8. Is every figure in the story traceable to a finding?
  9. Has the moral been removed from the end?
 10. Read it aloud. Does it sound like an adult or a worksheet?

Fix what fails, and return the corrected story — do not merely report problems.
List what you changed. Set `ship` false only if something is wrong that you
cannot fix from the material you were given."""


STAGES = ['plan', 'search', 'read', 'check', 'write', 'edit']


def run(goal, lens_hint, on_stage, on_tokens, client=None):
    """Run the whole team. `on_stage(name, output, seconds)` is called after
    each agent so the caller can persist progress; the UI polls that."""
    client = client or anthropic.Anthropic()
    agent = Stage(client, on_tokens)
    rules = _house_rules()

    def timed(name, fn):
        t0 = time.time()
        out = fn()
        on_stage(name, out if isinstance(out, str) else json.dumps(out, indent=1),
                 time.time() - t0)
        return out

    plan = timed('plan', lambda: agent.call(
        PLANNER % rules,
        f'Research goal: {goal}\n\n'
        + (f'The editor suggests the lens should be: {lens_hint}\n\n' if lens_hint else '')
        + 'Decide whether this can become a [Context] story, and plan the research.',
        schema=PLAN_SCHEMA))

    questions = '\n'.join(f'{i + 1}. {q}' for i, q in enumerate(plan['questions']))
    search = timed('search', lambda: agent.call(
        SEARCHER,
        f'Subject: {plan["title"]}\nCandidate Turn: {plan["candidate_turn"]}\n\n'
        f'Research questions:\n{questions}\n\nSearch, and report what you find.',
        tools=WEB_TOOLS, max_tokens=20000))

    read = timed('read', lambda: agent.call(
        READER,
        f'Subject: {plan["title"]}\n\nSearch notes:\n\n{search}\n\n'
        'Fetch and read the sources most worth reading in full.',
        tools=WEB_TOOLS, max_tokens=20000))

    check = timed('check', lambda: agent.call(
        CHECKER,
        f'Subject: {plan["title"]}\nCandidate Turn: {plan["candidate_turn"]}\n\n'
        f'SEARCH NOTES\n\n{search}\n\nREADING NOTES\n\n{read}\n\nGrade it.',
        schema=CHECK_SCHEMA, effort='xhigh'))

    if check['verdict'] == 'drop':
        raise RuntimeError('Fact checker dropped the story: ' + check['verdict_reason'])

    findings = json.dumps(check, indent=1)
    story = timed('write', lambda: agent.call(
        WRITER,
        f'{rules}\n\n---\n\nPLAN\n\n{json.dumps(plan, indent=1)}\n\n'
        f'GRADED FINDINGS\n\n{findings}\n\nWrite the story and the paper.',
        schema=STORY_SCHEMA, effort='xhigh', max_tokens=24000))

    edited = timed('edit', lambda: agent.call(
        EDITOR,
        f'{rules}\n\n---\n\nGRADED FINDINGS\n\n{findings}\n\n'
        f'DRAFT\n\n{json.dumps(story, indent=1)}\n\nRun the checklist.',
        schema=EDIT_SCHEMA, effort='xhigh', max_tokens=24000))

    return {'plan': plan, 'check': check, 'story': edited['story'],
            'checklist': edited['checklist'], 'changes': edited['changes'],
            'ship': edited['ship']}


REVISE = """You are the Editor on the [Context] research team, making one
requested change to a draft that is already in the approval queue.

You are given the current draft as JSON and an instruction from the editor-in-
chief. Apply the instruction and return the complete story object — every field,
not only the ones you touched.

Change what was asked and nothing else. Do not improve neighbouring prose, do
not re-balance the beats, do not add a finding. If the instruction would break a
house rule — putting the story off this planet, removing the Turn, making a
claim the paper does not support — apply what you can, and say so in `changes`.

Diagram label limit is 26 characters, as before."""


def revise(story, instruction, on_tokens=None, client=None):
    """Prompt-based edit from the approval screen."""
    agent = Stage(client or anthropic.Anthropic(), on_tokens)
    out = agent.call(
        REVISE,
        f'CURRENT DRAFT\n\n{json.dumps(story, indent=1)}\n\n'
        f'INSTRUCTION\n\n{instruction}',
        schema={'type': 'object',
                'properties': {'story': STORY_SCHEMA,
                               'changes': {'type': 'array', 'items': {'type': 'string'}}},
                'required': ['story', 'changes'],
                'additionalProperties': False},
        effort='high', max_tokens=24000)
    return out['story'], out['changes']
