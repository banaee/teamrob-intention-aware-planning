"""The team's faces for the opening's team slide: each photo in presentation/photos/ cropped to the face, as a circle,
in grayscale, written to presentation/photos/faces/<name>.png (a transparent corner outside the circle). The photos
themselves are never changed. The centre and the radius of each face, in the photo's own pixels, were read by eye from
the photo (no face detector is installed in the working environment); change them here and run again.

    ~/python-envs/ir-nomesa-env/bin/python presentation/scripts/crop_faces.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

PHOTOS = Path(__file__).resolve().parents[1] / "photos"
SIZE = 512          # the side of each output, in pixels: sharp at the slide's size on a 2560 x 1440 screen

# name: (photo, centre x, centre y, radius), the circle holding the face with a little of the hair.
FACES = {
    "hadi": ("hadi.jpg", 362, 435, 235),
    "franziska": ("Franziska.jpg", 312, 285, 215),
    "stephanie": ("Stephanie.jpg", 306, 112, 100),
    "fatemeh": ("fatemeh_raw.png", 1118, 1790, 880),
}


def face(photo: Path, cx: int, cy: int, r: int) -> Image.Image:
    im = ImageOps.exif_transpose(Image.open(photo)).convert("L")
    box = (cx - r, cy - r, cx + r, cy + r)
    if box[0] < 0 or box[1] < 0 or box[2] > im.width or box[3] > im.height:
        raise SystemExit(f"[crop_faces] the circle of {photo.name} leaves the photo: {box} in {im.size}")
    square = im.crop(box).resize((SIZE, SIZE), Image.LANCZOS)
    mask = Image.new("L", (SIZE * 4, SIZE * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, SIZE * 4 - 1, SIZE * 4 - 1), fill=255)
    out = Image.new("LA", (SIZE, SIZE))
    out.paste(square.convert("LA"), (0, 0), mask.resize((SIZE, SIZE), Image.LANCZOS))
    return out


def main() -> None:
    out_dir = PHOTOS / "faces"
    out_dir.mkdir(exist_ok=True)
    for name, (photo, cx, cy, r) in FACES.items():
        face(PHOTOS / photo, cx, cy, r).save(out_dir / f"{name}.png", optimize=True)
        print(f"[crop_faces] photos/faces/{name}.png from {photo}")


if __name__ == "__main__":
    main()
