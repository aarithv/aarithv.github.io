import * as THREE from 'three';

// Rim-lit hologram shader shared by the home brain and the page-header
// minis: faces turned away from the viewer glow, faces toward it go nearly
// clear, so the gyri read as contour lines and the inside stays visible.
// `uLit` (0..1) brightens and whitens a region when it is selected.
const vertexShader = /* glsl */ `
  varying vec3 vNormal;
  varying vec3 vView;
  varying float vY;
  void main() {
    vec4 mv = modelViewMatrix * vec4(position, 1.0);
    vNormal = normalize(normalMatrix * normal);
    vView = -mv.xyz;
    vY = position.y;
    gl_Position = projectionMatrix * mv;
  }
`;

const fragmentShader = /* glsl */ `
  uniform vec3 uColor;
  uniform float uBase;
  uniform float uRim;
  uniform float uTime;
  uniform float uLit;
  varying vec3 vNormal;
  varying vec3 vView;
  varying float vY;
  void main() {
    float facing = abs(dot(normalize(vNormal), normalize(vView)));
    float rim = pow(1.0 - facing, 2.4);
    float scan = 0.88 + 0.12 * sin(vY * 60.0 - uTime * 1.4);
    float a = (uBase + rim * uRim) * scan * (1.0 + uLit * 1.6);
    vec3 c = mix(uColor, vec3(0.6, 1.0, 0.75), uLit * 0.55);
    gl_FragColor = vec4(c, clamp(a, 0.0, 1.0));
  }
`;

const phosphor = new THREE.Color(0x00ff41);

export function hologramMaterial(base: number, rim: number) {
  return new THREE.ShaderMaterial({
    uniforms: {
      uColor: { value: phosphor },
      uBase: { value: base },
      uRim: { value: rim },
      uTime: { value: 0 },
      uLit: { value: 0 },
    },
    vertexShader,
    fragmentShader,
    transparent: true,
    depthWrite: false,
    depthTest: false,
    side: THREE.DoubleSide,
    blending: THREE.AdditiveBlending,
  });
}

/** Name of the region a GLB mesh belongs to (trimesh puts it on the node). */
export function meshName(mesh: THREE.Object3D) {
  return mesh.name || mesh.parent?.name || '';
}
