"""
extract_embedded.py — Extracts genuine community and event photographs embedded
inside promotional posters and screenshots when resolution is >= 480 px wide.
Original source files remain completely unmodified.
"""

import os
from PIL import Image

SOURCES_DIR = r"D:\mulearn\website\sources\mulearn\Events"
OUT_DIR = r"D:\mulearn\website\mulearn-chn\img\events"

os.makedirs(OUT_DIR, exist_ok=True)

# Target list: (source_rel, out_basename, crop_box (x1, y1, x2, y2), label, event)
EXTRACTIONS = [
    {
        "source": "Odessey/Screenshot 2026-11-19 213254.png",
        "name": "photo-odyssey-wrap",
        "box": (30, 425, 645, 777), # 615 x 352 px
        "label": "ODYSSEY Community Wrap Crowd",
        "event": "ODYSSEY"
    },
    {
        "source": "Odessey/Screenshot 2026-11-19 212606.png",
        "name": "photo-odyssey-stage",
        "box": (0, 0, 507, 332), # 507 x 332 px (full photo frame)
        "label": "ODYSSEY Stage Speaker Session",
        "event": "ODYSSEY"
    },
    {
        "source": "Buildathon/Screenshot 2026-11-19 213807.png",
        "name": "photo-buildathon-podium",
        "box": (84, 380, 605, 692), # 521 x 312 px
        "label": "Buildathon First Place Podium — Frustrated Devs",
        "event": "Buildathon"
    },
    {
        "source": "build with ai/Screenshot 2026-11-19 214034.png",
        "name": "photo-bwai-group",
        "box": (40, 133, 658, 475), # 618 x 342 px
        "label": "Build with AI Participant Group",
        "event": "Build with AI"
    },
    {
        "source": "Useless Projects/Screenshot 2026-11-19 213837.png",
        "name": "photo-useless-glimpses",
        "box": (75, 372, 629, 702), # 554 x 330 px
        "label": "Useless Projects 3.0 Celebratory Evening Group",
        "event": "Useless Projects 3.0"
    }
]

def run_extractions():
    extracted_records = []
    for item in EXTRACTIONS:
        src_path = os.path.join(SOURCES_DIR, item["source"])
        if not os.path.exists(src_path):
            print(f"Warning: {src_path} not found.")
            continue
            
        with Image.open(src_path) as im:
            crop = im.crop(item["box"])
            w, h = crop.size
            
            # Export clean WebP derivative
            out_file = f"{item['name']}.webp"
            out_path = os.path.join(OUT_DIR, out_file)
            crop.save(out_path, "WEBP", quality=85, method=6)
            
            sz = os.path.getsize(out_path)
            record = {
                "id": item["name"],
                "source": item["source"],
                "box": item["box"],
                "width": w,
                "height": h,
                "bytes": sz,
                "label": item["label"],
                "event": item["event"],
                "path": f"img/events/{out_file}"
            }
            extracted_records.append(record)
            print(f"Extracted {out_file}: {w}x{h} ({sz/1024:.1f} KB)")
            
    return extracted_records

if __name__ == "__main__":
    run_extractions()
