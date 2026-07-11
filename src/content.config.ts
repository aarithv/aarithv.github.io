import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    tech: z.array(z.string()),
    role: z.string(),
    links: z
      .object({
        github: z.string().url().optional(),
        demo: z.string().url().optional(),
        writeup: z.string().url().optional(),
      })
      .optional(),
    images: z.array(z.string()).optional(),
  }),
});

const research = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/research' }),
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
          url: z.string().url(),
        })
      )
      .optional(),
  }),
});

const awards = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/awards' }),
  schema: z.object({
    name: z.string(),
    body: z.string(),
    year: z.number(),
    context: z.string(),
  }),
});

export const collections = { projects, research, awards };
