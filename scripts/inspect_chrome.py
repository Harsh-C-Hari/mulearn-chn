import os
from PIL import Image

SOURCES_DIR = r"D:\mulearn\website\sources\mulearn\Events"

files_with_chrome = [
    "Buildathon/Screenshot 2026-11-19 213523.png",
    "Buildathon/Screenshot 2026-11-19 213607.png",
    "Odessey/Screenshot 2026-11-19 213205.png",
    "Odessey/Screenshot 2026-11-19 213254.png",
    "Useless Projects/Screenshot 2026-11-19 213414.png",
    "Useless Projects/Screenshot 2026-11-19 213837.png",
    "Useless Projects/Screenshot 2026-11-19 213851.png"
]

for rel in files_with_chrome:
    fp = os.path.join(SOURCES_DIR, rel)
    with Image.open(fp) as im:
        w, h = im.size
        print(f"{rel}: size={w}x{h}")
