#!/usr/bin/env bash
# Start the [Context] backoffice.
#
#   ./admin/serve.sh
#
# On the first run it writes admin/.env with a freshly generated secret URL
# prefix and prompts for the two secrets it cannot invent. After that it just
# starts, and prints the login link.
set -euo pipefail

cd "$(dirname "$0")/.."
ENV_FILE="admin/.env"

py() { command -v python3 >/dev/null && echo python3 || echo python; }
PY=$(py)

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

  printf 'Anthropic API key from https://platform.claude.com/settings/keys\n'
  printf '(leave blank to set up later — everything except Generate still works): '
  read -rs APIKEY; echo

  umask 077
  cat > "$ENV_FILE" <<EOF
# Written by admin/serve.sh. Gitignored — never commit this file.
CONTEXT_ADMIN_PREFIX=$PREFIX
CONTEXT_ADMIN_PASSWORD=$PASSWORD
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

if ! $PY -c 'import fastapi, uvicorn, anthropic' 2>/dev/null; then
  echo "Installing dependencies…"
  $PY -m pip install --quiet -r admin/requirements.txt
fi

if ! grep -qE '^ANTHROPIC_API_KEY=.+' "$ENV_FILE"; then
  echo "Note: no ANTHROPIC_API_KEY set — Generate will not run."
  echo "      Add it to $ENV_FILE when you have one."
  echo
fi

echo "───────────────────────────────────────────────────────────"
echo " Sign in:  http://127.0.0.1:$PORT$PREFIX/"
echo "───────────────────────────────────────────────────────────"
echo

exec $PY -m uvicorn admin.app:app --host 127.0.0.1 --port "$PORT"
