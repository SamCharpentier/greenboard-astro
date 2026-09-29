import { getEntry } from "astro:content";

/** Customers shown wherever the site says who trusts Greenboard, in the order they run. */
const TRUSTED = [
  "betterment",
  "kroll",
  "fiduciary",
  "root",
  "jmg-financial-group",
  "fsg",
  "capital",
  "retirable",
  "chicago-partners-wealth-advisors",
  "harbert-management-group",
  "summit-wealth-management",
  "compound-planning",
  "accolade-partners",
  "matter-family-office",
  "triad-financial-services",
  "tobias-financial-advisors",
] as const;

/** The trusted customers that have a logo, ready for `LogoMarquee`. Used by the homepage and About. */
export async function trustedLogos(): Promise<{ image: ImageMetadata; name: string }[]> {
  const entries = await Promise.all(TRUSTED.map((id) => getEntry("customers", id)));
  return entries.flatMap((entry) =>
    entry?.data.logo ? [{ image: entry.data.logo, name: entry.data.name }] : [],
  );
}
