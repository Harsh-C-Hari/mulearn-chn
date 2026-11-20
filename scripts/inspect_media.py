import os
import json
import hashlib
import subprocess
from PIL import Image, ExifTags, ImageStat

SOURCES_DIR = r"D:\mulearn\website\sources\mulearn"
FFPROBE_PATH = r"C:\ffmpeg\bin\ffprobe.exe"
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"

def analyze_all():
    media_files = []
    for root, dirs, files in os.walk(SOURCES_DIR):
        for f in sorted(files):
            if f.endswith('.zip'):
                continue
            full = os.path.join(root, f)
            rel = os.path.relpath(full, SOURCES_DIR).replace('\\', '/')
            ext = os.path.splitext(f)[1].lower()
            size = os.path.getsize(full)
            
            # Sha256
            h = hashlib.sha256()
            with open(full, 'rb') as fp:
                while c := fp.read(65536):
                    h.update(c)
            sha = h.hexdigest()
            
            entry = {
                "relpath": rel,
                "filename": f,
                "folder": os.path.dirname(rel),
                "extension": ext,
                "bytes": size,
                "sha256": sha
            }
            
            if ext in ['.jpg', '.jpeg', '.png', '.webp']:
                with Image.open(full) as img:
                    w, h_px = img.size
                    entry["media_type"] = "image"
                    entry["width"] = w
                    entry["height"] = h_px
                    entry["aspect_ratio"] = round(w / h_px, 3)
                    entry["format"] = img.format
                    entry["mode"] = img.mode
                    
                    # EXIF analysis
                    exif = img.getexif()
                    orientation = 1
                    gps_info = False
                    camera = None
                    date_time = None
                    if exif:
                        orientation = exif.get(0x0112, 1)
                        if 0x8825 in exif:
                            gps_info = True
                        camera = exif.get(0x0110) or exif.get(0x010F)
                        date_time = exif.get(0x0132)
                    
                    try:
                        exif_detailed = img._getexif()
                        if exif_detailed:
                            orientation = exif_detailed.get(0x0112, orientation)
                            if 0x8825 in exif_detailed:
                                gps_info = True
                            if not camera:
                                camera = exif_detailed.get(0x0110) or exif_detailed.get(0x010F)
                            if not date_time:
                                date_time = exif_detailed.get(0x0132) or exif_detailed.get(0x9003)
                    except Exception:
                        pass
                        
                    entry["exif_orientation"] = orientation
                    entry["has_gps"] = gps_info
                    entry["camera"] = str(camera) if camera else None
                    entry["date_time"] = str(date_time) if date_time else None
                    
            elif ext in ['.mp4', '.mov', '.webm']:
                entry["media_type"] = "video"
                cmd = [
                    FFPROBE_PATH, "-v", "quiet", "-print_format", "json",
                    "-show_format", "-show_streams", full
                ]
                res = subprocess.run(cmd, capture_output=True, text=True)
                probe = json.loads(res.stdout) if res.stdout else {}
                v_stream = next((s for s in probe.get("streams", []) if s.get("codec_type") == "video"), {})
                a_stream = next((s for s in probe.get("streams", []) if s.get("codec_type") == "audio"), {})
                fmt = probe.get("format", {})
                
                entry["width"] = int(v_stream.get("width", 0))
                entry["height"] = int(v_stream.get("height", 0))
                entry["aspect_ratio"] = round(entry["width"] / entry["height"], 3) if entry["height"] else 0
                entry["duration"] = round(float(fmt.get("duration", 0)), 2)
                entry["codec"] = v_stream.get("codec_name")
                entry["audio_codec"] = a_stream.get("codec_name") if a_stream else None
                entry["bitrate"] = int(fmt.get("bit_rate", 0))
                
            media_files.append(entry)
            
    print(f"Audited {len(media_files)} non-archive media files.")
    with open(r"D:\mulearn\website\mulearn-chn\scripts\media_audit.json", "w", encoding="utf-8") as f:
        json.dump(media_files, f, indent=2)

if __name__ == '__main__':
    analyze_all()
