# -*- coding: utf-8 -*-
"""Start the [Context] backoffice, on any operating system.

    python admin/serve.py

On the first run it writes admin/.env with a freshly generated secret URL
prefix and asks for a password. After that it just starts, and prints the
login link.

This exists because admin/serve.sh is a bash script: on Windows there is no
bash to run it, and double-clicking a .sh file only makes Explorer ask which
application to open it with. Everything the shell script does, this does, and
it runs the same way on Windows, macOS and Linux.

For the research team it prefers the Claude Code CLI, which uses the
subscription you have already signed into — no API key, no separate credit.
"""
import getpass
import os
import secrets
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join(ROOT, 'admin', '.env')
RULE = '─' * 59


def _read_env(path):
    values = {}
    try:
        with open(path, encoding='utf-8') as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    values[key.strip()] = value.strip()
    except OSError:
        pass
    return values


def _claude():
    return shutil.which('claude')


def _first_run():
    print('First run — setting up admin/.env\n')

    prefix = '/b-' + secrets.token_hex(8)
    print('Secret URL prefix: ' + prefix)
    print('(generated for you — every page lives under it)\n')

    password = getpass.getpass(
        'Admin password (make it long, you only type it once a day): ')
    if not password:
        sys.exit('A password is required. The backoffice will not run open.')

    backend, api_key = '', ''
    if _claude():
        print('\nFound the Claude Code CLI — the research team will use your')
        print('subscription. No API key needed.')
        backend = 'cli'
    else:
        print('\nClaude Code is not installed. Two options:')
        print('  1. Install it (npm i -g @anthropic-ai/claude-code), run "claude"')
        print('     once to sign in, and the research team uses your subscription.')
        print('  2. Paste an API key now — billed per token, separate from any')
        print('     Claude subscription: https://platform.claude.com/settings/keys\n')
        api_key = getpass.getpass('API key (leave blank to install Claude Code later): ')
        if api_key:
            backend = 'api'

    body = f"""# Written by admin/serve.py. Gitignored — never commit this file.
CONTEXT_ADMIN_PREFIX={prefix}
CONTEXT_ADMIN_PASSWORD={password}

# cli = Claude Code, on your subscription.  api = Anthropic API key.
# Leave blank to auto-detect (CLI first, because it costs nothing extra).
CONTEXT_LLM_BACKEND={backend}
ANTHROPIC_API_KEY={api_key}

# Set to 1 only for local http:// testing. Never on a real host.
CONTEXT_ADMIN_INSECURE_COOKIE=1
"""
    # Create it unreadable to anyone else before a password goes in it. The
    # mode is honoured on Unix; Windows relies on the profile's own ACLs.
    fd = os.open(ENV_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as fh:
        fh.write(body)
    print('\nWrote admin/.env — it holds your password, and it is gitignored.\n')


def _ensure_deps():
    try:
        import fastapi, uvicorn  # noqa: F401
        return
    except ImportError:
        pass
    print('Installing dependencies…')
    req = os.path.join(ROOT, 'admin', 'requirements.txt')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--quiet', '-r', req])


def _report_backend(env):
    """Say which backend is live before starting, so a missing login is obvious
    now rather than four minutes into a research run."""
    binary = _claude()
    if binary:
        print('Research backend: Claude Code CLI (your subscription)')
        probe = subprocess.run(
            [binary, '-p', 'Reply with exactly: ok', '--output-format', 'json',
             '--disallowedTools', '*', '--max-turns', '1'],
            capture_output=True, text=True, encoding='utf-8', errors='replace')
        if probe.returncode != 0:
            print('  ! The CLI is installed but the check call failed.')
            print('    Run "claude" once in a terminal and sign in.')
    elif env.get('ANTHROPIC_API_KEY'):
        print('Research backend: Anthropic API key (billed per token)')
    else:
        print('Research backend: none — Generate will not run.')
        print('  Install Claude Code and sign in, or add ANTHROPIC_API_KEY '
              'to admin/.env.')
    print()


def main():
    os.chdir(ROOT)
    if not os.path.exists(ENV_FILE):
        _first_run()

    env = _read_env(ENV_FILE)
    prefix = env.get('CONTEXT_ADMIN_PREFIX', '')
    port = os.environ.get('PORT', '8800')

    _ensure_deps()
    _report_backend(env)

    print(RULE)
    print(f' Sign in:  http://127.0.0.1:{port}{prefix}/')
    print(RULE)
    print()

    argv = [sys.executable, '-m', 'uvicorn', 'admin.app:app',
            '--host', '127.0.0.1', '--port', port]
    if os.name == 'nt':
        # Windows has no exec that replaces the process cleanly; a child keeps
        # Ctrl-C working the way you expect.
        sys.exit(subprocess.call(argv))
    os.execv(sys.executable, argv)


if __name__ == '__main__':
    main()
