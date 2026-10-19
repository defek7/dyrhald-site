"""Dyrhald website - turn a game screenshot into web-sized images in Website/img.

    python Website/tools/add_shot.py <screenshot.png> <name> [--crop L,T,R,B] [--width 1600]

Writes img/<name>.webp at the given width (keeps the aspect) and img/<name>-sm.webp at half that,
so pages can load the small one on phones. --crop takes a box in the original's pixels, e.g. to cut the HUD off:
--crop 380,70,1660,930 on a 1920x1080 shot. Needs Pillow (pip install pillow).
"""
import argparse, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(os.path.dirname(HERE), "img")

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("name")
ap.add_argument("--crop")
ap.add_argument("--width", type=int, default=1600)
ap.add_argument("--quality", type=int, default=78)
a = ap.parse_args()

im = Image.open(a.src).convert("RGB")
if a.crop:
    im = im.crop(tuple(int(v) for v in a.crop.split(",")))
os.makedirs(IMG, exist_ok=True)
for suffix, w in (("", a.width), ("-sm", a.width // 2)):
    w = min(w, im.width)
    out = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    path = os.path.join(IMG, a.name + suffix + ".webp")
    out.save(path, "WEBP", quality=a.quality, method=6)
    print(f"{path}  {out.width}x{out.height}  {os.path.getsize(path) // 1024} KB")
