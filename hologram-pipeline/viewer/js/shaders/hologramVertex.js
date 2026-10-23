export const hologramVertexShader = /* glsl */ `
  uniform float uPointSize;      // world-space point radius factor
  uniform float uDepthScale;
  uniform float uViewportHeight; // renderer framebuffer height, device px
  uniform float uFovFactor;      // 1.0 / tan(radians(fov) / 2.0)

  varying float vIntensity;
  varying vec3 vViewPos;

  void main() {
    // Baked luminance * bottom-fade, written into the PLY as r=g=b.
    vIntensity = color.r;

    vec3 pos = position;
    pos.z *= uDepthScale;

    vec4 mvPosition = modelViewMatrix * vec4(pos, 1.0);
    vViewPos = mvPosition.xyz;
    gl_Position = projectionMatrix * mvPosition;

    // Proper perspective size attenuation: converts a world-space point
    // radius into screen pixels at this fragment's depth, instead of an
    // arbitrary magic-number constant. Also scaled by point-local intensity
    // so faded (background/edge) points shrink rather than staying full
    // size and merely dim.
    float pixelsPerWorldUnit = (uViewportHeight * uFovFactor) / (2.0 * -mvPosition.z);
    gl_PointSize = uPointSize * pixelsPerWorldUnit * (0.4 + 0.6 * vIntensity);
  }
`;
