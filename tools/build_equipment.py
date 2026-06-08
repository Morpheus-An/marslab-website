#!/usr/bin/env python3
"""Normalize lab equipment shots into uniform premium 'studio' cards.

Each robot is trimmed to content, scaled with consistent padding, and centered
on a square canvas with a subtle vertical gradient backdrop -> a clean, catalog
-style lineup. Output: public/equipment/<slug>.jpg (1000x1000).
"""
import os
import numpy as np
from PIL import Image, ImageChops

SRC = "/tmp/hw/unzipped/ppt/media"
OUT = "/Users/lijingliang/Desktop/marslab-website/public/equipment"
os.makedirs(OUT, exist_ok=True)
SIZE = 1000
PAD = 0.11               # padding fraction on each side
TOP = (252, 252, 251)    # backdrop gradient top
BOT = (236, 236, 234)    # backdrop gradient bottom

MAP = {
    "unitree-g1":    "image7.png",
    "rokae-humanx":  "image6.png",
    "galaxea-r1":    "image1.png",
    "franka-panda":  "image3.png",
    "ur5e":          "image2.png",
    "ufactory-xarm": "image8.png",
    "sharpa-wave":   "image5.png",
}


def content_bbox(im):
    """Bounding box of the robot, handling transparent OR white backgrounds."""
    alpha = im.split()[-1]
    if alpha.getextrema()[0] < 250:           # has real transparency
        return im.getbbox()
    rgb = im.convert("RGB")
    bg = Image.new("RGB", rgb.size, (255, 255, 255))
    diff = ImageChops.difference(rgb, bg)
    diff = ImageChops.add(diff, diff, 2.0, -12)  # amplify, drop near-white noise
    return diff.getbbox()


def gradient_canvas():
    g = np.linspace(0, 1, SIZE)[:, None, None]
    top = np.array(TOP).reshape(1, 1, 3)
    bot = np.array(BOT).reshape(1, 1, 3)
    col = (top + (bot - top) * g).astype("uint8")     # SIZE x 1 x 3
    arr = np.repeat(col, SIZE, axis=1)                 # SIZE x SIZE x 3
    return Image.fromarray(arr, "RGB")


def process(slug, fn):
    im = Image.open(os.path.join(SRC, fn)).convert("RGBA")
    bb = content_bbox(im)
    if bb:
        im = im.crop(bb)
    avail = int(SIZE * (1 - 2 * PAD))
    w, h = im.size
    s = min(avail / w, avail / h)
    im = im.resize((max(1, round(w * s)), max(1, round(h * s))), Image.LANCZOS)
    canvas = gradient_canvas()
    x = (SIZE - im.size[0]) // 2
    y = (SIZE - im.size[1]) // 2
    canvas.paste(im, (x, y), im)
    canvas.save(os.path.join(OUT, slug + ".jpg"), "JPEG", quality=92)
    print(f"OK {slug:14s} <- {fn}  ({im.size[0]}x{im.size[1]} on {SIZE})")


def main():
    crops = []
    for slug, fn in MAP.items():
        process(slug, fn)
        crops.append(slug)
    # contact sheet for review
    cols = 4
    cell = 250
    rows = (len(crops) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * cell), "#cccccc")
    for i, slug in enumerate(crops):
        t = Image.open(os.path.join(OUT, slug + ".jpg")).resize((cell - 8, cell - 8))
        r, c = divmod(i, cols)
        sheet.paste(t, (c * cell + 4, r * cell + 4))
    sheet.save("/tmp/hw/equip_contact.png")
    print("contact -> /tmp/hw/equip_contact.png")


if __name__ == "__main__":
    main()
