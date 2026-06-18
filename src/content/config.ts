import { defineCollection, z } from 'astro:content';

const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updateDate: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    category: z.enum(['local', 'veille', 'radar']).default('local'),
    draft: z.boolean().default(false),
    sources: z.array(z.object({
      label: z.string(),
      url: z.string(),
    })).default([]),
  }),
});

export const collections = { blog: blogCollection };
