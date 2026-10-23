import * as THREE from 'three';
import { PLYLoader } from 'three/addons/loaders/PLYLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import GUI from 'lil-gui';

import { hologramVertexShader } from './shaders/hologramVertex.js';
import { hologramFragmentShader } from './shaders/hologramFragment.js';
import { applySway } from './sway.js';
import * as defaults from './config.js';

async function loadMeta() {
  try {
    const res = await fetch('./data/meta.json', { cache: 'no-store' });
    if (!res.ok) throw new Error(`meta.json fetch failed: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.warn('Could not load data/meta.json, using built-in defaults.', err);
    return { color: defaults.DEFAULT_COLOR, depthScale: defaults.DEFAULT_DEPTH_SCALE };
  }
}

function showFatalError(message) {
  const el = document.createElement('div');
  el.style.cssText =
    'position:fixed;inset:0;display:flex;align-items:center;justify-content:center;' +
    'color:#ff5555;background:#000;font:14px ui-monospace,monospace;padding:2rem;text-align:center;';
  el.textContent = message;
  document.body.appendChild(el);
}

async function main() {
  const meta = await loadMeta();

  const canvas = document.getElementById('hologram-canvas');
  const scene = new THREE.Scene();

  const camera = new THREE.PerspectiveCamera(40, window.innerWidth / window.innerHeight, 0.01, 100);
  camera.position.set(0, 0, 3);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setClearColor(0x000000, 1);

  const controls = new OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;
  controls.enablePan = false;
  controls.minDistance = 0.8;
  controls.maxDistance = 8;
  // Constrain rotation so the point cloud's nonexistent "back" (it's a
  // single depth layer from one photo) is never exposed.
  controls.minAzimuthAngle = -Math.PI / 3; // -60deg
  controls.maxAzimuthAngle = Math.PI / 3; // +60deg
  controls.minPolarAngle = Math.PI / 2 - 0.35;
  controls.maxPolarAngle = Math.PI / 2 + 0.35;

  function fovFactorFor(cam) {
    return 1.0 / Math.tan(THREE.MathUtils.degToRad(cam.fov) / 2);
  }

  const uniforms = {
    uColor: { value: new THREE.Color(meta.color || defaults.DEFAULT_COLOR) },
    uTime: { value: 0 },
    uPointSize: { value: defaults.DEFAULT_POINT_SIZE },
    uDepthScale: { value: meta.depthScale ?? defaults.DEFAULT_DEPTH_SCALE },
    uScanDensity: { value: defaults.DEFAULT_SCAN_DENSITY },
    uGlowIntensity: { value: defaults.DEFAULT_GLOW_INTENSITY },
    uGlitchStrength: { value: defaults.DEFAULT_GLITCH_STRENGTH },
    // Physically-based point-size attenuation (see hologramVertex.js) needs
    // to know the actual framebuffer height and vertical FOV; kept in sync
    // on resize below.
    uViewportHeight: { value: renderer.domElement.height },
    uFovFactor: { value: fovFactorFor(camera) },
  };

  const material = new THREE.ShaderMaterial({
    uniforms,
    vertexShader: hologramVertexShader,
    fragmentShader: hologramFragmentShader,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    vertexColors: true,
  });

  let pointCloud = null;

  const loader = new PLYLoader();
  loader.load(
    './data/points.ply',
    (geometry) => {
      geometry.computeBoundingSphere();
      geometry.center();

      pointCloud = new THREE.Points(geometry, material);
      scene.add(pointCloud);

      // Frame the camera on the bust so head+shoulders fill the view.
      const radius = geometry.boundingSphere ? geometry.boundingSphere.radius : 1;
      const fitDistance = (radius * 1.6) / Math.sin((camera.fov * Math.PI) / 360);
      camera.position.set(0, 0, Math.max(fitDistance, controls.minDistance));
      camera.updateProjectionMatrix();
      controls.target.set(0, 0, 0);
      controls.update();
    },
    undefined,
    (err) => {
      console.error('Failed to load point cloud PLY:', err);
      showFatalError(
        'Could not load hologram data (data/points.ply). Run make_hologram.py --image <photo> first.'
      );
    }
  );

  // --- Optional bloom post-processing ---
  const composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  const bloomPass = new UnrealBloomPass(
    new THREE.Vector2(window.innerWidth, window.innerHeight),
    0.9, // strength
    0.6, // radius
    0.1 // threshold
  );
  composer.addPass(bloomPass);
  composer.addPass(new OutputPass());

  const state = {
    color: meta.color || defaults.DEFAULT_COLOR,
    pointSize: defaults.DEFAULT_POINT_SIZE,
    scanDensity: defaults.DEFAULT_SCAN_DENSITY,
    glowIntensity: defaults.DEFAULT_GLOW_INTENSITY,
    depthScale: meta.depthScale ?? defaults.DEFAULT_DEPTH_SCALE,
    bloom: true,
  };

  const gui = new GUI({ title: 'Hologram' });
  gui.addColor(state, 'color').onChange((v) => uniforms.uColor.value.set(v));
  gui.add(state, 'pointSize', 0.002, 0.05, 0.001).onChange((v) => (uniforms.uPointSize.value = v));
  gui.add(state, 'scanDensity', 0, 40, 0.5).onChange((v) => (uniforms.uScanDensity.value = v));
  gui.add(state, 'glowIntensity', 0, 2, 0.05).onChange((v) => (uniforms.uGlowIntensity.value = v));
  gui.add(state, 'depthScale', 0, 2, 0.02).onChange((v) => (uniforms.uDepthScale.value = v));
  gui.add(state, 'bloom').name('bloom (glow pass)');

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    composer.setSize(window.innerWidth, window.innerHeight);
    uniforms.uViewportHeight.value = renderer.domElement.height;
    uniforms.uFovFactor.value = fovFactorFor(camera);
  });

  const clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);
    const t = clock.getElapsedTime();
    uniforms.uTime.value = t;

    if (pointCloud) applySway(pointCloud, t);
    controls.update();

    if (state.bloom) {
      composer.render();
    } else {
      renderer.render(scene, camera);
    }
  }
  animate();
}

main().catch((err) => {
  console.error(err);
  showFatalError(`Viewer failed to start: ${err.message}`);
});
