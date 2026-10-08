#!/usr/bin/env bash
# web-ui.sh: the web-ui in one command, from any folder.
#
#   ./web-ui.sh [flags]        the full start: the page installed and built when it needs it, then the server with the
#                              built page at http://127.0.0.1:8000/
#   ./web-ui.sh -dev [flags]   development: the server serves /api/ only and restarts on every change under shared/,
#                              world/, domains/, mesa_sim/, webui/ (the page excepted) and configs/; Vite's dev server
#                              at http://localhost:5173/ reloads the page on every change of its sources. After a
#                              server restart, reload the browser.
#
# [flags] are mesa_sim/run_webui.py's: the headless start's (--domain, --scenario, --run, ...) and --steps, --port.
# In -dev, --port (default 8000) is passed to Vite's dev server too, which forwards /api/ to it.
# Ctrl+C stops everything.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="$HOME/python-envs/ir-nomesa-env/bin/python"
PAGE="$ROOT/webui/page"
export PYTHONHASHSEED=0
cd "$ROOT"

DEV=false
if [[ "${1:-}" == "-dev" || "${1:-}" == "--dev" ]]; then
  DEV=true
  shift
fi

# npm ci only when node_modules is missing or older than the lock file (npm ci removes and reinstalls it all)
if [[ ! -f "$PAGE/node_modules/.package-lock.json" || "$PAGE/package-lock.json" -nt "$PAGE/node_modules/.package-lock.json" ]]; then
  echo "[web-ui.sh] installing the page's dependencies (npm ci)"
  (cd "$PAGE" && npm ci)
fi

if ! $DEV; then
  # the build only when it is missing or older than the page's sources (the sources run_webui.py checks)
  if [[ ! -f "$PAGE/dist/index.html" ]] || [[ -n "$(cd "$PAGE" && find src index.html package.json package-lock.json \
      vite.config.ts tsconfig.json -newer dist/index.html -print -quit)" ]]; then
    echo "[web-ui.sh] building the page (npm run build)"
    (cd "$PAGE" && npm run build)
  fi
  exec "$PY" mesa_sim/run_webui.py "$@"
fi

# -dev: the server's port read from the flags, for Vite's dev server and for the wait below
export WEBUI_PORT=8000
args=("$@")
for i in "${!args[@]}"; do
  case "${args[$i]}" in
    --port) WEBUI_PORT="${args[$((i + 1))]:-8000}" ;;
    --port=*) WEBUI_PORT="${args[$i]#--port=}" ;;
  esac
done

# -dev: the server under watchfiles in the background, Vite's dev server in the foreground once the server answers
quoted=""
(($#)) && quoted="$(printf ' %q' "$@")"
trap 'trap - EXIT; kill 0' EXIT INT TERM
"$PY" -m watchfiles --filter default --ignore-paths webui/page \
  "$PY mesa_sim/run_webui.py --api_only$quoted" \
  shared world domains mesa_sim webui configs &

echo "[web-ui.sh] waiting for the server on port $WEBUI_PORT"
for _ in $(seq 120); do
  curl -s -o /dev/null "http://127.0.0.1:$WEBUI_PORT/api/catalogue" && break
  sleep 0.5
done
(cd "$PAGE" && npm run dev)
