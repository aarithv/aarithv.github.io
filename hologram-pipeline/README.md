# Hologram Pipeline

Turns a headshot photo into an interactive 3D, single-color "hologram" of the
head and shoulders: a Python preprocessing + monocular-depth pipeline feeds a
point cloud into a small Three.js viewer with a custom shader (scanlines,
flicker, rim glow, additive blending) and mouse-driven rotation.

This is a standalone tool — it doesn't touch or depend on the sibling Astro
website in any way.

## Quick start

```bash
cd hologram-pipeline
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python make_hologram.py --image /path/to/headshot.jpg --color "#00E5FF"
```

This runs the full pipeline (background removal → head/shoulders crop →
depth estimation → point-cloud export), archives every run's intermediate
files under `output/<image-stem>-<timestamp>/`, copies the final assets into
`viewer/data/`, then starts a local server and opens the viewer in your
browser.

To just re-launch the viewer on the most recent output (e.g. after tweaking
the shader) without rerunning the whole ML pipeline:

```bash
python make_hologram.py --serve-only
```

## CLI options

| Flag | Default | Meaning |
|---|---|---|
| `--image PATH` | — | Input headshot photo (required unless `--serve-only`) |
| `--color "#RRGGBB"` | `#00E5FF` | The hologram's single hue |
| `--max-points N` | `200000` | Point-cloud budget (higher = denser, slower) |
| `--depth-scale F` | `0.6` | Initial depth exaggeration (also live-tunable in the viewer GUI) |
| `--port N` | `8000` | Local server port |
| `--no-browser` | off | Don't auto-open a browser tab |
| `--serve-only` | off | Skip the pipeline, just serve `viewer/` |

## What each stage does

1. **Preprocess** (`pipeline/preprocess.py`) — `rembg` (u2net_human_seg model)
   removes the background for a clean subject mask. A face bounding box (from
   OpenCV's built-in Haar cascade — no extra downloads or API-version risk;
   MediaPipe's newer Tasks API is tried first as an optional enhancement but
   is not required) drives a crop from just above the hairline down to
   roughly the shoulder line. The bottom ~18% of the mask is smoothstep-faded
   to zero so the bust dissolves rather than ending in a hard cut.
2. **Depth** (`pipeline/depth.py`) — a monocular depth model
   (`depth-anything/Depth-Anything-V2-Small-hf`, falling back automatically
   to `Intel/dpt-hybrid-midas` on failure) estimates per-pixel depth, which is
   then masked, normalized, and lightly smoothed with an edge-preserving
   bilateral filter (so the face doesn't look spiky). `mask.png` and
   `depth.png` are saved for inspection.
3. **Geometry** (`pipeline/geometry.py`) — depth + mask + the headshot's own
   luminance become a point cloud (orthographic unprojection, luminance ×
   fade baked into grayscale vertex color), stride-subsampled to the point
   budget, written as a standard binary PLY (`red=green=blue=intensity`) —
   Three.js's stock `PLYLoader` parses this with zero custom code.
4. **Viewer** (`viewer/`) — a plain-HTML/ES-modules Three.js app (no bundler,
   uses a browser import map). Custom shader renders the cloud in one hue
   only (brightness/alpha vary, no other hues), with scrolling scanlines,
   flicker, occasional glitch offset, and rim glow; optional bloom via
   `UnrealBloomPass`. `OrbitControls` are constrained to roughly ±60° azimuth
   and a small polar tilt — this is a single depth layer from one photo, so
   there's no "back" to rotate into. The point cloud also idly sways
   side-to-side on its own, independent of your dragging. A small `lil-gui`
   panel exposes color, point size, scanline density, glow intensity, and
   depth scale live.

## Known environment quirk

`rembg` pulls in `pymatting` → `numba`, which JIT-compiles against the exact
detected host CPU at import time. On some ARM CPU models, `numba`/`llvmlite`'s
bundled LLVM has an incomplete instruction-scheduling model for that specific
core and **crashes the whole Python process** on `import rembg`. The fix —
already baked into `make_hologram.py` (set before any pipeline code is
imported) — is forcing a generic codegen target:

```bash
export NUMBA_CPU_NAME=generic
```

You shouldn't need to set this yourself; it's set automatically at the top of
`make_hologram.py`. If you ever import `pipeline.preprocess` from a different
entrypoint, set this first.

## Notes

- Runs on CPU by default; automatically uses CUDA if `torch.cuda.is_available()`
  (no code changes needed on a GPU machine — `torch` is installed from the
  standard PyPI wheel, not the CPU-only index, so CUDA support is present but
  simply unused here).
- `viewer/vendor/` contains frozen copies of Three.js (core + `examples/jsm`)
  and `lil-gui`, sourced via `scripts/vendor_three.mjs` (re-run it after
  `cd scripts && npm install` to pick up a newer version later). The viewer
  has no npm/build-step dependency at runtime — it's plain static files.
- Video/GIF export of the sway animation is intentionally not built yet
  (`scripts/export_video.py` is a stub) — `ffmpeg` isn't installed on this
  machine. See the comment at the top of that file for the two viable
  approaches if you want to add it later.
