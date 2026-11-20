import os
import json
from rapidocr_onnxruntime import RapidOCR

SOURCES_DIR = r"D:\mulearn\website\sources\mulearn\Events"
engine = RapidOCR()

all_ocr = {}
for root, dirs, files in os.walk(SOURCES_DIR):
    for f in sorted(files):
        if f.endswith('.png'):
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, SOURCES_DIR).replace('\\', '/')
            result, _ = engine(fp)
            lines = [r[1] for r in result] if result else []
            all_ocr[rel] = lines

with open(r"D:\mulearn\website\mulearn-chn\scripts\event_ocr_all.json", "w", encoding="utf-8") as out:
    json.dump(all_ocr, out, indent=2)

print("OCR complete for all event images.")
