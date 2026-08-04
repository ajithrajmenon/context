# -*- coding: utf-8 -*-
"""Two ways to reach Claude, one interface.

    cli   shells out to the `claude` binary in headless mode. It authenticates
          with the subscription you already logged into, so there is no API key
          and no separate credit to buy.
    api   the Anthropic SDK with an API key, billed per token.

The six agents in research.py do not know which one they are talking to. They
hand over a system prompt, a user prompt, an optional JSON schema and an
optional tool list, and get back text or a parsed object.

Choosing between them:

    CONTEXT_LLM_BACKEND=cli   force the CLI
    CONTEXT_LLM_BACKEND=api   force the API
    unset                     CLI if the binary is on PATH, else API

One flag matters and is easy to get wrong: `claude --bare` deliberately does
not read the subscription login and requires an API key. We never pass it,
because using the subscription is the entire point of the CLI backend.
"""
import json
import os
import re
import shutil
import subprocess


class Refused(RuntimeError):
    """Claude declined the request."""


class BackendError(RuntimeError):
    """The backend could not produce an answer."""


# ---------------------------------------------------------------- API

class ApiBackend:
    """Anthropic SDK. Schema-enforced output, per-token billing."""

    name = 'api'
    label = 'Anthropic API (per-token billing)'

    def __init__(self, model='claude-opus-5'):
        import anthropic
        self._anthropic = anthropic
        self.client = anthropic.Anthropic()
        self.model = model

    def available(self):
        return bool(os.environ.get('ANTHROPIC_API_KEY'))

    def complete(self, system, prompt, schema=None, web=False, effort='high',
                 max_tokens=16000):
        messages = [{'role': 'user', 'content': prompt}]
        kwargs = {
            'model': self.model, 'max_tokens': max_tokens, 'system': system,
            'thinking': {'type': 'adaptive'},
            'output_config': {'effort': effort},
        }
        if schema:
            kwargs['output_config']['format'] = {'type': 'json_schema', 'schema': schema}
        if web:
            kwargs['tools'] = [
                {'type': 'web_search_20260209', 'name': 'web_search', 'max_uses': 12},
                {'type': 'web_fetch_20260209', 'name': 'web_fetch', 'max_uses': 10}]

        # A server-side tool loop can stop with "pause_turn" when it hits its
        # iteration limit. Re-sending resumes it; the cap stops a runaway.
        for _ in range(6):
            response = self.client.messages.create(messages=messages, **kwargs)
            usage = (response.usage.input_tokens or 0,
                     response.usage.output_tokens or 0)
            if response.stop_reason == 'refusal':
                cat = getattr(response.stop_details, 'category', None)
                raise Refused(f'Claude declined this request ({cat or "no category"}).')
            if response.stop_reason != 'pause_turn':
                break
            messages = [messages[0], {'role': 'assistant', 'content': response.content}]
        else:
            raise BackendError('Server tool loop did not settle after 6 continuations.')

        text = '\n'.join(b.text for b in response.content if b.type == 'text')
        return (json.loads(text) if schema else text), usage


# ---------------------------------------------------------------- CLI

class CliBackend:
    """The `claude` binary in headless mode, on your subscription.

    `--json-schema` gives schema-conforming output in `structured_output`, so
    the structured stages are as reliable here as on the API. Tools are the
    CLI's own WebSearch and WebFetch rather than the server-side ones — same
    capability, different plumbing.
    """

    name = 'cli'
    label = 'Claude Code CLI (your subscription)'

    def __init__(self, model=None, cwd=None, timeout=1800):
        self.binary = shutil.which('claude')
        self.model = model or os.environ.get('CONTEXT_CLI_MODEL', '')
        # Run outside the repo by default. In the repo the CLI would load
        # CLAUDE.md, hooks and plugins into every agent's context — extra
        # tokens, and behaviour that changes when the repo changes.
        self.cwd = cwd or os.environ.get('CONTEXT_CLI_CWD') or os.path.expanduser('~')
        self.timeout = int(os.environ.get('CONTEXT_CLI_TIMEOUT', timeout))

    def available(self):
        return bool(self.binary)

    def _argv(self, system, prompt, schema, web):
        argv = [self.binary, '-p', prompt, '--output-format', 'json',
                '--append-system-prompt', system]
        if self.model:
            argv += ['--model', self.model]
        if schema:
            argv += ['--json-schema', json.dumps(schema)]
        if web:
            argv += ['--allowedTools', 'WebSearch,WebFetch', '--max-turns', '30']
        else:
            # No tools at all: these stages only have to think and write, and a
            # tool call here would be the agent wandering off its job.
            argv += ['--disallowedTools', '*', '--max-turns', '1']
        return argv

    def complete(self, system, prompt, schema=None, web=False, effort='high',
                 max_tokens=16000):
        if not self.binary:
            raise BackendError(
                'The `claude` command is not on PATH. Install Claude Code and '
                'run `claude` once to sign in, or set an ANTHROPIC_API_KEY to '
                'use the API backend instead.')

        proc = subprocess.run(self._argv(system, prompt, schema, web),
                              capture_output=True, text=True, cwd=self.cwd,
                              timeout=self.timeout)
        if proc.returncode != 0:
            raise BackendError(_cli_error(proc))

        try:
            payload = json.loads(proc.stdout)
        except ValueError:
            raise BackendError('The CLI did not return JSON:\n'
                               + (proc.stdout or proc.stderr)[:900]) from None

        if payload.get('is_error') or payload.get('subtype') == 'error_during_execution':
            raise BackendError(str(payload.get('result') or payload)[:900])

        usage = payload.get('usage') or {}
        tokens = (usage.get('input_tokens', 0) or 0, usage.get('output_tokens', 0) or 0)

        if schema:
            out = payload.get('structured_output')
            if out is None:
                # Older CLI builds ignore --json-schema. Fall back to pulling
                # JSON out of the text so a stale install degrades instead of
                # failing outright.
                out = _loads_loose(payload.get('result', ''))
            if out is None:
                raise BackendError(
                    'The CLI returned no structured output. Update Claude Code '
                    '(`claude update`) — --json-schema needs a recent version.')
            return out, tokens

        return payload.get('result', ''), tokens


def _cli_error(proc):
    blob = (proc.stdout or '') + '\n' + (proc.stderr or '')
    low = blob.lower()
    if 'invalid api key' in low or 'authentication' in low or 'not logged in' in low:
        return ('Claude Code is not signed in. Run `claude` once in a terminal '
                'and log in with your subscription, then try again.\n\n' + blob[:600])
    if 'rate limit' in low or 'usage limit' in low:
        return ('Your Claude subscription has hit its usage limit. Wait for the '
                'window to reset, or switch to the API backend.\n\n' + blob[:600])
    return f'claude exited {proc.returncode}:\n{blob[:900]}'


def _loads_loose(text):
    """Best-effort JSON out of prose. Only used when structured_output is absent."""
    if not text:
        return None
    fence = re.search(r'```(?:json)?\s*(.+?)```', text, re.S)
    if fence:
        text = fence.group(1)
    start, end = text.find('{'), text.rfind('}')
    if start == -1 or end <= start:
        return None
    try:
        return json.loads(text[start:end + 1])
    except ValueError:
        return None


# ---------------------------------------------------------------- choosing

def get(name=None):
    """Pick a backend. Explicit choice wins; otherwise prefer the subscription
    because it costs nothing extra."""
    name = (name or os.environ.get('CONTEXT_LLM_BACKEND') or '').strip().lower()

    if name == 'api':
        return ApiBackend()
    if name == 'cli':
        return CliBackend()
    if name:
        raise BackendError(f'Unknown CONTEXT_LLM_BACKEND {name!r}. Use cli or api.')

    cli = CliBackend()
    if cli.available():
        return cli
    if os.environ.get('ANTHROPIC_API_KEY'):
        return ApiBackend()
    raise BackendError(
        'No way to reach Claude. Either install Claude Code and sign in '
        '(no API credit needed), or set ANTHROPIC_API_KEY.')


def describe():
    """One line for the UI, without raising if nothing is configured."""
    try:
        backend = get()
    except BackendError as exc:
        return 'none', str(exc)
    return backend.name, backend.label
