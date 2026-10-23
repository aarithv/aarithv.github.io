#!/usr/bin/env node
// One-time/occasional vendoring script: copies three.js core + jsm addons and
// lil-gui into viewer/vendor/, frozen and independent of any node_modules.
//
// Usage:
//   cd hologram-pipeline/scripts && npm install && node vendor_three.mjs
//
// Sources three.js from the sibling Astro project's node_modules (faster,
// avoids re-downloading something already on disk) if present; otherwise
// falls back to this directory's own node_modules/three (run `npm install
// three@<version>` here first in that case). lil-gui always comes from this
// directory's own node_modules (see package.json).

import { existsSync, cpSync, mkdirSync, rmSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const scriptsDir = dirname(fileURLToPath(import.meta.url));
const pipelineRoot = join(scriptsDir, '..');
const siblingThree = join(pipelineRoot, '..', 'node_modules', 'three');
const localThree = join(scriptsDir, 'node_modules', 'three');
const threeSrc = existsSync(siblingThree) ? siblingThree : localThree;

if (!existsSync(threeSrc)) {
  console.error(
    'Could not find a three.js install to vendor from. Either run this from a ' +
      'checkout where ../node_modules/three exists (the sibling Astro project), ' +
      'or run `npm install` inside scripts/ first.'
  );
  process.exit(1);
}

const vendorDir = join(pipelineRoot, 'viewer', 'vendor');
const threeDest = join(vendorDir, 'three');
const guiDest = join(vendorDir, 'lil-gui');

rmSync(threeDest, { recursive: true, force: true });
mkdirSync(threeDest, { recursive: true });
cpSync(join(threeSrc, 'build', 'three.module.js'), join(threeDest, 'three.module.js'));
cpSync(join(threeSrc, 'build', 'three.core.js'), join(threeDest, 'three.core.js'));
cpSync(join(threeSrc, 'examples', 'jsm'), join(threeDest, 'jsm'), { recursive: true });
console.log(`Vendored three.js from ${threeSrc} -> ${threeDest}`);

const guiSrc = join(scriptsDir, 'node_modules', 'lil-gui', 'dist', 'lil-gui.esm.js');
if (existsSync(guiSrc)) {
  mkdirSync(guiDest, { recursive: true });
  cpSync(guiSrc, join(guiDest, 'lil-gui.esm.js'));
  console.log(`Vendored lil-gui -> ${guiDest}`);
} else {
  console.warn(`lil-gui not found at ${guiSrc} — run \`npm install\` in scripts/ first.`);
}
