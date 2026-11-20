import os
import re

for page in ['index.html', 'styleguide.html']:
    with open(page, 'r', encoding='utf-8') as f:
        content = f.read()

    patterns = [
        r'<link[^>]+href=["\']([^"\']+)["\']',
        r'<script[^>]+src=["\']([^"\']+)["\']',
        r'<img[^>]+src=["\']([^"\']+)["\']',
        r'<source[^>]+srcset=["\']([^"\']+)["\']',
        r'<use[^>]+href=["\']([^"\']+)["\']',
    ]

    found_urls = set()
    for pat in patterns:
        for m in re.finditer(pat, content):
            url = m.group(1).strip()
            if url.startswith(('http', '#', 'mailto:', 'tel:', 'data:')):
                continue
            if ',' in url and ' ' in url:
                for part in url.split(','):
                    u = part.strip().split(' ')[0]
                    if u and not u.startswith(('http', '#', 'data:')):
                        found_urls.add(u)
            else:
                found_urls.add(url)

    missing = []
    root_relative = []
    for u in sorted(found_urls):
        if u.startswith('data:'):
            continue
        clean_u = u.split('?')[0].split('#')[0]
        if not clean_u:
            continue
        if clean_u.startswith('/'):
            root_relative.append(clean_u)
            local_p = clean_u.lstrip('/')
        else:
            local_p = clean_u

        if not os.path.exists(local_p):
            missing.append((u, local_p))

    print(f'=== {page}: {len(found_urls)} local asset URLs checked ===')
    print(f'Root-relative count: {len(root_relative)}')
    if missing:
        print(f'MISSING ({len(missing)}):')
        for orig, p in missing:
            print(f'  {orig} -> {p}')
    else:
        print('All referenced assets exist on disk!')

# Audit CSS url() references
css_urls = []
css_missing = []
for root, dirs, files in os.walk('css'):
    for f in files:
        if f.endswith('.css'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8') as c_file:
                content = c_file.read()
            # strip comments
            clean_content = re.sub(r'/\*[\s\S]*?\*/', '', content)
            for m in re.finditer(r'url\(([^)]+)\)', clean_content):
                raw_u = m.group(1).strip('\'"')
                if not raw_u.startswith(('data:', 'http')):
                    css_urls.append((fp, raw_u))
                    css_dir = os.path.dirname(fp)
                    target = os.path.normpath(os.path.join(css_dir, raw_u))
                    if not os.path.exists(target):
                        css_missing.append((fp, raw_u, target))

print(f'\n=== CSS url() references: {len(css_urls)} checked ===')
if css_missing:
    print(f'MISSING ({len(css_missing)}):')
    for fp, u, tgt in css_missing:
        print(f'  {fp}: {u} -> {tgt}')
else:
    print('All CSS url() targets exist on disk!')
