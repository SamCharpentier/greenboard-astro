import { defineCollection, reference } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

/*
 * Each collection is shaped like the Sanity document it becomes: the same
 * field names, references between documents by id, SEO on every page type.
 * Moving to Sanity swaps the loader for a GROQ query that returns this shape,
 * and the templates stay as they are.
 */

const seo = z.object({
  title: z.string().optional(),
  description: z.string(),
  noindex: z.boolean().default(false),
});

const status = z.enum(["published", "draft"]).default("published");

const people = defineCollection({
  loader: glob({ pattern: "*.json", base: "./src/content/people" }),
  schema: ({ image }) =>
    z.object({
      name: z.string(),
      role: z.string().optional(),
      company: z.string().optional(),
      image: image().optional(),
    }),
});

const customers = defineCollection({
  loader: glob({ pattern: "*.json", base: "./src/content/customers" }),
  schema: z.object({
    name: z.string(),
    testimonial: z
      .object({
        quote: z.string(),
        person: reference("people"),
      })
      .optional(),
  }),
});

const products = defineCollection({
  loader: glob({ pattern: "*.json", base: "./src/content/products" }),
  schema: ({ image }) =>
    z.object({
      name: z.string(),
      title: z.string(),
      lead: z.string(),
      summary: z.string(),
      order: z.number(),
      features: z.array(
        z.object({
          heading: z.string(),
          text: z.array(z.string()),
          image: image(),
          video: z.string().optional(),
        }),
      ),
      seo,
    }),
});

const solutions = defineCollection({
  loader: glob({ pattern: "*.json", base: "./src/content/solutions" }),
  schema: ({ image }) =>
    z.object({
      name: z.string(),
      title: z.string(),
      tagline: z.string(),
      summary: z.string(),
      image: image(),
      imageAlt: z.string().optional(),
      order: z.number(),
      benefits: z.array(z.object({ heading: z.string(), text: z.string() })),
      seo,
    }),
});

const comparisons = defineCollection({
  loader: glob({ pattern: "*.json", base: "./src/content/comparisons" }),
  schema: ({ image }) =>
    z.object({
      competitor: z.string(),
      heading: z.string(),
      logo: image(),
      summary: z.string(),
      rows: z.array(
        z.object({
          feature: z.string(),
          greenboard: z.boolean(),
          competitor: z.boolean(),
        }),
      ),
      asOf: z.coerce.date(),
      status,
      seo,
    }),
});

const caseStudies = defineCollection({
  loader: glob({ pattern: "*.md", base: "./src/content/case-studies" }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      customer: z.string(),
      firmType: reference("solutions"),
      logo: image(),
      summary: z.string(),
      excerpt: z.string(),
      stats: z.array(
        z.object({
          number: z.string(),
          unit: z.string().optional(),
          label: z.string(),
        }),
      ),
      facts: z.array(z.object({ label: z.string(), value: z.string() })),
      quote: z.object({ text: z.string(), person: reference("people") }),
      date: z.coerce.date(),
      status,
      seo,
    }),
});

const posts = defineCollection({
  loader: glob({ pattern: "*.md", base: "./src/content/posts" }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      summary: z.string(),
      date: z.coerce.date(),
      author: reference("people").optional(),
      featured: z.boolean().default(false),
      whitepaperForm: z.boolean().default(false),
      cover: image().optional(),
      coverAlt: z.string().optional(),
      coverUrl: z.url().optional(),
      status,
      seo,
    }),
});

export const collections = {
  people,
  customers,
  products,
  solutions,
  comparisons,
  caseStudies,
  posts,
};
