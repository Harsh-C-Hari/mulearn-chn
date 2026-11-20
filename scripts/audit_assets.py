import os
import sys
import json
import hashlib
import subprocess
from PIL import Image, ExifTags

SOURCES_DIR = r"D:\mulearn\website\sources\mulearn"
FFPROBE_PATH = r"C:\ffmpeg\bin\ffprobe.exe"

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def probe_video(filepath):
    cmd = [
        FFPROBE_PATH,
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        filepath
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(res.stdout)
        video_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
        audio_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), None)
        format_info = data.get("format", {})
        
        duration = float(format_info.get("duration", 0))
        size = int(format_info.get("size", 0))
        bitrate = int(format_info.get("bit_rate", 0))
        
        width = int(video_stream.get("width", 0)) if video_stream else 0
        height = int(video_stream.get("height", 0)) if video_stream else 0
        codec = video_stream.get("codec_name", "") if video_stream else ""
        fps_eval = video_stream.get("r_frame_rate", "0/1") if video_stream else "0/1"
        try:
            num, den = fps_eval.split("/")
            fps = float(num) / float(den) if float(den) != 0 else 0
        except Exception:
            fps = 0
            
        return {
            "type": "video",
            "width": width,
            "height": height,
            "duration": round(duration, 2),
            "codec": codec,
            "has_audio": audio_stream is not None,
            "fps": round(fps, 2),
            "bitrate": bitrate
        }
    except Exception as e:
        return {"type": "video", "error": str(e)}

def inspect_image(filepath):
    try:
        with Image.open(filepath) as img:
            w, h = img.size
            fmt = img.format
            mode = img.mode
            
            exif_dict = {}
            exif_orientation = 1
            has_gps = False
            
            raw_exif = img.getexif()
            if raw_exif:
                for k, v in raw_exif.items():
                    tag_name = ExifTags.TAGS.get(k, str(k))
                    if tag_name == "Orientation":
                        exif_orientation = v
                    elif tag_name == "GPSInfo":
                        has_gps = True
                    exif_dict[tag_name] = str(v)
            
            # Check for _getexif() if available (e.g. for JPEG)
            try:
                detailed_exif = img._getexif()
                if detailed_exif:
                    for k, v in detailed_exif.items():
                        tag_name = ExifTags.TAGS.get(k, str(k))
                        if tag_name == "Orientation":
                            exif_orientation = v
                        elif tag_name == "GPSInfo":
                            has_gps = True
                        if tag_name not in exif_dict:
                            exif_dict[tag_name] = str(v)
            except Exception:
                pass
                
            return {
                "type": "image",
                "width": w,
                "height": h,
                "format": fmt,
                "mode": mode,
                "exif_orientation": exif_orientation,
                "has_gps": has_gps,
                "exif_tags": list(exif_dict.keys())
            }
    except Exception as e:
        return {"type": "image", "error": str(e)}

def main():
    records = []
    for root, dirs, files in os.walk(SOURCES_DIR):
        for file in sorted(files):
            fullpath = os.path.join(root, file)
            relpath = os.path.relpath(fullpath, SOURCES_DIR).replace("\\", "/")
            filesize = os.path.getsize(fullpath)
            sha256 = get_sha256(fullpath)
            
            ext = os.path.splitext(file)[1].lower()
            if ext in [".jpg", ".jpeg", ".png", ".webp"]:
                info = inspect_image(fullpath)
            elif ext in [".mp4", ".mov", ".webm"]:
                info = probe_video(fullpath)
            elif ext in [".zip"]:
                info = {"type": "archive"}
            else:
                info = {"type": "other"}
                
            record = {
                "relpath": relpath,
                "filename": file,
                "bytes": filesize,
                "sha256": sha256,
                **info
            }
            records.append(record)
            
    print(f"Total files audited: {len(records)}")
    out_json = r"D:\mulearn\website\mulearn-chn\scripts\audit_raw.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
    print(f"Saved audit to {out_json}")

if __name__ == "__main__":
    main()
