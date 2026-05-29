import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
	// Load Markdown and MDX files in the `src/content/blog/` directory.
	loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
	// Type-check frontmatter using a schema
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			// Transform string to Date object
			pubDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			heroImage: z.optional(image()),
			// Pipeline éditorial (agents + supervision)
			tags: z.array(z.string()).default([]),
			author: z.string().default('Labo IA Locale'),
			// draft: true = pas encore vérifié → exclu du build de prod
			draft: z.boolean().default(false),
			// Sources vérifiées (URL réelles) — traçabilité du garde-fou
			sources: z.array(z.object({ label: z.string(), url: z.string().url() })).default([]),
		}),
});

export const collections = { blog };
