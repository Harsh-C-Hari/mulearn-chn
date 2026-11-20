import os
import json
import numpy as np
from PIL import Image

SOURCES_DIR = r"D:\mulearn\website\sources\mulearn\Events"

targets = [
    # Odyssey
    ("Odessey/Screenshot 2026-11-19 213254.png", "odyssey_wrap_crowd"),
    ("Odessey/Screenshot 2026-11-19 213243.png", "odyssey_winner_sparx"),
    ("Odessey/Screenshot 2026-11-19 213249.png", "odyssey_runnerup_cypher"),
    ("Odessey/Screenshot 2026-11-19 213238.png", "odyssey_runnerup_jijnasus"),
    ("Odessey/Screenshot 2026-11-19 212606.png", "odyssey_session_speaker"),
    # Buildathon
    ("Buildathon/Screenshot 2026-11-19 213807.png", "buildathon_1st_frustrated_devs"),
    ("Buildathon/Screenshot 2026-11-19 213812.png", "buildathon_2nd_tek_knights"),
    ("Buildathon/Screenshot 2026-11-19 213801.png", "buildathon_3rd_holo"),
    # Build with AI
    ("build with ai/Screenshot 2026-11-19 214034.png", "bwai_wrap_group"),
    ("build with ai/Screenshot 2026-11-19 214208.png", "bwai_winner_phoenix"),
    ("build with ai/Screenshot 2026-11-19 214200.png", "bwai_creative_amingos"),
    ("build with ai/Screenshot 2026-11-19 214204.png", "bwai_innovative_bizzare"),
    # Useless Projects
    ("Useless Projects/Screenshot 2026-11-19 213837.png", "useless_glimpses_group")
]

results = []
for rel, label in targets:
    p = os.path.join(SOURCES_DIR, rel)
    if not os.path.exists(p):
        continue
    with Image.open(p) as img:
        w, h = img.size
        # To find photo bounds, let's look at image brightness/color variance across horizontal and vertical slices
        # Most posters have a solid or textured graphic background with a central rectangular photograph
        arr = np.array(img.convert('RGB'))
        # Row-wise standard deviation of colors
        row_std = np.std(arr, axis=(1, 2))
        col_std = np.std(arr, axis=(0, 2))
        results.append({
            "rel": rel,
            "label": label,
            "width": w,
            "height": h
        })

print(json.dumps(results, indent=2))
