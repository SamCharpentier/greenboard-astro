// @ts-check
import { existsSync, readFileSync } from "node:fs";
import { defineConfig, fontProviders } from "astro/config";
import sitemap from "@astrojs/sitemap";
import { SITE_URL } from "./src/consts.ts";
import { isNoindexRoute } from "./src/utils/seo.ts";
import { satteri } from "@astrojs/markdown-satteri";
import markOurs from "./src/utils/mark-ours.mjs";

/* A page that asks search engines not to index it stays out of the sitemap too,
   whether that comes from NOINDEX_ROUTES or from its own content */
/** @param {string} pathname */
const builtPageIsNoindex = (pathname) => {
  const file = new URL(`./dist${pathname.replace(/\/?$/, "/")}index.html`, import.meta.url);
  return existsSync(file) && /<meta name="robots" content="noindex/.test(readFileSync(file, "utf8"));
};

export default defineConfig({
  site: SITE_URL,
  markdown: {
    processor: satteri({ hastPlugins: [markOurs] }),
  },
  integrations: [
    sitemap({
      filter: (page) => {
        const { pathname } = new URL(page);
        return !isNoindexRoute(pathname) && !builtPageIsNoindex(pathname);
      },
    }),
  ],
  fonts: [
    {
      name: "Outfit",
      cssVariable: "--font-outfit",
      provider: fontProviders.local(),
      fallbacks: ["Helvetica Neue", "Arial", "sans-serif"],
      options: {
        variants: [
          {
            weight: "100 900",
            style: "normal",
            src: ["./src/assets/fonts/outfit-variable.woff2"],
          },
        ],
      },
    },
  ],
  vite: { build: { cssTarget: "safari15.4" } },
});
