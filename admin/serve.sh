#!/usr/bin/env bash
# Start the [Context] backoffice.
#
#   ./admin/serve.sh
#
# This is bash, so it needs a shell — on Windows, and for anyone who reached
# for a .sh file in a file manager, `python admin/serve.py` does the same job
# and runs everywhere.
#
# On the first run it writes admin/.env with a freshly generated secret URL
# prefix and asks for a password. After that it just starts, and prints the
# login link.
#
# For the research team it prefers the Claude Code CLI, which uses the
# subscription you have already signed into — no API key, no separate credit.
set -euo pipefail

cd "$(dirname "$0")/.."
ENV_FILE="admin/.env"

PY=$(command -v python3 >/dev/null && echo python3 || echo python)

if [ ! -f "$ENV_FILE" ]; then
  echo "First run — setting up $ENV_FILE"
  echo

  PREFIX="/b-$($PY -c 'import secrets; print(secrets.token_hex(8))')"
  echo "Secret URL prefix: $PREFIX"
  echo "(generated for you — every page lives under it)"
  echo

  printf 'Admin password (make it long, you only type it once a day): '
  read -rs PASSWORD; echo
  if [ -z "$PASSWORD" ]; then
    echo "A password is required. The backoffice will not run open." >&2
    exit 1
  fi

  BACKEND=""
  APIKEY=""
  if command -v claude >/dev/null 2>&1; then
    echo
    echo "Found the Claude Code CLI — the research team will use your"
    echo "subscription. No API key needed."
    BACKEND="cli"
  else
    echo
    echo "Claude Code is not installed. Two options:"
    echo "  1. Install it (npm i -g @anthropic-ai/claude-code), run 'claude'"
    echo "     once to sign in, and the research team uses your subscription."
    echo "  2. Paste an API key now — billed per token, separate from any"
    echo "     Claude subscription: https://platform.claude.com/settings/keys"
    echo
    printf 'API key (leave blank to install Claude Code later): '
    read -rs APIKEY; echo
    [ -n "$APIKEY" ] && BACKEND="api"
  fi

  umask 077
  cat > "$ENV_FILE" <<EOF
# Written by admin/serve.sh. Gitignored — never commit this file.
CONTEXT_ADMIN_PREFIX=$PREFIX
CONTEXT_ADMIN_PASSWORD=$PASSWORD

# cli = Claude Code, on your subscription.  api = Anthropic API key.
# Leave blank to auto-detect (CLI first, because it costs nothing extra).
CONTEXT_LLM_BACKEND=$BACKEND
ANTHROPIC_API_KEY=$APIKEY

# Set to 1 only for local http:// testing. Never on a real host.
CONTEXT_ADMIN_INSECURE_COOKIE=1
EOF
  echo
  echo "Wrote $ENV_FILE (readable only by you)."
  echo
fi

PREFIX=$(grep -E '^CONTEXT_ADMIN_PREFIX=' "$ENV_FILE" | cut -d= -f2-)
PORT="${PORT:-8800}"

if ! $PY -c 'import fastapi, uvicorn' 2>/dev/null; then
  echo "Installing dependencies…"
  $PY -m pip install --quiet -r admin/requirements.txt
fi

# Say which backend is live before starting, so a missing login is obvious now
# rather than four minutes into a research run.
if command -v claude >/dev/null 2>&1; then
  echo "Research backend: Claude Code CLI (your subscription)"
  if ! claude -p 'Reply with exactly: ok' --output-format json \
       --disallowedTools '*' --max-turns 1 >/dev/null 2>&1; then
    echo "  ! The CLI is installed but the check call failed."
    echo "    Run 'claude' once in a terminal and sign in."
  fi
elif grep -qE '^ANTHROPIC_API_KEY=.+' "$ENV_FILE"; then
  echo "Research backend: Anthropic API key (billed per token)"
else
  echo "Research backend: none — Generate will not run."
  echo "  Install Claude Code and sign in, or add ANTHROPIC_API_KEY to $ENV_FILE."
fi
echo

echo "───────────────────────────────────────────────────────────"
echo " Sign in:  http://127.0.0.1:$PORT$PREFIX/"
echo "───────────────────────────────────────────────────────────"
echo

exec $PY -m uvicorn admin.app:app --host 127.0.0.1 --port "$PORT"
