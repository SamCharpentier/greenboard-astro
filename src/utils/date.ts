import { SITE_LOCALE } from "@/consts.ts";

/** Formats a date as text for props, where `FormattedDate` can't go. Used by the blog. */
export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat(SITE_LOCALE, {
    dateStyle: "long",
    timeZone: "UTC",
  }).format(date);
}
