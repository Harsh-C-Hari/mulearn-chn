import os
import json
from PIL import Image

SOURCES_DIR = r"D:\mulearn\website\sources\mulearn"

# Let's inspect every event screenshot in detail
event_folders = ['build with ai', 'Buildathon', 'Odessey', 'Tech forge', 'Type Race', 'Useless Projects', 'Web slingers']

def inspect_event_images():
    results = {}
    for folder in event_folders:
        dirpath = os.path.join(SOURCES_DIR, 'Events', folder)
        if not os.path.exists(dirpath):
            continue
        files = sorted(os.listdir(dirpath))
        results[folder] = []
        for f in files:
            p = os.path.join(dirpath, f)
            if f.endswith('.png'):
                with Image.open(p) as img:
                    w, h = img.size
                    # Check top 40px and bottom 40px, left 30px and right 30px for potential chrome / carousel indicator
                    # Instagram carousel dots usually appear near bottom center (y in [h-40, h-10])
                    # Carousel arrows appear on left/right edges (x near 10-30, y near h/2)
                    results[folder].append({
                        "file": f,
                        "size": f"{w}x{h}",
                        "bytes": os.path.getsize(p)
                    })
            elif f.endswith('.mp4'):
                results[folder].append({
                    "file": f,
                    "type": "video",
                    "bytes": os.path.getsize(p)
                })
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    inspect_event_images()
