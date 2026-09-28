/** Site name. Appended to every page title and used as `og:site_name`. */
export const SITE_NAME = "Greenboard";
/** Fallback meta description for pages that don't set their own. */
export const SITE_DESCRIPTION =
  "Greenboard is the AI-native system of action for SEC and FINRA compliance.";
/** Canonical origin. Resolves canonical URLs, social images, and the sitemap. */
export const SITE_URL = "https://www.greenboard.com";
/** BCP 47 locale tag used to format dates and numbers. */
export const SITE_LOCALE = "en-US";
/** Routes excluded from search and the sitemap. Surrounding slashes are ignored. */
export const NOINDEX_ROUTES: string[] = ["/404", "/example-components"];
