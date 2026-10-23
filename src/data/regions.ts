// The site is drawn as an atlas of one brain: each section is a region. This
// file holds the structural side (URL, brain view, order); the text for each
// section (label, structure name, role, summary) lives in content/site.md. The
// home page and every page header render a real 3D brain (see brain-pipeline/)
// where each region is the actual anatomical structure, in MNI152 space.
//
// `map.x` picks the side of the home brain a region's callout label prefers
// (negative = left). `view` is the brain orientation (radians) that best shows
// the structure: yaw turns about the vertical axis from a left-lateral view,
// pitch tilts the top toward the viewer.

export interface Region {
  id: string;
  href: string;
  map: { x: number; y: number };
  view: { yaw: number; pitch: number };
}

export const regions: Region[] = [
  {
    id: 'about',
    href: '/about',
    map: { x: -0.92, y: -0.72 },
    view: { yaw: -0.9, pitch: 0.15 },
  },
  {
    id: 'research',
    href: '/research',
    map: { x: -1, y: 0.02 },
    view: { yaw: 0.35, pitch: 0.2 },
  },
  {
    id: 'projects',
    href: '/projects',
    map: { x: -0.86, y: 0.74 },
    view: { yaw: 0, pitch: 0.55 },
  },
  {
    id: 'awards',
    href: '/awards',
    map: { x: 0.92, y: -0.72 },
    view: { yaw: -0.35, pitch: 0.2 },
  },
  {
    id: 'resume',
    href: '/resume',
    map: { x: 1, y: 0.02 },
    view: { yaw: 0.2, pitch: -0.25 },
  },
  {
    id: 'photography',
    href: '/photography',
    map: { x: 0.86, y: 0.74 },
    view: { yaw: 0.95, pitch: 0.1 },
  },
];

export function regionFor(pathname: string) {
  const clean = pathname.replace(/\/$/, '') || '/';
  // Sub-pages (e.g. /projects/gradients) belong to their section's region.
  return regions.find((r) => clean === r.href || clean.startsWith(`${r.href}/`));
}
