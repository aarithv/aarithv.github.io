import fs from 'node:fs';
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

// The READMEs in public/ folders are notes for editing (see EDITING.md), not
// pages, so they're removed from the built site.
const folderNotes = ['documents/README.md', 'images/photography/README.md'];
const dropFolderNotes = {
  name: 'drop-folder-notes',
  hooks: {
    'astro:build:done': ({ dir }) => {
      for (const note of folderNotes) fs.rmSync(new URL(note, dir), { force: true });
    },
  },
};

export default defineConfig({
  // aarithv.github.io is a *user* Pages site (the repo must be named
  // aarithv.github.io for GitHub Pages to serve it at the domain root),
  // so base stays '/'. If this repo is ever deployed as a *project* page
  // instead (a different repo name, served under aarithv.github.io/<repo>/),
  // change base to '/<repo-name>/'.
  site: 'https://aarithv.github.io',
  base: '/',
  integrations: [dropFolderNotes],
  vite: {
    plugins: [tailwindcss()],
  },
});
