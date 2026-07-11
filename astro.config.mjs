// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  // Matches the aarithv/aarithv.github.io repo — a user Pages site, so it
  // deploys at the domain root (no `base` needed).
  site: 'https://aarithv.github.io',
  vite: {
    plugins: [tailwindcss()]
  }
});