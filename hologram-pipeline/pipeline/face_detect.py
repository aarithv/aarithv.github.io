"""Face bounding-box detection.

OpenCV's built-in Haar cascade is the primary method: it ships inside
opencv-python-headless (no extra download, no API-version risk) and is more
than adequate for a single centered frontal headshot. MediaPipe's modern
Tasks API is tried first as an optional enhancement (better on angled faces),
but any failure — missing package, failed model download, API mismatch — is
swallowed and we fall back to Haar without complaint.
"""

from __future__ import annotations

import numpy as np


def _detect_with_mediapipe(image_rgb: np.ndarray) -> tuple[int, int, int, int] | None:
    try:
        import mediapipe as mp
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import vision as mp_vision
    except Exception:
        return None

    try:
        import urllib.request
        import os
        import tempfile

        model_path = os.path.join(tempfile.gettempdir(), "blaze_face_short_range.tflite")
        if not os.path.exists(model_path):
            url = (
                "https://storage.googleapis.com/mediapipe-models/face_detector/"
                "blaze_face_short_range/float16/latest/blaze_face_short_range.tflite"
            )
            urllib.request.urlretrieve(url, model_path)

        base_options = mp_python.BaseOptions(model_asset_path=model_path)
        options = mp_vision.FaceDetectorOptions(base_options=base_options)
        detector = mp_vision.FaceDetector.create_from_options(options)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        result = detector.detect(mp_image)
        if not result.detections:
            return None

        box = result.detections[0].bounding_box
        return (box.origin_x, box.origin_y, box.width, box.height)
    except Exception:
        return None


def _detect_with_haar(image_rgb: np.ndarray) -> tuple[int, int, int, int] | None:
    import cv2

    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    cascade = cv2.CascadeClassifier(cascade_path)
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))
    if len(faces) == 0:
        return None

    # Largest detected face (most likely the subject, not a background face).
    faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
    x, y, w, h = faces[0]
    return (int(x), int(y), int(w), int(h))


def detect_face_bbox(image_rgb: np.ndarray) -> tuple[int, int, int, int]:
    """Return (x, y, w, h) of the primary face, in pixel coordinates.

    Falls back to a centered box covering the middle ~40% of the image width
    if no face is found at all, so the pipeline never hard-fails on a
    detection miss.
    """
    box = _detect_with_mediapipe(image_rgb) or _detect_with_haar(image_rgb)
    if box is not None:
        return box

    h_img, w_img = image_rgb.shape[:2]
    w = int(w_img * 0.4)
    h = int(h_img * 0.4)
    x = (w_img - w) // 2
    y = int(h_img * 0.15)
    return (x, y, w, h)
