"""Stage 3: depth + mask + luminance -> point cloud -> binary PLY.

PLY schema (binary_little_endian): float x, y, z + uchar red, green, blue,
with red == green == blue == baked intensity (luminance * bottom-fade). This
is a completely standard PLY that Three.js's stock PLYLoader parses with zero
custom code — it hard-codes a 3-component red/green/blue -> `color` vertex
attribute mapping. Because the viewer renders with additive blending on a
dark background, a low grayscale value already reads as "faded/transparent".
"""

from __future__ import annotations

import math

import numpy as np

from . import config


def _luminance(rgb: np.ndarray) -> np.ndarray:
    r = rgb[:, :, 0].astype(np.float32)
    g = rgb[:, :, 1].astype(np.float32)
    b = rgb[:, :, 2].astype(np.float32)
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0


def build_point_cloud(
    cropped_rgb: np.ndarray,
    mask: np.ndarray,
    depth: np.ndarray,
    max_points: int = config.MAX_POINTS,
    depth_scale: float = config.DEFAULT_DEPTH_SCALE,
) -> dict:
    h, w = mask.shape
    luminance = _luminance(cropped_rgb)
    intensity = luminance * mask

    valid = mask > 0.02
    valid_count = int(valid.sum())
    stride = max(1, math.ceil(math.sqrt(valid_count / max(max_points, 1))))

    ys, xs = np.nonzero(valid)
    keep = (ys % stride == 0) & (xs % stride == 0)
    ys, xs = ys[keep], xs[keep]

    u = xs.astype(np.float32)
    v = ys.astype(np.float32)
    d = depth[ys, xs]
    inten = intensity[ys, xs]

    x = (u - w / 2.0) / config.SCALE_XY
    y = -(v - h / 2.0) / config.SCALE_XY
    z = (d - 0.5) * depth_scale

    positions = np.stack([x, y, z], axis=1).astype(np.float32)
    colors = np.clip(inten * 255.0, 0, 255).astype(np.uint8)
    colors_rgb = np.stack([colors, colors, colors], axis=1)

    return {
        "positions": positions,
        "colors": colors_rgb,
        "count": positions.shape[0],
        "stride": stride,
    }


def write_ply(path: str, positions: np.ndarray, colors: np.ndarray) -> None:
    n = positions.shape[0]
    header = (
        "ply\n"
        "format binary_little_endian 1.0\n"
        "comment hologram-pipeline output\n"
        f"element vertex {n}\n"
        "property float x\n"
        "property float y\n"
        "property float z\n"
        "property uchar red\n"
        "property uchar green\n"
        "property uchar blue\n"
        "end_header\n"
    )

    vertex_dtype = np.dtype(
        [("x", "<f4"), ("y", "<f4"), ("z", "<f4"), ("red", "u1"), ("green", "u1"), ("blue", "u1")]
    )
    vertices = np.empty(n, dtype=vertex_dtype)
    vertices["x"] = positions[:, 0]
    vertices["y"] = positions[:, 1]
    vertices["z"] = positions[:, 2]
    vertices["red"] = colors[:, 0]
    vertices["green"] = colors[:, 1]
    vertices["blue"] = colors[:, 2]

    with open(path, "wb") as f:
        f.write(header.encode("ascii"))
        f.write(vertices.tobytes())
