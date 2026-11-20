"""
extract_frames.py — Extracts key video frames using ffmpeg for thumbnails/posters
where stills are otherwise unavailable (e.g. Tech Forge 2.0).
Original source files remain completely unmodified.
"""

import os
import subprocess
from PIL import Image

SOURCES_DIR = r"D:\mulearn\website\sources\mulearn"
OUT_DIR = r"D:\mulearn\website\mulearn-chn\img\events"
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"

os.makedirs(OUT_DIR, exist_ok=True)

FRAMES = [
    {
        "source": "Events/Tech forge/Recording 2026-11-19 212924.mp4",
        "name": "techforge-title",
        "timestamp": "00:00:02.000",
        "label": "Tech Forge 2.0 Animated Title Frame"
    }
]

def run_frame_extractions():
    extracted = []
    for item in FRAMES:
        src = os.path.join(SOURCES_DIR, item["source"])
        if not os.path.exists(src):
            print(f"Warning: {src} not found.")
            continue
            
        temp_png = os.path.join(OUT_DIR, f"{item['name']}_temp.png")
        cmd = [
            FFMPEG_PATH, "-y",
            "-ss", item["timestamp"],
            "-i", src,
            "-vframes", "1",
            "-q:v", "2",
            temp_png
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if os.path.exists(temp_png):
            with Image.open(temp_png) as im:
                w, h = im.size
                out_webp = os.path.join(OUT_DIR, f"{item['name']}.webp")
                im.save(out_webp, "WEBP", quality=85, method=6)
            os.remove(temp_png)
            
            sz = os.path.getsize(out_webp)
            record = {
                "id": item["name"],
                "source": item["source"],
                "timestamp": item["timestamp"],
                "width": w,
                "height": h,
                "bytes": sz,
                "path": f"img/events/{item['name']}.webp"
            }
            extracted.append(record)
            print(f"Extracted video frame {item['name']}.webp: {w}x{h} ({sz/1024:.1f} KB)")
        else:
            print(f"Error extracting frame from {src}: {res.stderr}")
            
    return extracted

if __name__ == "__main__":
    run_frame_extractions()
