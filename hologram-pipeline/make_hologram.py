#!/usr/bin/env python3
"""One-command CLI: headshot photo -> head-and-shoulders 3D hologram viewer.

Usage:
    python make_hologram.py --image headshot.jpg --color "#00E5FF"
    python make_hologram.py --serve-only   # just re-launch the viewer server
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

# rembg pulls in pymatting -> numba, which JIT-compiles against the exact
# detected host CPU. On some ARM CPU models numba/llvmlite's bundled LLVM has
# an incomplete scheduling model and crashes the whole process on import.
# Forcing a generic codegen target sidesteps it; must be set before numba
# (or anything importing it) is ever imported in this process.
os.environ.setdefault("NUMBA_CPU_NAME", "generic")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def parse_args() -> argparse.Namespace:
    from pipeline import config

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", help="Path to the input headshot photo")
    parser.add_argument("--color", default=config.DEFAULT_COLOR, help="Single hologram hue, e.g. #00E5FF")
    parser.add_argument("--max-points", type=int, default=config.MAX_POINTS)
    parser.add_argument("--depth-scale", type=float, default=config.DEFAULT_DEPTH_SCALE)
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-browser", action="store_true", help="Don't auto-open a browser tab")
    parser.add_argument("--serve-only", action="store_true", help="Skip the pipeline, just serve viewer/")
    return parser.parse_args()


def run_pipeline(args: argparse.Namespace) -> Path:
    from pipeline import config, depth as depth_stage, geometry, preprocess
    from pipeline.utils import StepLogger, check_dependencies

    check_dependencies()

    from PIL import Image

    image_path = Path(args.image).resolve()
    if not image_path.exists():
        print(f"Image not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    stem = image_path.stem
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    run_dir = HERE / "output" / f"{stem}-{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    log = StepLogger()

    log.step(f"Input: {image_path}")
    shutil.copy(image_path, run_dir / "input.jpg")

    log.step("Stage 1/3: removing background + cropping to head/shoulders...")
    pre = preprocess.preprocess(str(image_path))
    Image.fromarray(pre["cropped_rgb"]).save(run_dir / "cropped.jpg", quality=92)
    Image.fromarray((pre["mask"] * 255).astype("uint8")).save(run_dir / "mask.png")
    log.step(f"  face bbox={pre['face_bbox']}  crop box={pre['crop_box']}")

    log.step("Stage 2/3: estimating depth...")
    raw_depth, model_used = depth_stage.estimate_depth(pre["cropped_rgb"])
    log.step(f"  depth model used: {model_used}")
    processed_depth = depth_stage.process_depth(raw_depth, pre["mask"])
    Image.fromarray((processed_depth * 255).astype("uint8")).save(run_dir / "depth.png")

    log.step("Stage 3/3: building point cloud + writing PLY...")
    cloud = geometry.build_point_cloud(
        pre["cropped_rgb"],
        pre["mask"],
        processed_depth,
        max_points=args.max_points,
        depth_scale=args.depth_scale,
    )
    ply_path = run_dir / "points.ply"
    geometry.write_ply(str(ply_path), cloud["positions"], cloud["colors"])
    log.step(f"  wrote {cloud['count']} points (stride={cloud['stride']}) -> {ply_path.name}")

    meta = {
        "color": args.color,
        "depthScale": args.depth_scale,
        "pointCount": cloud["count"],
        "depthModel": model_used,
        "sourceImage": image_path.name,
        "generatedAt": timestamp,
    }
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2))
    log.write(run_dir / "run.log")

    # Copy this run's outputs into viewer/data/, which is what the viewer
    # loads by default.
    data_dir = HERE / "viewer" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    for name in ("mask.png", "depth.png", "points.ply", "meta.json"):
        shutil.copy(run_dir / name, data_dir / name)

    log.step(f"Run archived at {run_dir}")
    return run_dir


def main() -> None:
    args = parse_args()

    if not args.serve_only:
        if not args.image:
            print("--image is required (or pass --serve-only to just relaunch the viewer)", file=sys.stderr)
            sys.exit(1)
        run_pipeline(args)

    from pipeline.server import serve

    serve(str(HERE / "viewer"), port=args.port, open_browser=not args.no_browser)


if __name__ == "__main__":
    main()
