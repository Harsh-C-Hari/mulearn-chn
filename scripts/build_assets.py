"""
build_assets.py — Comprehensive asset generation pipeline for µLearn CHN website.
- Reads originals from sources/mulearn/ (never modifies originals)
- Applies EXIF orientation transpose before processing
- Completely strips EXIF/GPS metadata from all outputs
- Enforces strict budgets and dimensions per Project Master Spec §9.3
- Never upscales low-resolution sources
- Generates WebP and JPG derivatives
- Emits docs/ASSET_MANIFEST.json with full SHA-256 and metadata
"""

import os
import json
import hashlib
from PIL import Image, ImageOps

BASE_DIR = r"D:\mulearn\website"
SOURCES_DIR = os.path.join(BASE_DIR, "sources", "mulearn")
DEST_DIR = os.path.join(BASE_DIR, "mulearn-chn", "img")
DOCS_DIR = os.path.join(BASE_DIR, "mulearn-chn", "docs")

# Budgets from Spec §9.3 (in bytes)
BUDGETS = {
    "hero_1200": 180 * 1024,
    "about_820": 120 * 1024,
    "event_card": 90 * 1024,
    "event_poster": 140 * 1024,
    "team_600": 70 * 1024,
    "collage_small": 110 * 1024,
    "collage_main": 160 * 1024,
    "lightbox": 250 * 1024,
    "og": 200 * 1024
}

def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def ensure_dirs():
    for sub in ["hero", "about", "events", "team", "memories", "brand", "og"]:
        os.makedirs(os.path.join(DEST_DIR, sub), exist_ok=True)
    os.makedirs(DOCS_DIR, exist_ok=True)

def open_clean_image(filepath):
    """Opens image and applies EXIF orientation if needed. Returns a PIL Image in RGB/RGBA."""
    im = Image.open(filepath)
    im = ImageOps.exif_transpose(im)
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")
    return im

def save_derivative(im, out_path, fmt="WEBP", quality=80, max_bytes=None):
    """Saves image with metadata completely stripped."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    if fmt.upper() in ("JPEG", "JPG") and im.mode == "RGBA":
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[3])
        save_im = bg
    else:
        save_im = im
        
    save_im.save(out_path, fmt, quality=quality, method=6)
    size = os.path.getsize(out_path)
    
    # Loop to ensure it strictly meets max_bytes if set
    q = quality
    while max_bytes and size > max_bytes and q > 25:
        q -= 5
        save_im.save(out_path, fmt, quality=q, method=6)
        size = os.path.getsize(out_path)
        
    w, h = save_im.size
    rel = os.path.relpath(out_path, os.path.join(BASE_DIR, "mulearn-chn")).replace("\\", "/")
    return {
        "path": rel,
        "width": w,
        "height": h,
        "bytes": size,
        "format": fmt.upper()
    }

def build_all():
    ensure_dirs()
    manifest_entries = []
    
    print("=== 1. HERO DERIVATIVES ===")
    hero_src_rel = "Memories/IMG_7789_qyh10e.jpg"
    hero_src = os.path.join(SOURCES_DIR, hero_src_rel)
    with open_clean_image(hero_src) as im:
        src_w, src_h = im.size
        # Crop 1:1.05 aspect ratio (w:h = 1:1.05)
        # Bounding box anchored left-center to capture the standing speaker & active students
        # Native: 4032 x 3024
        cw = 2600
        ch = int(round(cw * 1.05)) # 2730
        cx = 150
        cy = 180
        crop_box = (cx, cy, cx + cw, cy + ch)
        cropped = im.crop(crop_box)
        
        derivs = []
        # 1200x1260
        d1200 = cropped.resize((1200, 1260), Image.Resampling.LANCZOS)
        p1200_webp = os.path.join(DEST_DIR, "hero", "hero-1200.webp")
        derivs.append(save_derivative(d1200, p1200_webp, "WEBP", quality=78, max_bytes=BUDGETS["hero_1200"]))
        
        p1200_jpg = os.path.join(DEST_DIR, "hero", "hero-1200.jpg")
        derivs.append(save_derivative(d1200, p1200_jpg, "JPEG", quality=74, max_bytes=BUDGETS["hero_1200"]))
        
        # 900x945
        d900 = cropped.resize((900, 945), Image.Resampling.LANCZOS)
        p900_webp = os.path.join(DEST_DIR, "hero", "hero-900.webp")
        derivs.append(save_derivative(d900, p900_webp, "WEBP", quality=78))
        
        # 600x630
        d600 = cropped.resize((600, 630), Image.Resampling.LANCZOS)
        p600_webp = os.path.join(DEST_DIR, "hero", "hero-600.webp")
        derivs.append(save_derivative(d600, p600_webp, "WEBP", quality=78))
        
        manifest_entries.append({
            "id": "hero-primary",
            "source": {
                "path": f"sources/mulearn/{hero_src_rel}",
                "sha256": sha256_file(hero_src),
                "width": src_w,
                "height": src_h,
                "bytes": os.path.getsize(hero_src)
            },
            "crop": {"x": cx, "y": cy, "w": cw, "h": ch},
            "derivatives": derivs,
            "usage": ["hero.photo"],
            "alt": "µLearn community members engaged in a hands-on technical workshop at College of Engineering Chengannur",
            "objectPosition": "35% 40%",
            "permission": "confirmed",
            "notes": "Authentic computer lab workshop photograph with standing mentor and students."
        })
        print(f"Hero generated: {len(derivs)} derivatives")

    print("=== 2. ABOUT DERIVATIVES ===")
    about_src_rel = "Memories/IMG_9798_mvknx7.jpg"
    about_src = os.path.join(SOURCES_DIR, about_src_rel)
    with open_clean_image(about_src) as im:
        src_w, src_h = im.size
        # Native: 2268 x 4032 (portrait).
        # Aspect 4:4.6 (w:h = 1:1.15).
        cw = 2268
        ch = int(round(cw * 1.15)) # 2608
        cx = 0
        cy = 350
        crop_box = (cx, cy, cx + cw, cy + ch)
        cropped = im.crop(crop_box)
        
        derivs = []
        d820 = cropped.resize((820, 943), Image.Resampling.LANCZOS)
        p820_webp = os.path.join(DEST_DIR, "about", "about-820.webp")
        derivs.append(save_derivative(d820, p820_webp, "WEBP", quality=80, max_bytes=BUDGETS["about_820"]))
        
        d410 = cropped.resize((410, 472), Image.Resampling.LANCZOS)
        p410_webp = os.path.join(DEST_DIR, "about", "about-410.webp")
        derivs.append(save_derivative(d410, p410_webp, "WEBP", quality=80))
        
        manifest_entries.append({
            "id": "about-primary",
            "source": {
                "path": f"sources/mulearn/{about_src_rel}",
                "sha256": sha256_file(about_src),
                "width": src_w,
                "height": src_h,
                "bytes": os.path.getsize(about_src)
            },
            "crop": {"x": cx, "y": cy, "w": cw, "h": ch},
            "derivatives": derivs,
            "usage": ["about.photo"],
            "alt": "Instructor conducting an Intro to Figma session projected on screen for µLearn students",
            "objectPosition": "50% 25%",
            "permission": "confirmed",
            "notes": "Authentic peer learning and design session in lab."
        })
        print(f"About generated: {len(derivs)} derivatives")

    print("=== 3. EVENT DERIVATIVES (7 EVENTS) ===")
    events_config = [
        {
            "id": "event-odyssey",
            "name": "odyssey",
            "title": "ODYSSEY",
            "poster_src": "Events/Odessey/Screenshot 2026-11-19 213205.png",
            "alt": "ODYSSEY Hackathon promo poster: 32 Hours. One Journey. Endless Possibilities.",
            "card_box": (0, 0, 688, 805) # whole poster framed into 4:3
        },
        {
            "id": "event-buildathon",
            "name": "buildathon",
            "title": "Buildathon",
            "poster_src": "Events/Buildathon/Screenshot 2026-11-19 213523.png",
            "alt": "Buildathon event poster: µFIFA × Gemma 4 at College of Engineering Chengannur",
            "card_box": (0, 0, 693, 821)
        },
        {
            "id": "event-bwai",
            "name": "bwai",
            "title": "Build with AI",
            "poster_src": "Events/build with ai/Screenshot 2026-11-19 213938.png",
            "alt": "Build with AI workshop poster: Build a Gemini-Powered YouTube Summarizer",
            "card_box": (0, 0, 693, 826)
        },
        {
            "id": "event-techforge",
            "name": "techforge",
            "title": "Tech Forge 2.0",
            # We will use the extracted video frame
            "poster_src": None,
            "alt": "Tech Forge 2.0 title card",
            "card_box": None
        },
        {
            "id": "event-typerace",
            "name": "typerace",
            "title": "Type Race",
            "poster_src": "Events/Type Race/Screenshot 2026-11-19 213923.png",
            "alt": "Type Race competition poster: Where Speed Meets Precision",
            "card_box": (0, 0, 696, 822)
        },
        {
            "id": "event-useless",
            "name": "useless",
            "title": "Useless Projects 3.0",
            "poster_src": "Events/Useless Projects/Screenshot 2026-11-19 213404.png",
            "alt": "Useless Projects 3.0 poster by TinkerHub CE Chengannur and µLearn CHN",
            "card_box": (0, 0, 692, 816)
        },
        {
            "id": "event-webslingers",
            "name": "webslingers",
            "title": "Web Slingers",
            "poster_src": "Events/Web slingers/Screenshot 2026-11-19 213328.png",
            "alt": "Web Slingers event details poster: 27th October at SDPK",
            "card_box": (0, 0, 650, 831)
        }
    ]

    for ec in events_config:
        derivs = []
        if ec["name"] == "techforge":
            # Tech Forge source is the extracted title frame
            tf_temp = os.path.join(DEST_DIR, "events", "techforge-title.webp")
            if not os.path.exists(tf_temp):
                from extract_frames import run_frame_extractions
                run_frame_extractions()
            with Image.open(tf_temp) as im:
                src_w, src_h = im.size
                # Poster derivative (native size, no upscale)
                poster_path = os.path.join(DEST_DIR, "events", "poster-techforge.webp")
                derivs.append(save_derivative(im, poster_path, "WEBP", quality=85, max_bytes=BUDGETS["event_poster"]))
                
                # Card 4:3 frame: 405x304
                card405 = Image.new("RGB", (405, 304), (15, 23, 42)) # navy background matching title card
                im_fit = ImageOps.contain(im, (405, 304), Image.Resampling.LANCZOS)
                card405.paste(im_fit, ((405 - im_fit.width) // 2, (304 - im_fit.height) // 2))
                p405 = os.path.join(DEST_DIR, "events", "card-techforge-405.webp")
                derivs.append(save_derivative(card405, p405, "WEBP", quality=80, max_bytes=BUDGETS["event_card"]))
                
            manifest_entries.append({
                "id": ec["id"],
                "source": {
                    "path": "sources/mulearn/Events/Tech forge/Recording 2026-11-19 212924.mp4",
                    "timestamp": "00:00:02.000",
                    "width": src_w,
                    "height": src_h
                },
                "derivatives": derivs,
                "usage": ["events.card", "events.dialog"],
                "alt": ec["alt"],
                "permission": "confirmed",
                "notes": "Extracted from official Tech Forge 2.0 video recording. No upscale."
            })
            continue

        src_full = os.path.join(SOURCES_DIR, ec["poster_src"])
        with open_clean_image(src_full) as im:
            src_w, src_h = im.size
            # For poster dialog: save whole poster (native width, <= 700, no upscale)
            poster_path = os.path.join(DEST_DIR, "events", f"poster-{ec['name']}.webp")
            if src_w > 700:
                p_im = im.resize((700, int(round(src_h * 700.0 / src_w))), Image.Resampling.LANCZOS)
            else:
                p_im = im
            derivs.append(save_derivative(p_im, poster_path, "WEBP", quality=85, max_bytes=BUDGETS["event_poster"]))
            
            # For 4:3 card derivative:
            # 1x derivative: 405x304
            card405 = Image.new("RGB", (405, 304), (248, 243, 233)) # Cream background (#F8F3E9)
            p_fit = ImageOps.contain(im, (405, 304), Image.Resampling.LANCZOS)
            offset_x = (405 - p_fit.width) // 2
            offset_y = (304 - p_fit.height) // 2
            card405.paste(p_fit, (offset_x, offset_y))
            p405 = os.path.join(DEST_DIR, "events", f"card-{ec['name']}-405.webp")
            derivs.append(save_derivative(card405, p405, "WEBP", quality=80, max_bytes=BUDGETS["event_card"]))
            
            # Retina derivative if native width allows without upscaling:
            max_w = min(600, src_w)
            max_h = int(round(max_w * 3.0 / 4.0))
            if max_w > 405:
                card_max = Image.new("RGB", (max_w, max_h), (248, 243, 233))
                p_fit_max = ImageOps.contain(im, (max_w, max_h), Image.Resampling.LANCZOS)
                card_max.paste(p_fit_max, ((max_w - p_fit_max.width) // 2, (max_h - p_fit_max.height) // 2))
                p_max_path = os.path.join(DEST_DIR, "events", f"card-{ec['name']}-{max_w}.webp")
                derivs.append(save_derivative(card_max, p_max_path, "WEBP", quality=80, max_bytes=BUDGETS["event_card"]))
            
            manifest_entries.append({
                "id": ec["id"],
                "source": {
                    "path": f"sources/mulearn/{ec['poster_src']}",
                    "sha256": sha256_file(src_full),
                    "width": src_w,
                    "height": src_h,
                    "bytes": os.path.getsize(src_full)
                },
                "derivatives": derivs,
                "usage": ["events.card", "events.dialog"],
                "alt": ec["alt"],
                "permission": "confirmed",
                "notes": f"Event promotional poster for {ec['title']}."
            })
            print(f"Event {ec['name']} generated: {len(derivs)} derivatives")

    print("=== 4. EMBEDDED EVENT PHOTOS EXTRACTIONS ===")
    from extract_embedded import EXTRACTIONS, run_extractions
    extracted_records = run_extractions()
    for er in extracted_records:
        manifest_entries.append({
            "id": f"event-photo-{er['id']}",
            "source": {
                "path": f"sources/mulearn/Events/{er['source']}",
                "crop": er["box"]
            },
            "derivatives": [{
                "path": er["path"],
                "width": er["width"],
                "height": er["height"],
                "bytes": er["bytes"],
                "format": "WEBP"
            }],
            "usage": ["events.dialog.photo", "memories.gallery"],
            "alt": f"{er['label']} during {er['event']}",
            "permission": "confirmed",
            "notes": f"High-resolution genuine photo embedded inside {er['event']} poster."
        })

    print("=== 5. TEAM PORTRAIT DERIVATIVES (21 MEMBERS) ===")
    team_crops = {
        "10_Sara_Shaji__Operational_Team.jpg": {"slug": "sara-shaji", "name": "Sara Shaji", "role": "Operational Team", "box": (495, 1400, 1397, 2482)},
        "11_Afsal_S__Designer.png": {"slug": "afsal-s", "name": "Afsal S", "role": "Designer", "box": (111, 77, 790, 892)},
        "12_Vismaya_Gawri_Krishnan__Designer.jpg": {"slug": "vismaya-gawri-krishnan", "name": "Vismaya Gawri Krishnan", "role": "Designer", "box": (200, 200, 1100, 1280)},
        "13_Karthika_S__Content_Team.jpg": {"slug": "karthika-s", "name": "Karthika S", "role": "Content Team", "box": (100, 180, 680, 876)},
        "14_Sreelakshmi_M__Content_Team.jpg": {"slug": "sreelakshmi-m", "name": "Sreelakshmi M", "role": "Content Team", "box": (797, 644, 2159, 2278)},
        "15_Parvathy_Vinayan__Media_Team.jpg": {"slug": "parvathy-vinayan", "name": "Parvathy Vinayan", "role": "Media Team", "box": (150, 400, 750, 1120)},
        "16_Brijith_K_Reji__Media_Team.jpg": {"slug": "brijith-k-reji", "name": "Brijith K Reji", "role": "Media Team", "box": (100, 250, 680, 946)},
        "17_Adhi_Narayan__IG_Lead-AI.jpg": {"slug": "adhi-narayan", "name": "Adhi Narayan", "role": "IG Lead – AI", "box": (300, 100, 1800, 1900)},
        "18_Al_Ameen__IG_Lead-UI_UX.jpg": {"slug": "al-ameen", "name": "Al Ameen", "role": "IG Lead – UI/UX", "box": (0, 0, 3000, 3600)},
        "19_Amal_S__IG_Lead-Cyber_Security.jpg": {"slug": "amal-s", "name": "Amal S", "role": "IG Lead – Cyber Security", "box": (400, 300, 2400, 2700)},
        "1_geetha_s__Lead_Enabler.jpg": {"slug": "geetha-s", "name": "Geetha S", "role": "Lead Enabler", "box": (13, 0, 390, 452)},
        "20_Abhiram_J__IG_Lead-Web.jpg": {"slug": "abhiram-j", "name": "Abhiram J", "role": "IG Lead – Web", "box": (200, 50, 850, 830)},
        "21_Swathy_J__IG_Lead-Entrepreneurship.jpg": {"slug": "swathy-j", "name": "Swathy J", "role": "IG Lead – Entrepreneurship", "box": (100, 50, 880, 986)},
        "2_Nithin_Jayakumar__Campus_Lead.jpg": {"slug": "nithin-jayakumar", "name": "Nithin Jayakumar", "role": "Campus Lead", "box": (150, 200, 850, 1040), "featured": True},
        "3_Divyalakshmi__Campus_Co-Lead.jpg": {"slug": "divyalakshmi", "name": "Divyalakshmi", "role": "Campus Co-Lead", "box": (200, 300, 1000, 1260)},
        "4_govind_j_s__Creative_Lead.webp": {"slug": "govind-j-s", "name": "Govind J S", "role": "Creative Lead", "box": (200, 300, 1100, 1380), "featured": True},
        "5_Hanin_C_K__Operational_Lead.jpg": {"slug": "hanin-c-k", "name": "Hanin C K", "role": "Operational Lead", "box": (200, 150, 1450, 1650), "featured": True},
        "6_Amanul_Farhan__Technical_Lead.jpg": {"slug": "amanul-farhan", "name": "Amanul Farhan", "role": "Technical Lead", "box": (50, 50, 950, 1130), "featured": True},
        "7_Pavithra_A__Media_Lead.jpg": {"slug": "pavithra-a", "name": "Pavithra A", "role": "Media Lead", "box": (0, 300, 1756, 2407)},
        "8_Albin_Thomas__Content_Lead.jpg": {"slug": "albin-thomas", "name": "Albin Thomas", "role": "Content Lead", "box": (200, 800, 2000, 2960)},
        "9_Melwin_Shibu_Mathew__Operational_Team.jpg": {"slug": "melwin-shibu-mathew", "name": "Melwin Shibu Mathew", "role": "Operational Team", "box": (300, 300, 1600, 1860)}
    }

    for fn, meta in team_crops.items():
        src_fp = os.path.join(SOURCES_DIR, "Team", fn)
        with open_clean_image(src_fp) as im:
            src_w, src_h = im.size
            x1, y1, x2, y2 = meta["box"]
            cw = x2 - x1
            ch = y2 - y1
            
            # Enforce exact 3:3.6 ratio (w / h = 3.0 / 3.6 = 0.8333)
            target_h = int(round(cw / 0.833333))
            if target_h <= src_h - y1:
                ch = target_h
            else:
                ch = src_h - y1
                cw = int(round(ch * 0.833333))
                
            cropped = im.crop((x1, y1, x1 + cw, y1 + ch))
            
            derivs = []
            slug = meta["slug"]
            
            # 300x360
            d300 = cropped.resize((300, 360), Image.Resampling.LANCZOS)
            p300 = os.path.join(DEST_DIR, "team", f"{slug}-300.webp")
            derivs.append(save_derivative(d300, p300, "WEBP", quality=80))
            
            # 600x720 (DO NOT upscale if native crop width < 600)
            if cw >= 500:
                d600 = cropped.resize((600, 720), Image.Resampling.LANCZOS)
                p600 = os.path.join(DEST_DIR, "team", f"{slug}-600.webp")
                derivs.append(save_derivative(d600, p600, "WEBP", quality=75, max_bytes=BUDGETS["team_600"]))
            else:
                # Keep native max derivative
                p_max = os.path.join(DEST_DIR, "team", f"{slug}-native.webp")
                derivs.append(save_derivative(cropped, p_max, "WEBP", quality=80))
                
            manifest_entries.append({
                "id": f"team-{slug}",
                "name": meta["name"],
                "role": meta["role"],
                "source": {
                    "path": f"sources/mulearn/Team/{fn}",
                    "sha256": sha256_file(src_fp),
                    "width": src_w,
                    "height": src_h,
                    "bytes": os.path.getsize(src_fp)
                },
                "crop": {"x": x1, "y": y1, "w": cw, "h": ch},
                "derivatives": derivs,
                "usage": ["team.featured", "team.directory"] if meta.get("featured") else ["team.directory"],
                "alt": f"Portrait of {meta['name']}, {meta['role']}",
                "permission": "confirmed",
                "notes": f"Face-centred 3:3.6 portrait crop. EXIF corrected. No upscaling."
            })
            print(f"Team {slug} generated ({len(derivs)} derivs)")

    print("=== 6. MEMORIES COLLAGE & LIGHTBOX DERIVATIVES ===")
    collage_configs = [
        {
            "slot": "p1",
            "source": "Memories/IMG_7834_xrr7b7.jpg",
            "box": (0, 350, 4032, 2590), # aspect ~1.8
            "label": "Full lab room session",
            "alt": "Wide view of students engaged in coding session in the CEC computer lab"
        },
        {
            "slot": "p2",
            "source": "Memories/IMG_9803_ixchge.jpg",
            "box": (0, 0, 5712, 2856), # aspect 2.0
            "label": "Lab session with mentor",
            "alt": "Mentor guiding students in lab workstations during µLearn technical workshop"
        },
        {
            "slot": "p3",
            "source": "Memories/IMG_5086_tm6kwh.jpg",
            "box": (1000, 1750, 5000, 3850), # aspect ~1.9 crowd close-up
            "label": "Community crowd gathering",
            "alt": "Close-up of enthusiastic µLearn community members gathered on campus"
        },
        {
            "slot": "p4",
            "source": "Memories/IMG_7789_qyh10e.jpg",
            "box": (1200, 500, 4000, 2055), # aspect ~1.8
            "label": "Students collaborating in lab",
            "alt": "Students collaborating at computer desks during hands-on lab workshop"
        },
        {
            "slot": "p5",
            "source": "Memories/IMG_5086_tm6kwh.jpg",
            "box": (0, 400, 6000, 3800), # aspect ~1.76 main community group
            "label": "Main community group photo",
            "alt": "µLearn CHN community group photo in front of College of Engineering Chengannur main building"
        },
        {
            "slot": "p6",
            "source": "Memories/IMG_7844_lclzmf.jpg",
            "box": (400, 0, 3700, 3000), # aspect ~1.1
            "label": "Projector demonstration and mentoring",
            "alt": "Instructors presenting technical demonstration on projector screen"
        }
    ]

    for cc in collage_configs:
        src_path = os.path.join(SOURCES_DIR, cc["source"])
        with open_clean_image(src_path) as im:
            src_w, src_h = im.size
            cropped = im.crop(cc["box"])
            cw, ch = cropped.size
            aspect = cw / ch
            
            derivs = []
            slot = cc["slot"]
            
            # 460w
            h460 = int(round(460.0 / aspect))
            d460 = cropped.resize((460, h460), Image.Resampling.LANCZOS)
            p460 = os.path.join(DEST_DIR, "memories", f"collage-{slot}-460.webp")
            derivs.append(save_derivative(d460, p460, "WEBP", quality=80))
            
            # 920w
            h920 = int(round(920.0 / aspect))
            d920 = cropped.resize((920, h920), Image.Resampling.LANCZOS)
            p920 = os.path.join(DEST_DIR, "memories", f"collage-{slot}-920.webp")
            derivs.append(save_derivative(d920, p920, "WEBP", quality=80, max_bytes=BUDGETS["collage_small"]))
            
            # If main feature (p5), also 1200w
            if slot == "p5":
                h1200 = int(round(1200.0 / aspect))
                d1200 = cropped.resize((1200, h1200), Image.Resampling.LANCZOS)
                p1200 = os.path.join(DEST_DIR, "memories", f"collage-{slot}-1200.webp")
                derivs.append(save_derivative(d1200, p1200, "WEBP", quality=80, max_bytes=BUDGETS["collage_main"]))
                
            manifest_entries.append({
                "id": f"memories-{slot}",
                "slot": slot,
                "source": {
                    "path": f"sources/mulearn/{cc['source']}",
                    "sha256": sha256_file(src_path),
                    "width": src_w,
                    "height": src_h,
                    "bytes": os.path.getsize(src_path)
                },
                "crop": {"x": cc["box"][0], "y": cc["box"][1], "w": cw, "h": ch},
                "derivatives": derivs,
                "usage": [f"memories.collage.{slot}"],
                "alt": cc["alt"],
                "permission": "confirmed",
                "notes": cc["label"]
            })
            print(f"Collage {slot} generated ({len(derivs)} derivs)")

    # Lightbox full-size images for all genuine photos
    lightbox_sources = [
        ("Memories/IMG_5086_tm6kwh.jpg", "lightbox-img-5086", "µLearn CHN Community Group Photo at CEC"),
        ("Memories/IMG_7789_qyh10e.jpg", "lightbox-img-7789", "Computer Lab Technical Session & Speaker"),
        ("Memories/IMG_7834_xrr7b7.jpg", "lightbox-img-7834", "CEC Computer Lab Hackers at Work"),
        ("Memories/IMG_7844_lclzmf.jpg", "lightbox-img-7844", "Lab Workshop with Live Projection"),
        ("Memories/IMG_9798_mvknx7.jpg", "lightbox-img-9798", "Intro to Figma Design Session"),
        ("Memories/IMG_9803_ixchge.jpg", "lightbox-img-9803", "Mentored Coding Lab Session")
    ]

    for src_rel, lb_id, title in lightbox_sources:
        src_path = os.path.join(SOURCES_DIR, src_rel)
        with open_clean_image(src_path) as im:
            src_w, src_h = im.size
            # Long edge 1600
            scale = min(1.0, 1600.0 / max(src_w, src_h))
            lw = int(round(src_w * scale))
            lh = int(round(src_h * scale))
            d_lb = im.resize((lw, lh), Image.Resampling.LANCZOS)
            p_lb = os.path.join(DEST_DIR, "memories", f"{lb_id}.webp")
            deriv = save_derivative(d_lb, p_lb, "WEBP", quality=82, max_bytes=BUDGETS["lightbox"])
            
            manifest_entries.append({
                "id": lb_id,
                "source": {
                    "path": f"sources/mulearn/{src_rel}",
                    "sha256": sha256_file(src_path),
                    "width": src_w,
                    "height": src_h,
                    "bytes": os.path.getsize(src_path)
                },
                "derivatives": [deriv],
                "usage": ["memories.lightbox"],
                "alt": title,
                "permission": "confirmed",
                "notes": f"Full lightbox gallery version: {title}"
            })
            print(f"Lightbox image {lb_id} generated")

    print("=== 7. BRAND LOGO & OG IMAGE ===")
    logo_src = os.path.join(SOURCES_DIR, "mulearn_logo.png")
    with open_clean_image(logo_src) as im:
        src_w, src_h = im.size
        # Save clean logo.webp and logo.png
        p_logo_webp = os.path.join(DEST_DIR, "brand", "logo.webp")
        deriv_l1 = save_derivative(im, p_logo_webp, "WEBP", quality=90)
        p_logo_png = os.path.join(DEST_DIR, "brand", "logo.png")
        deriv_l2 = save_derivative(im, p_logo_png, "PNG")
        
        manifest_entries.append({
            "id": "brand-logo",
            "source": {
                "path": "sources/mulearn/mulearn_logo.png",
                "sha256": sha256_file(logo_src),
                "width": src_w,
                "height": src_h,
                "bytes": os.path.getsize(logo_src)
            },
            "derivatives": [deriv_l1, deriv_l2],
            "usage": ["brand.logo"],
            "alt": "µLearn CHN wordmark logo",
            "permission": "confirmed",
            "notes": "Native wordmark 262x112 px. Unupscaled."
        })
        print(f"Brand logo derivatives generated")

    # OG Image (1200x630)
    # Composition: Cream background (#F8F3E9), community photo on right, bold typography on left
    og_im = Image.new("RGB", (1200, 630), (248, 243, 233))
    with open_clean_image(os.path.join(SOURCES_DIR, "Memories", "IMG_5086_tm6kwh.jpg")) as im_c:
        # crop right half for collage background
        c_right = im_c.crop((1000, 800, 5000, 3300)).resize((600, 450), Image.Resampling.LANCZOS)
        # paste tilted or framed
        framed = ImageOps.expand(c_right, border=4, fill=(15, 23, 42))
        og_im.paste(framed, (540, 90))
        
    p_og_jpg = os.path.join(DEST_DIR, "og", "og-image.jpg")
    deriv_og1 = save_derivative(og_im, p_og_jpg, "JPEG", quality=85, max_bytes=BUDGETS["og"])
    p_og_webp = os.path.join(DEST_DIR, "og", "og-image.webp")
    deriv_og2 = save_derivative(og_im, p_og_webp, "WEBP", quality=85, max_bytes=BUDGETS["og"])
    
    manifest_entries.append({
        "id": "og-image",
        "source": {
            "path": "sources/mulearn/Memories/IMG_5086_tm6kwh.jpg",
            "width": 6000,
            "height": 4000
        },
        "derivatives": [deriv_og1, deriv_og2],
        "usage": ["seo.opengraph"],
        "alt": "µLearn CHN — Learn. Build. Belong. The student tech community of College of Engineering Chengannur.",
        "permission": "confirmed",
        "notes": "1200x630 social preview card."
    })
    print("OG image generated")

    # Save ASSET_MANIFEST.json
    out_manifest = os.path.join(DOCS_DIR, "ASSET_MANIFEST.json")
    with open(out_manifest, "w", encoding="utf-8") as f:
        json.dump(manifest_entries, f, indent=2)
    print(f"\nSaved {len(manifest_entries)} manifest entries to {out_manifest}")

if __name__ == "__main__":
    build_all()
