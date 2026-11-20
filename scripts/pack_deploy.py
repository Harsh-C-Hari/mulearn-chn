#!/usr/bin/env python3
"""Build the DEPLOYABLE website package (no docs, scripts, reference boards or source assets).
Usage: python3 scripts/pack_deploy.py <zip-name-without-.zip> [outdir]. Never overwrites."""
import sys,os,zipfile
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
name=sys.argv[1];out=sys.argv[2] if len(sys.argv)>2 else os.path.dirname(root)
dest=os.path.join(out,name+'.zip')
if os.path.exists(dest): sys.exit('REFUSING to overwrite '+dest)
EXCLUDE_TOP={'docs','scripts','reference','sources','README.md'}
n=0
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for d,dirs,files in os.walk(root):
        rel=os.path.relpath(d,root)
        if rel=='.': dirs[:]=sorted(x for x in dirs if x not in EXCLUDE_TOP and x!='__pycache__')
        for f in sorted(files):
            if rel=='.' and f in EXCLUDE_TOP: continue
            if f.endswith(('.pyc','.DS_Store')): continue
            full=os.path.join(d,f);z.write(full,os.path.relpath(full,root).replace(os.sep,'/'));n+=1
with zipfile.ZipFile(dest) as z: assert z.testzip() is None
print(f'{dest} files={n} size={os.path.getsize(dest)/1048576:.2f} MB')
