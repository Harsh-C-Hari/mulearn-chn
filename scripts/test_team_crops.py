import os
import cv2
import numpy as np
from PIL import Image, ImageOps

TEAM_DIR = r"D:\mulearn\website\sources\mulearn\Team"
OUT_TEST = r"D:\mulearn\website\mulearn-chn\scripts\team_crops_test"
os.makedirs(OUT_TEST, exist_ok=True)

# Face detector using cv2 DNN or cascade with downscaled image for robustness
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

def get_crop_box(w, h, fx, fy, fw, fh, target_ratio=3.0/3.6):
    # target_ratio = width / height = 0.8333
    # center around face center
    fc_x = fx + fw / 2.0
    fc_y = fy + fh / 2.0
    
    # We want the face to occupy roughly 35-45% of the portrait height
    crop_h = fh / 0.40
    crop_w = crop_h * target_ratio
    
    # If crop exceeds image bounds, adjust
    if crop_w > w:
        crop_w = w
        crop_h = crop_w / target_ratio
    if crop_h > h:
        crop_h = h
        crop_w = crop_h * target_ratio
        
    x1 = fc_x - crop_w / 2.0
    y1 = fc_y - crop_h * 0.42 # place face slightly above vertical center
    
    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0
    if x1 + crop_w > w:
        x1 = w - crop_w
    if y1 + crop_h > h:
        y1 = h - crop_h
        
    return int(round(x1)), int(round(y1)), int(round(crop_w)), int(round(crop_h))

results = {}
for f in sorted(os.listdir(TEAM_DIR)):
    if f.endswith(('.jpg', '.png', '.webp')):
        fp = os.path.join(TEAM_DIR, f)
        pil_img = Image.open(fp)
        pil_img = ImageOps.exif_transpose(pil_img)
        w, h = pil_img.size
        
        # Downscale for face detection
        scale = 800.0 / max(w, h) if max(w, h) > 800 else 1.0
        small = pil_img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
        cv_img = cv2.cvtColor(np.array(small.convert('RGB')), cv2.COLOR_RGB2GRAY)
        
        # If exif rotated
        if '18_Al_Ameen' in f:
            cv_img = cv2.rotate(cv2.imread(fp), cv2.ROTATE_90_CLOCKWISE)
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            if scale != 1.0:
                cv_img = cv2.resize(cv_img, (int(w * scale), int(h * scale)))
                
        faces = face_cascade.detectMultiScale(cv_img, 1.1, 4, minSize=(30, 30))
        if len(faces) > 0:
            # Pick the largest face
            faces = sorted(faces, key=lambda b: b[2] * b[3], reverse=True)
            fx, fy, fw, fh = [int(v / scale) for v in faces[0]]
            # check sanity: face center should be within image upper 70%
            if (fy + fh/2) > h * 0.75:
                # fallback
                fx, fy, fw, fh = int(w*0.25), int(h*0.15), int(w*0.5), int(w*0.5)
        else:
            fx, fy, fw, fh = int(w*0.25), int(h*0.15), int(w*0.5), int(w*0.5)
            
        bx, by, bw, bh = get_crop_box(w, h, fx, fy, fw, fh)
        crop = pil_img.crop((bx, by, bx + bw, by + bh))
        crop_thumb = crop.resize((300, 360), Image.Resampling.LANCZOS)
        
        out_name = f.split('__')[0] + '.webp'
        crop_thumb.save(os.path.join(OUT_TEST, out_name), 'WEBP', quality=85)
        results[f] = {
            "source_size": [w, h],
            "crop_box": [bx, by, bw, bh],
            "crop_aspect": round(bw / bh, 3)
        }
        print(f"Cropped {f[:25]}: box=({bx}, {by}, {bw}, {bh}) => 300x360")
