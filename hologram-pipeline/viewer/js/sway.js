// Slow idle side-to-side sway applied to the point-cloud object itself —
// independent of OrbitControls, which separately orbits the camera. Keeps
// the two from fighting over one rotation value.
const SWAY_SPEED = 0.35;
const SWAY_AMPLITUDE = 0.18; // radians, ~10 degrees

export function applySway(object3D, elapsedSeconds) {
  object3D.rotation.y = Math.sin(elapsedSeconds * SWAY_SPEED) * SWAY_AMPLITUDE;
}
