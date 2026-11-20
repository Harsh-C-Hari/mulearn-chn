#!/usr/bin/env bash
# Usage: scripts/checkpoint.sh <name>   e.g. mulearn-chn_phase-04_subphase-01
# Builds full + deploy ZIPs (never overwrites), extracts both fresh, verifies, prints a summary.
set -e
N="$1"; ROOT="$(cd "$(dirname "$0")/.." && pwd)"; OUT="${OUT:-$(dirname "$ROOT")/../out}"; mkdir -p "$OUT"; OUT="$(cd "$OUT" && pwd)"
DEP="${2:-${N}_deploy}"
python3 "$ROOT/scripts/pack_checkpoint.py" "$N" "$OUT"
python3 "$ROOT/scripts/pack_deploy.py" "$DEP" "$OUT"
for Z in "$N" "$DEP"; do rm -rf "/tmp/x_$Z"; mkdir "/tmp/x_$Z"; unzip -q "$OUT/$Z.zip" -d "/tmp/x_$Z"; done
F="/tmp/x_$N/mulearn-chn"; D="/tmp/x_$DEP"
echo "FULL: $(find "$F" -type f | wc -l) files; has docs=$([ -d $F/docs ] && echo y) scripts=$([ -d $F/scripts ] && echo y) reference=$([ -d $F/reference ] && echo y) index=$([ -f $F/index.html ] && echo y)"
echo "DEPLOY: $(find "$D" -type f | wc -l) files; index=$([ -f $D/index.html ] && echo y) docs=$([ -d $D/docs ] && echo LEAK || echo none) scripts=$([ -d $D/scripts ] && echo LEAK || echo none) reference=$([ -d $D/reference ] && echo LEAK || echo none) sources=$([ -d $D/sources ] && echo LEAK || echo none)"
# every local ref in deployable index.html must exist there
python3 - "$D" <<'PY'
import re,sys,os
d=sys.argv[1]; h=open(d+'/index.html',encoding='utf-8').read()
refs=set(re.findall(r'(?:src|href)="((?:css|js|data|img|fonts|vendor)/[^"#?]+)"',h))
for m in re.findall(r'srcset="([^"]+)"',h):
    for part in m.split(','): refs.add(part.strip().split(' ')[0])
miss=[r for r in refs if not os.path.exists(os.path.join(d,r))]
print('deploy local refs:',len(refs),'missing:',miss)
PY
ls -la "$OUT/$N.zip" "$OUT/$DEP.zip"
