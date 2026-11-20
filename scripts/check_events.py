import os
import glob
from PIL import Image

EVENTS_DIR = r"D:\mulearn\website\sources\mulearn\Events"

def check_events():
    for root, dirs, files in os.walk(EVENTS_DIR):
        for f in sorted(files):
            if f.endswith('.png'):
                p = os.path.join(root, f)
                rel = os.path.relpath(p, EVENTS_DIR).replace('\\', '/')
                with Image.open(p) as im:
                    w, h = im.size
                    # Check edges for carousel arrows (often white circles or chevron arrows in middle-left or middle-right)
                    # Let's inspect pixel brightness/variations at edge regions (e.g. x in [0, 40] and [w-40, w], y around h/2)
                    print(f"{rel}: {w}x{h}")

if __name__ == '__main__':
    check_events()
