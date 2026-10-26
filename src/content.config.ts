import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Everything editable lives in the top-level content/ folder; see EDITING.md.

const research = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './content/research' }),
  schema: z.object({
    lab: z.string(),
    pi: z.string(),
    startDate: z.coerce.date(),
    endDate: z.coerce.date().optional(),
    description: z.string(),
    links: z
      .array(
        z.object({
          label: z.string(),
          url: z.string(),
        })
      )
      .optional(),
  }),
});

const awards = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './content/awards' }),
  schema: z.object({
    name: z.string(),
    body: z.string(),
    year: z.number(),
    context: z.string(),
  }),
});

const link = z.object({ label: z.string(), href: z.string() });
const section = z.object({ label: z.string(), structure: z.string(), role: z.string(), summary: z.string() });
const image = z.object({ file: z.string(), alt: z.string().optional(), caption: z.string().optional() });

// Site-wide text, the bio, and one file per page. Each page's body (below its
// front matter) is its intro paragraph.
const pages = defineCollection({
  loader: glob({ pattern: ['site.md', 'bio.md', 'pages/*.md'], base: './content' }),
  schema: z.object({
    // every page (and site.md, as the default)
    title: z.string().optional(),
    description: z.string().optional(),
    shareImage: z.string().optional(),
    // site.md
    name: z.string().optional(),
    brand: z.string().optional(),
    tagline: z.string().optional(),
    location: z.string().optional(),
    links: z.array(link).optional(),
    sections: z.record(z.string(), section).optional(),
    // home
    role: z.string().optional(),
    status: z.string().optional(),
    // about
    headshot: image.optional(),
    readout: z.array(z.object({ key: z.string(), value: z.string() })).optional(),
    snapshots: z.array(image).optional(),
    // projects
    tools: z.array(z.object({ name: z.string(), href: z.string(), summary: z.string() })).optional(),
    statusTitle: z.string().optional(),
    statusText: z.string().optional(),
    // resume
    documents: z.array(z.object({ file: z.string(), label: z.string() })).optional(),
    // photography
    camera: z.string().optional(),
    photos: z.array(z.object({ file: z.string(), camera: z.string().optional() })).optional(),
  }),
});

export const collections = { research, awards, pages };
