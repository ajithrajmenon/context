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
import platform
import re
import shutil
import subprocess
import tempfile


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

    Two things about the CLI shape this class, and both were learned the hard
    way:

    1. **Nothing large goes on the command line.** An agent's system prompt is
       the whole of STYLE.md — around 14 KB — and Windows runs npm's `claude`
       through a `.cmd` shim, where the ceiling is cmd.exe's 8,191 characters,
       not CreateProcess's 32,767. So the user prompt is piped on stdin and the
       system prompt goes to a temp file read via `--append-system-prompt-file`.
       Only flags and a schema are left in argv.

    2. **`--json-schema` is delivered by a tool call.** The CLI hands the model
       a `StructuredOutput` tool and fills `structured_output` from its input.
       Denying every tool and capping the run at one turn — which looks like the
       obviously safe thing to do for a stage that only has to think — denies
       that tool and kills the run before it can answer.

    Tools are the CLI's own WebSearch and WebFetch rather than the server-side
    ones: same capability, different plumbing.
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

    def _argv(self, schema, web, sys_path=None, system=None):
        """Flags only. `sys_path` is a file holding the system prompt; if the
        installed CLI is too old for that flag, `system` is passed inline."""
        argv = [self.binary, '-p', '--output-format', 'json']
        if sys_path:
            argv += ['--append-system-prompt-file', sys_path]
        elif system:
            argv += ['--append-system-prompt', system]
        if self.model:
            argv += ['--model', self.model]

        tools = ['WebSearch', 'WebFetch'] if web else []
        if schema:
            argv += ['--json-schema', json.dumps(schema)]
            # The model answers by calling this tool. Deny it and the stage
            # cannot reply at all.
            tools.append('StructuredOutput')
        if tools:
            # Web research wanders; a structured stage should answer and stop.
            argv += ['--allowedTools', ','.join(tools),
                     '--max-turns', '30' if web else '6']
        else:
            # Nothing to call: this stage only has to think and write, and a
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

        sys_path = None
        if _supports_system_prompt_file(self.binary):
            fd, sys_path = tempfile.mkstemp(prefix='context-agent-', suffix='.md')
            with os.fdopen(fd, 'w', encoding='utf-8') as fh:
                fh.write(system)
            argv = self._argv(schema, web, sys_path=sys_path)
        else:
            argv = self._argv(schema, web, system=system)
            if _oversized(argv):
                # Old CLI on a short command line: the system prompt has
                # nowhere to go but into the message itself.
                argv = self._argv(schema, web)
                prompt = f'{system}\n\n---\n\n{prompt}'

        try:
            _check_length(argv)
            # encoding is explicit because Windows would otherwise decode as
            # cp1252 and mangle every em-dash in STYLE.md.
            proc = subprocess.run(argv, input=prompt, capture_output=True,
                                  text=True, encoding='utf-8', errors='replace',
                                  cwd=self.cwd, timeout=self.timeout)
        finally:
            if sys_path:
                try:
                    os.remove(sys_path)
                except OSError:
                    pass

        if proc.returncode != 0:
            raise BackendError(_cli_error(proc))

        try:
            payload = json.loads(proc.stdout)
        except ValueError:
            raise BackendError('The CLI did not return JSON:\n'
                               + (proc.stdout or proc.stderr)[:900]) from None

        if payload.get('is_error') or payload.get('subtype') == 'error_during_execution':
            denied = [d.get('tool_name') for d in payload.get('permission_denials') or []]
            detail = payload.get('result') or '; '.join(payload.get('errors') or [])
            if denied:
                detail = (detail or 'the run stopped early') + \
                    ' — tools denied: ' + ', '.join(sorted(set(denied)))
            raise BackendError(str(detail or payload)[:900])

        # Most of a CLI turn's input arrives as cache reads, so `input_tokens`
        # alone reports a couple of tokens for a 14 KB prompt. Count all three.
        usage = payload.get('usage') or {}
        tokens = (sum(usage.get(k) or 0 for k in (
                      'input_tokens', 'cache_creation_input_tokens',
                      'cache_read_input_tokens')),
                  usage.get('output_tokens') or 0)

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


# npm installs `claude` as a .cmd shim on Windows, so the process is really
# cmd.exe, whose whole command line must fit in 8,191 characters — not the
# 32,767 CreateProcess allows. Everywhere else the limit is large enough that
# it is only worth guarding against absurdity.
_ARGV_BUDGET = 7500 if platform.system() == 'Windows' else 120000

_FILE_FLAG = {}


def _oversized(argv, budget=None):
    # +3 per argument for the quoting and separator the OS adds.
    return sum(len(a) + 3 for a in argv) > (_ARGV_BUDGET if budget is None else budget)


def _check_length(argv):
    if _oversized(argv):
        raise BackendError(
            'The command line for the CLI came out too long ({} chars, limit {}). '
            'Update Claude Code — a recent version takes the system prompt from '
            'a file, which is what keeps this small.'.format(
                sum(len(a) + 3 for a in argv), _ARGV_BUDGET))


def _supports_system_prompt_file(binary):
    """Does this build take --append-system-prompt-file?

    The flag is hidden from `--help`, so asking for a file that does not exist
    is the honest probe: a build that knows the flag complains about the file,
    one that does not complains about the flag. Neither costs an API call.
    Memoised — this runs once per binary per process.
    """
    if binary in _FILE_FLAG:
        return _FILE_FLAG[binary]
    ok = False
    try:
        probe = subprocess.run(
            [binary, '-p', 'x', '--append-system-prompt-file',
             os.path.join(tempfile.gettempdir(), 'context-probe-does-not-exist')],
            capture_output=True, text=True, encoding='utf-8', errors='replace',
            timeout=60)
        blob = ((probe.stdout or '') + (probe.stderr or '')).lower()
        ok = 'not found' in blob and 'unknown option' not in blob
    except (OSError, subprocess.SubprocessError):
        ok = False
    _FILE_FLAG[binary] = ok
    return ok


def _cli_error(proc):
    blob = (proc.stdout or '') + '\n' + (proc.stderr or '')
    low = blob.lower()
    if 'command line is too long' in low or 'argument list too long' in low:
        return ('The command line handed to Claude Code was too long for this '
                'shell. Update Claude Code (`claude update`) so the system '
                'prompt can be passed as a file instead.\n\n' + blob[:600])
    if 'unknown option' in low:
        return ('Claude Code rejected an option, which usually means the '
                'installed version is old. Run `claude update`, or '
                '`npm i -g @anthropic-ai/claude-code`.\n\n' + blob[:600])
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
