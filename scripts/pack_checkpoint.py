#!/usr/bin/env python3
"""Create a versioned, complete project ZIP (forward-slash paths, top folder mulearn-chn/).
Usage: python3 scripts/pack_checkpoint.py <zip-name-without-.zip> [outdir]
Never overwrites an existing ZIP of the same name (aborts instead)."""
import sys, os, zipfile
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
name = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(root)
dest = os.path.join(out, name + ".zip")
if os.path.exists(dest): sys.exit(f"REFUSING to overwrite {dest}")
SKIP_DIRS = {"__pycache__", ".git", "node_modules"}
n = 0
with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS)
        for f in sorted(files):
            if f.endswith((".pyc", ".DS_Store")): continue
            full = os.path.join(d, f)
            z.write(full, "mulearn-chn/" + os.path.relpath(full, root).replace(os.sep, "/")); n += 1
with zipfile.ZipFile(dest) as z: assert z.testzip() is None
print(f"{dest}  files={n}  size={os.path.getsize(dest)/1048576:.2f} MB")
