"""Stage 2: monocular depth estimation, masked normalization, smoothing."""

from __future__ import annotations

import numpy as np
from PIL import Image

from . import config


def _run_depth_pipeline(model_id: str, image_rgb: np.ndarray):
    import torch
    from transformers import pipeline

    device = 0 if torch.cuda.is_available() else -1
    depth_pipe = pipeline("depth-estimation", model=model_id, device=device)
    result = depth_pipe(Image.fromarray(image_rgb))

    # Different transformers versions have used slightly different result
    # keys for this pipeline; handle both defensively.
    depth_img = result.get("depth", None)
    if depth_img is None:
        depth_img = result.get("predicted_depth", None)
    if depth_img is None:
        raise RuntimeError(f"Unexpected depth-estimation pipeline output keys: {list(result.keys())}")

    if hasattr(depth_img, "convert"):
        depth = np.array(depth_img.convert("F"), dtype=np.float32)
    else:
        depth = np.array(depth_img, dtype=np.float32)
        if depth.ndim > 2:
            depth = depth.squeeze()
    return depth


def estimate_depth(image_rgb: np.ndarray) -> tuple[np.ndarray, str]:
    """Returns (depth, model_used). Tries the primary model, falls back to
    the MiDaS-based model on any failure."""
    try:
        depth = _run_depth_pipeline(config.DEPTH_MODEL_PRIMARY, image_rgb)
        return depth, config.DEPTH_MODEL_PRIMARY
    except Exception as exc:
        print(f"Primary depth model failed ({exc!r}), falling back to MiDaS...")
        depth = _run_depth_pipeline(config.DEPTH_MODEL_FALLBACK, image_rgb)
        return depth, config.DEPTH_MODEL_FALLBACK


def process_depth(depth: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Resize depth to the mask's resolution if needed, normalize over the
    masked region only, smooth with an edge-preserving bilateral filter."""
    import cv2

    if depth.shape != mask.shape:
        depth = cv2.resize(depth, (mask.shape[1], mask.shape[0]), interpolation=cv2.INTER_LINEAR)

    valid = mask > 0.05
    if valid.any():
        d_min = depth[valid].min()
        d_max = depth[valid].max()
    else:
        d_min, d_max = depth.min(), depth.max()

    span = max(d_max - d_min, 1e-6)
    normalized = np.clip((depth - d_min) / span, 0.0, 1.0)
    normalized = np.where(valid, normalized, 0.0)

    depth_u8 = (normalized * 255).astype(np.uint8)
    smoothed_u8 = cv2.bilateralFilter(
        depth_u8,
        d=config.BILATERAL_D,
        sigmaColor=config.BILATERAL_SIGMA_COLOR,
        sigmaSpace=config.BILATERAL_SIGMA_SPACE,
    )
    smoothed = smoothed_u8.astype(np.float32) / 255.0
    smoothed = np.where(valid, smoothed, 0.0)
    return smoothed
