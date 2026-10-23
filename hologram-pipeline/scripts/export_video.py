#!/usr/bin/env python3
"""Stub for optional sway-animation video export — not built yet.

ffmpeg is not installed on this machine, and this feature was explicitly
lower priority per the original spec, so it's left as a documented stub
rather than a half-working implementation.

Two viable approaches if this gets built later:

  (a) Playwright headless-Chromium, frame-by-frame screenshots + ffmpeg
      encode. Recommended: driven entirely from Python (reuses this venv —
      just `pip install playwright && playwright install chromium`), and
      produces deterministic frame timing since capture isn't tied to real
      wall-clock rendering (each frame: set a fixed `uTime`, screenshot,
      advance). Then shell out to `ffmpeg -framerate N -i frame_%04d.png
      out.mp4`.

  (b) In-browser recording (e.g. CCapture.js) triggered from the GUI or a
      keyboard shortcut. Simpler to wire into the existing viewer, but still
      needs ffmpeg (or a WASM encoder) to turn captured frames into an actual
      video container, and real-time capture is more prone to dropped/uneven
      frames on a slow machine than (a)'s fixed-timestep approach.
"""

from __future__ import annotations

import shutil
import sys


def main() -> None:
    if shutil.which("ffmpeg") is None:
        print(
            "ffmpeg is not installed, so video export isn't available.\n"
            "Install it first, e.g.:\n"
            "  sudo apt-get install ffmpeg\n"
            "Then implement one of the two approaches described in this file's docstring.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(
        "export_video.py is a stub — see the module docstring for the two "
        "recommended implementation approaches. Nothing was recorded.",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
