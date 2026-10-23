"""Stage 1: background removal, head+shoulders crop, bottom-edge mask fade."""

from __future__ import annotations

import io

import numpy as np
from PIL import Image

from . import config
from .face_detect import detect_face_bbox


def remove_background(image_rgb: np.ndarray) -> np.ndarray:
    """Return an RGBA uint8 array; alpha is the clean subject mask."""
    from rembg import remove, new_session

    session = new_session(config.REMBG_MODEL)
    pil_img = Image.fromarray(image_rgb)
    buf = io.BytesIO()
    pil_img.save(buf, format="PNG")
    result_bytes = remove(buf.getvalue(), session=session)
    result = Image.open(io.BytesIO(result_bytes)).convert("RGBA")
    return np.array(result)


def compute_crop_box(
    face_bbox: tuple[int, int, int, int],
    mask_bbox: tuple[int, int, int, int] | None,
    image_size: tuple[int, int],
) -> tuple[int, int, int, int]:
    """(left, top, right, bottom) crop box: from above the hairline down to
    roughly the shoulder line, centered on the face and intersected with the
    subject mask's own bounding box so we never crop into background-only
    regions."""
    x, y, w, h = face_bbox
    img_w, img_h = image_size

    top = y - config.HEADROOM_FACTOR * h
    bottom = y + h + config.SHOULDER_DROP_FACTOR * h
    cx = x + w / 2
    half_width = (w * config.SIDE_MARGIN_FACTOR) / 2
    left = cx - half_width
    right = cx + half_width

    if mask_bbox is not None:
        mx0, my0, mx1, my1 = mask_bbox
        left = max(left, mx0)
        right = min(right, mx1)
        top = max(top, my0)
        bottom = min(bottom, my1)

    left = max(0, int(left))
    top = max(0, int(top))
    right = min(img_w, int(right))
    bottom = min(img_h, int(bottom))
    return (left, top, right, bottom)


def fade_bottom_edge(mask: np.ndarray) -> np.ndarray:
    """Multiply the bottom FADE_BAND_FRACTION of the mask by a smoothstep
    gradient from 1.0 down to 0.0, so the bust dissolves into light instead
    of ending in a hard cut."""
    h = mask.shape[0]
    band = int(h * config.FADE_BAND_FRACTION)
    if band <= 0:
        return mask

    fade = np.ones(h, dtype=np.float32)
    fade_start = h - band
    t = np.linspace(0.0, 1.0, band, dtype=np.float32)
    smoothstep = t * t * (3 - 2 * t)
    fade[fade_start:] = 1.0 - smoothstep

    return mask * fade[:, None]


def preprocess(image_path: str) -> dict:
    """Run the full preprocessing stage.

    Returns a dict with:
      cropped_rgb: uint8 HxWx3
      mask: float32 HxW in [0, 1] (background-removed + bottom-faded)
    """
    pil_img = Image.open(image_path).convert("RGB")
    image_rgb = np.array(pil_img)

    rgba = remove_background(image_rgb)
    alpha = rgba[:, :, 3].astype(np.float32) / 255.0

    ys, xs = np.nonzero(alpha > 0.1)
    mask_bbox = (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())) if len(xs) else None

    face_bbox = detect_face_bbox(image_rgb)
    crop_box = compute_crop_box(face_bbox, mask_bbox, (image_rgb.shape[1], image_rgb.shape[0]))
    left, top, right, bottom = crop_box

    cropped_rgb = image_rgb[top:bottom, left:right]
    cropped_alpha = alpha[top:bottom, left:right]
    faded_mask = fade_bottom_edge(cropped_alpha)

    return {
        "cropped_rgb": cropped_rgb,
        "mask": faded_mask,
        "face_bbox": face_bbox,
        "crop_box": crop_box,
    }
