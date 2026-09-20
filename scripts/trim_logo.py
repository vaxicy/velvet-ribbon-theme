"""Build logo/logo128.png from the source artwork.

Two outputs:
  logo/logo128.png                     white rounded plate + artwork (+ soft shadow)
  store-assets/icon-candidates/logo-plain-128.png   bare artwork, transparent outside

The outer white page of the source is removed with a corner flood fill so white
details INSIDE the artwork (sparkle, cream wave) survive.
"""
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "logo" / "logo source.png"
if not SRC.exists():
    SRC = ROOT / "store-assets" / "icon-candidates" / "logo-source.png"
DST = ROOT / "logo" / "logo128.png"
PLAIN = ROOT / "store-assets" / "icon-candidates" / "logo-plain-128.png"

KEY = (255, 0, 255)
N = 1024                    # working canvas
PLATE = 0.86                # plate side as a fraction of the canvas
PLATE_R = 0.25              # corner radius as a fraction of the plate side
ART = 0.75                  # artwork size as a fraction of the plate side
SHADOW = (57, 29, 58, 40)   # soft plum shadow
SHADOW_BLUR = 26
SHADOW_DY = 18


def cut_artwork():
    im = Image.open(SRC).convert("RGB")
    w, h = im.size
    for corner in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        ImageDraw.floodfill(im, corner, KEY, thresh=42)
    alpha = Image.new("L", (w, h), 255)
    px, ap = im.load(), alpha.load()
    for y in range(h):
        for x in range(w):
            if px[x, y] == KEY:
                ap[x, y] = 0
    alpha = alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(0.5))
    art = im.convert("RGBA")
    art.putalpha(alpha)
    return art.crop(alpha.point(lambda p: 255 if p > 8 else 0).getbbox())


def main():
    art = cut_artwork()

    canvas = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    side = int(N * PLATE)
    r = int(side * PLATE_R)
    box = [(N - side) // 2, (N - side) // 2, (N + side) // 2, (N + side) // 2]

    # soft shadow
    shadow = Image.new("L", (N, N), 0)
    ImageDraw.Draw(shadow).rounded_rectangle(box, radius=r, fill=255)
    shadow = shadow.filter(ImageFilter.GaussianBlur(SHADOW_BLUR))
    layer = Image.new("RGBA", (N, N), SHADOW)
    layer.putalpha(shadow.point(lambda p: p * SHADOW[3] // 255))
    canvas.alpha_composite(layer, (0, SHADOW_DY))

    # white plate
    plate = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    ImageDraw.Draw(plate).rounded_rectangle(box, radius=r, fill=(255, 255, 255, 255))
    canvas.alpha_composite(plate)

    # artwork centred on the plate
    a = int(side * ART)
    art = art.resize((a, a), Image.LANCZOS)
    canvas.alpha_composite(art, ((N - a) // 2, (N - a) // 2))

    canvas.resize((128, 128), Image.LANCZOS).save(DST)
    canvas.resize((512, 512), Image.LANCZOS).save(
        ROOT / "store-assets" / "icon-candidates" / "logo-preview-512.png")

    # bare version for reference
    b = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
    bare = art.resize((900, 900), Image.LANCZOS)
    b.alpha_composite(bare, (62, 62))
    b.resize((128, 128), Image.LANCZOS).save(PLAIN)
    print("logo128.png written (plate), plain copy written")


if __name__ == "__main__":
    main()
