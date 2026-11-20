#!/usr/bin/env bash
# Serves the site on localhost, runs the audit, stops the server. Usage: scripts/run_audit.sh [html]
cd "$(dirname "$0")/.."
python3 -m http.server 8765 >/dev/null 2>&1 & SP=$!
sleep 1
AUDIT_URL="http://localhost:8765/${1:-styleguide.html}" AUDIT_OUT="${AUDIT_OUT:-docs/audit-results.json}" python3 scripts/audit_a11y.py "${1:-styleguide.html}" >/tmp/audit.out 2>&1
kill $SP
