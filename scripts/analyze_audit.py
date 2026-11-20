import json

with open(r'D:\mulearn\website\mulearn-chn\scripts\media_audit.json', 'r', encoding='utf-8') as f:
    files = json.load(f)

print("=== ORIENTATION != 1 ===")
for x in files:
    if x.get('exif_orientation', 1) != 1:
        print(f"{x['relpath']}: orientation={x['exif_orientation']}")

print("\n=== GPS INFO PRESENT ===")
for x in files:
    if x.get('has_gps'):
        print(f"{x['relpath']}: GPS tag present")

print("\n=== LARGEST FILES (> 2MB) ===")
for x in sorted(files, key=lambda i: i['bytes'], reverse=True)[:15]:
    sz_mb = x['bytes'] / 1024 / 1024
    print(f"{x['relpath']}: {sz_mb:.2f} MB, {x.get('width')}x{x.get('height')}")

print("\n=== SMALLEST / LOW-RES IMAGES (width < 600 or height < 600) ===")
for x in [f for f in files if f.get('media_type') == 'image' and (f.get('width', 9999) < 600 or f.get('height', 9999) < 600)]:
    sz_kb = x['bytes'] / 1024
    print(f"{x['relpath']}: {x['width']}x{x['height']}, {sz_kb:.1f} KB")

print("\n=== VIDEOS ===")
for x in [f for f in files if f.get('media_type') == 'video']:
    sz_mb = x['bytes'] / 1024 / 1024
    print(f"{x['relpath']}: {x['width']}x{x['height']}, {x['duration']}s, {sz_mb:.2f} MB, codec={x.get('codec')}, audio={x.get('audio_codec')}")
