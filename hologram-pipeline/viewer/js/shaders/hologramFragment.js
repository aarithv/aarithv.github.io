export const hologramFragmentShader = /* glsl */ `
  uniform vec3 uColor;
  uniform float uTime;
  uniform float uScanDensity;
  uniform float uGlowIntensity;
  uniform float uGlitchStrength;

  varying float vIntensity;
  varying vec3 vViewPos;

  float hash(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
  }

  void main() {
    // Circular point sprite instead of a square.
    vec2 pc = gl_PointCoord - 0.5;
    float d = length(pc);
    if (d > 0.5) discard;

    // Cheap rim/fresnel proxy: brighter toward the edge of each point sprite.
    float rim = smoothstep(0.15, 0.5, d);

    // Slowly scrolling horizontal scanlines, in view space so they read as
    // part of the "projection" rather than the screen.
    float scan = 0.5 + 0.5 * sin(vViewPos.y * uScanDensity - uTime * 1.5);

    // Subtle flicker.
    float flicker = 0.92 + 0.08 * sin(uTime * 17.0 + vViewPos.x * 3.0);

    // Occasional hashed glitch line: most of the time contributes nothing.
    float glitchLine = step(0.996, hash(vec2(floor(uTime * 6.0), floor(vViewPos.y * 8.0))));
    float glitchBoost = glitchLine * uGlitchStrength * 40.0;

    float brightness = vIntensity * flicker * mix(0.85, 1.0, scan) + rim * uGlowIntensity + glitchBoost;
    float alpha = vIntensity * (1.0 - d);

    gl_FragColor = vec4(uColor * brightness, alpha);
  }
`;
