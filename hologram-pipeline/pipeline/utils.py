"""Small shared helpers: logging and image IO."""

from __future__ import annotations

import sys
import time


class StepLogger:
    """Tiny helper that prints a timestamped, timed line per pipeline step and
    also collects the same lines into a list for writing to run.log."""

    def __init__(self) -> None:
        self.lines: list[str] = []
        self._start = time.time()

    def _emit(self, msg: str) -> None:
        elapsed = time.time() - self._start
        line = f"[{elapsed:7.2f}s] {msg}"
        print(line, file=sys.stderr)
        self.lines.append(line)

    def step(self, msg: str) -> None:
        self._emit(msg)

    def write(self, path) -> None:
        with open(path, "w") as f:
            f.write("\n".join(self.lines) + "\n")


def check_dependencies() -> None:
    """Friendly upfront import check so a missing package prints a clear
    `pip install` line instead of a raw traceback deep in some module."""
    missing = []
    checks = [
        ("numpy", "numpy"),
        ("PIL", "pillow"),
        ("cv2", "opencv-python-headless"),
        ("onnxruntime", "onnxruntime"),
        ("rembg", "rembg[cpu]"),
        ("torch", "torch"),
        ("transformers", "transformers"),
    ]
    for module_name, pip_name in checks:
        try:
            __import__(module_name)
        except ImportError:
            missing.append(pip_name)

    if missing:
        print(
            "Missing required package(s). Did you activate the virtualenv?\n"
            "  source hologram-pipeline/.venv/bin/activate\n"
            "Then install what's missing:\n"
            f"  pip install {' '.join(missing)}\n"
            "Or just: pip install -r hologram-pipeline/requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)
