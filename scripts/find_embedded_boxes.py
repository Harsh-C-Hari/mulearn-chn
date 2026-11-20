import os
import cv2
import numpy as np
from PIL import Image

SOURCES_DIR = r"D:\mulearn\website\sources\mulearn\Events"
OUT_DIR = r"D:\mulearn\website\mulearn-chn\scripts\embedded_candidates"
os.makedirs(OUT_DIR, exist_ok=True)

targets = [
    # (rel_path, label, approx_box (x, y, w, h) if known or None)
    ("Odessey/Screenshot 2026-11-19 213254.png", "odyssey_wrap_crowd"),
    ("Odessey/Screenshot 2026-11-19 213243.png", "odyssey_winner_sparx"),
    ("Odessey/Screenshot 2026-11-19 213249.png", "odyssey_runnerup_cypher"),
    ("Odessey/Screenshot 2026-11-19 213238.png", "odyssey_runnerup_jijnasus"),
    ("Odessey/Screenshot 2026-11-19 212606.png", "odyssey_session_speaker"),
    ("Buildathon/Screenshot 2026-11-19 213807.png", "buildathon_1st_frustrated_devs"),
    ("Buildathon/Screenshot 2026-11-19 213812.png", "buildathon_2nd_tek_knights"),
    ("Buildathon/Screenshot 2026-11-19 213801.png", "buildathon_3rd_holo"),
    ("build with ai/Screenshot 2026-11-19 214034.png", "bwai_wrap_group"),
    ("build with ai/Screenshot 2026-11-19 214208.png", "bwai_winner_phoenix"),
    ("build with ai/Screenshot 2026-11-19 214200.png", "bwai_creative_amingos"),
    ("build with ai/Screenshot 2026-11-19 214204.png", "bwai_innovative_bizzare"),
    ("Useless Projects/Screenshot 2026-11-19 213837.png", "useless_glimpses_group")
]

def analyze_poster_photo(rel_path, label):
    fp = os.path.join(SOURCES_DIR, rel_path)
    img_cv = cv2.imread(fp)
    if img_cv is None:
        return
    h, w = img_cv.shape[:2]
    
    # Check edges and contours to find photo frame
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []
    for c in contours:
        x, y, cw, ch = cv2.boundingRect(c)
        # We want candidate rectangles that are large enough (e.g. cw >= 350 and ch >= 200, not entire image)
        if cw >= 350 and ch >= 200 and cw < w - 20 and ch < h - 20:
            candidates.append((cw * ch, x, y, cw, ch))
            
    candidates.sort(reverse=True)
    print(f"=== {rel_path} ({w}x{h}) ===")
    if candidates:
        for idx, (area, x, y, cw, ch) in enumerate(candidates[:3]):
            print(f"  Candidate {idx}: box=({x}, {y}, {cw}, {ch}), aspect={cw/ch:.2f}")
            crop = img_cv[y:y+ch, x:x+cw]
            cv2.imwrite(os.path.join(OUT_DIR, f"{label}_c{idx}_{cw}x{ch}.png"), crop)
    else:
        print("  No rectangular contour found by simple edge detection.")

for rel, label in targets:
    analyze_poster_photo(rel, label)
