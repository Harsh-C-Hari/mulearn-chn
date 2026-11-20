import os
import zipfile
import shutil

BASE_DIR = r"D:\mulearn\website"
SOURCE_FOLDER = os.path.join(BASE_DIR, "mulearn-chn")
TARGET_ZIP = os.path.join(BASE_DIR, "mulearn-chn.zip")
PHASE_DIR = os.path.join(BASE_DIR, "phase")
PHASE1_ZIP = os.path.join(PHASE_DIR, "mulearn-chn_phase_1.zip")
PHASE1_SPEC_ZIP = os.path.join(PHASE_DIR, "mulearn-chn_phase-01_20261120.zip")

os.makedirs(PHASE_DIR, exist_ok=True)

# Temporary directory / exclusions
EXCLUDE_PATTERNS = ["__pycache__", ".git", ".DS_Store", "Thumbs.db"]

def should_exclude(relpath):
    parts = relpath.replace("\\", "/").split("/")
    for p in parts:
        if p in EXCLUDE_PATTERNS or p.endswith(".pyc"):
            return True
    return False

def create_bundle(dest_path):
    print(f"Creating {dest_path}...")
    file_count = 0
    total_uncompressed = 0
    with zipfile.ZipFile(dest_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        # Add root dir entry
        zf.writestr("mulearn-chn/", "")
        for root, dirs, files in os.walk(SOURCE_FOLDER):
            # Sort for deterministic zip
            dirs.sort()
            files.sort()
            for d in dirs:
                full_d = os.path.join(root, d)
                rel_d = os.path.relpath(full_d, BASE_DIR).replace("\\", "/") + "/"
                if not should_exclude(rel_d):
                    zf.writestr(rel_d, "")
            for f in files:
                full_f = os.path.join(root, f)
                rel_f = os.path.relpath(full_f, BASE_DIR).replace("\\", "/")
                if not should_exclude(rel_f):
                    zf.write(full_f, rel_f)
                    file_count += 1
                    total_uncompressed += os.path.getsize(full_f)
                    
    zip_size = os.path.getsize(dest_path)
    print(f"Packed {file_count} files ({total_uncompressed / 1024 / 1024:.2f} MB uncompressed) -> {dest_path} ({zip_size / 1024 / 1024:.2f} MB)")
    return file_count, zip_size

# 1. Create root mulearn-chn.zip
create_bundle(TARGET_ZIP)

# 2. Create phase/mulearn-chn_phase_1.zip
shutil.copyfile(TARGET_ZIP, PHASE1_ZIP)
print(f"Copied to {PHASE1_ZIP}")

# 3. Create phase/mulearn-chn_phase-01_20261120.zip (spec-compliant name)
shutil.copyfile(TARGET_ZIP, PHASE1_SPEC_ZIP)
print(f"Copied to {PHASE1_SPEC_ZIP}")
