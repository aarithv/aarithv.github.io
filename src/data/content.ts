// Build-time access to the editable content in the top-level content/ folder
// (see EDITING.md), plus discovery of the files people drop into public/.
import fs from 'node:fs';
import path from 'node:path';
import { getEntry, render } from 'astro:content';
import { regions, type Region } from './regions';

export type Section = Region & { label: string; structure: string; role: string; summary: string };

async function entry(id: string) {
  const found = await getEntry('pages', id);
  if (!found) throw new Error(`Missing content file for "${id}" in content/`);
  return found;
}

export async function getSite() {
  return (await entry('site')).data;
}

/** One page's front matter plus its body (the intro) as a renderable component. */
export async function getPage(name: string) {
  const page = await entry(`pages/${name}`);
  const { Content } = await render(page);
  return { ...page.data, Content, hasBody: Boolean(page.body?.trim()) };
}

export async function getBio() {
  const { Content } = await render(await entry('bio'));
  return Content;
}

/** The six regions with their editable text from content/site.md. */
export async function getSections(): Promise<Section[]> {
  const text = (await getSite()).sections ?? {};
  return regions.map((r) => {
    const t = text[r.id];
    if (!t) throw new Error(`content/site.md is missing the "${r.id}" section`);
    return { ...r, ...t };
  });
}

export async function getSectionFor(pathname: string) {
  const clean = pathname.replace(/\/$/, '') || '/';
  // Sub-pages (e.g. /projects/gradients) belong to their section's region.
  return (await getSections()).find((s) => clean === s.href || clean.startsWith(`${s.href}/`));
}

const publicDir = path.join(process.cwd(), 'public');
function filesIn(dir: string, extensions: string[]) {
  const full = path.join(publicDir, dir);
  if (!fs.existsSync(full)) return [];
  return fs
    .readdirSync(full, { withFileTypes: true })
    .filter((f) => f.isFile() && extensions.includes(path.extname(f.name).toLowerCase()))
    .map((f) => f.name);
}

// Ordered: files listed in the content file first (in that order), then any
// others in the folder alphabetically. Listed files that no longer exist are
// skipped, so deleting a file never breaks the build.
function ordered(found: string[], listed: string[]) {
  const present = new Set(found);
  const first = listed.filter((f) => present.has(f));
  const rest = found.filter((f) => !listed.includes(f)).sort((a, b) => a.localeCompare(b));
  return [...first, ...rest];
}

/** Every image in public/images/photography/. */
export async function getPhotos() {
  const page = (await entry('pages/photography')).data;
  const meta = new Map((page.photos ?? []).map((p) => [p.file, p]));
  const files = ordered(filesIn('images/photography', ['.jpg', '.jpeg', '.png', '.webp', '.avif', '.gif']), [
    ...meta.keys(),
  ]);
  return files.map((file) => {
    const camera = meta.get(file)?.camera ?? page.camera ?? '';
    return { src: `/images/photography/${encodeURIComponent(file)}`, alt: camera || file, camera };
  });
}

/** Turns "av_resume_071226.pdf" into "Av resume 071226" for unlisted files. */
function labelFromFile(file: string) {
  const words = file.replace(/\.[^.]+$/, '').replace(/[_-]+/g, ' ').trim();
  return words.charAt(0).toUpperCase() + words.slice(1);
}

/** Every PDF directly in public/documents/ (subfolders are for linked files). */
export async function getDocuments() {
  const page = (await entry('pages/resume')).data;
  const labels = new Map((page.documents ?? []).map((d) => [d.file, d.label]));
  return ordered(filesIn('documents', ['.pdf']), [...labels.keys()]).map((file) => ({
    label: labels.get(file) ?? labelFromFile(file),
    href: `/documents/${encodeURIComponent(file)}`,
  }));
}

export function plateFor(region: Region) {
  return `PL. ${String(regions.findIndex((r) => r.id === region.id) + 1).padStart(2, '0')}`;
}
