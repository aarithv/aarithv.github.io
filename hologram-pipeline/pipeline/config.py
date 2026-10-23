"""Single source of truth for the hologram pipeline's tunable constants."""

# The one hue used everywhere in the viewer. Change this (or pass --color) to
# recolor the whole hologram — nothing else in the shader introduces a hue.
DEFAULT_COLOR = "#00E5FF"

# --- Face detection / crop ---
# How far above the detected face bounding box to start the crop (in units of
# the face box's own height), and how far below it to extend down to roughly
# the shoulder line.
HEADROOM_FACTOR = 0.6
SHOULDER_DROP_FACTOR = 1.8
# Horizontal margin around the face box, in units of the face box's width.
SIDE_MARGIN_FACTOR = 1.6

# --- Mask bottom fade ---
# Fraction of the crop's height (from the bottom) over which the alpha mask
# is smoothstep-faded to zero, so the bust dissolves rather than hard-cuts.
FADE_BAND_FRACTION = 0.18

# --- Depth ---
DEPTH_MODEL_PRIMARY = "depth-anything/Depth-Anything-V2-Small-hf"
DEPTH_MODEL_FALLBACK = "Intel/dpt-hybrid-midas"
BILATERAL_D = 9
BILATERAL_SIGMA_COLOR = 25
BILATERAL_SIGMA_SPACE = 25

# --- Geometry / export ---
MAX_POINTS = 200_000
SCALE_XY = 260.0  # pixels per world-unit, chosen so the bust roughly fills [-1, 1]
DEFAULT_DEPTH_SCALE = 0.6  # initial value only — live-tunable in the viewer GUI

# --- Rembg ---
REMBG_MODEL = "u2net_human_seg"
