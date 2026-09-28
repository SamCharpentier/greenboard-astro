import css from "@/styles/base.css?raw";

/** Reads the design tokens straight from `base.css`, so the web system page can never drift from the values the site uses. */

type Scope = Map<string, string>;

const source = css.replace(/\/\*[\s\S]*?\*\//g, "");

const rules = [...source.matchAll(/([^{}]+)\{([^{}]*)\}/g)].map((match) => ({
  selectors: match[1].split(",").map((selector) => selector.trim()),
  tokens: new Map(
    [...match[2].matchAll(/--([\w-]+)\s*:\s*([^;]+);/g)].map((token) => [
      token[1],
      token[2].trim().replace(/\s+/g, " "),
    ]),
  ) as Scope,
}));

/** Tokens declared on `:root`. */
export const root: Scope =
  rules.find(
    (rule) => rule.selectors.length === 1 && rule.selectors[0] === ":root",
  )?.tokens ?? new Map();

export const themeNames = ["light", "soft", "dark", "deep", "brand"] as const;
export type ThemeName = (typeof themeNames)[number];

const declared = (name: ThemeName): Scope =>
  rules.find((rule) => rule.selectors.includes(`.theme-${name}`))?.tokens ??
  new Map();

/** Tokens each theme class sets, over the light values `:root` starts from. */
export const themes = Object.fromEntries(
  themeNames.map((name) => [
    name,
    new Map([...declared("light"), ...declared(name)]),
  ]),
) as Record<ThemeName, Scope>;

const lookup = (name: string, scope?: Scope) =>
  scope?.get(name) ?? root.get(name);

/** A token's value with every `var()` it points to followed through. */
export function resolve(name: string, scope?: Scope): string | undefined {
  const value = lookup(name, scope);
  if (!value) return undefined;
  const alias = value.match(/^var\(--([\w-]+)\)$/);
  return alias ? (resolve(alias[1], scope) ?? value) : value;
}

/** A token's value in words: `ivory-50`, `midnight-800 at 16%`. */
export function describe(value: string, scope?: Scope): string {
  const alias = value.match(/^var\(--([\w-]+)\)$/);
  if (alias) {
    const next = scope?.get(alias[1]);
    return next ? describe(next, scope) : alias[1];
  }
  const mix = value.match(/^color-mix\(in srgb, (.+?) (\d+)%, (.+)\)$/);
  if (mix) {
    const base = describe(mix[1], scope);
    return mix[3] === "transparent"
      ? `${base} at ${mix[2]}%`
      : `${base} ${mix[2]}%, ${describe(mix[3], scope)}`;
  }
  return value.toLowerCase();
}

type Rgb = [number, number, number];

const hexToRgb = (hex: string): Rgb | undefined => {
  const match = hex.match(/^#([0-9a-f]{6})$/i);
  if (!match) return undefined;
  const int = parseInt(match[1], 16);
  return [(int >> 16) & 255, (int >> 8) & 255, int & 255];
};

/** A color token as RGB, with `color-mix` blended over `backdrop` when it is see-through. */
export function rgb(
  value: string,
  scope?: Scope,
  backdrop?: Rgb,
): Rgb | undefined {
  const alias = value.match(/^var\(--([\w-]+)\)$/);
  if (alias) {
    const next = lookup(alias[1], scope);
    return next ? rgb(next, scope, backdrop) : undefined;
  }
  const mix = value.match(/^color-mix\(in srgb, (.+?) (\d+)%, (.+)\)$/);
  if (mix) {
    const a = rgb(mix[1], scope, backdrop);
    const b =
      mix[3] === "transparent" ? backdrop : rgb(mix[3], scope, backdrop);
    if (!a || !b) return undefined;
    const share = Number(mix[2]) / 100;
    return a.map((channel, i) => channel * share + b[i] * (1 - share)) as Rgb;
  }
  return hexToRgb(value);
}

export const toHex = (color: Rgb) =>
  `#${color.map((channel) => Math.round(channel).toString(16).padStart(2, "0")).join("")}`.toUpperCase();

const luminance = (color: Rgb) => {
  const [r, g, b] = color.map((channel) => {
    const c = channel / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};

/** WCAG contrast ratio between two colors. */
export function contrast(a: Rgb, b: Rgb) {
  const [light, dark] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (light + 0.05) / (dark + 0.05);
}

/** WCAG level for a contrast ratio, for text of normal size. */
export const level = (ratio: number) =>
  ratio >= 7
    ? "AAA"
    : ratio >= 4.5
      ? "AA"
      : ratio >= 3
        ? "Large text only"
        : "Fails";

/** The two ends of a fluid token, in pixels. */
export function fluid(name: string) {
  const min = Number(resolve(`${name}-min`));
  const max = Number(resolve(`${name}-max`));
  return Number.isFinite(min) && Number.isFinite(max)
    ? { min, max }
    : undefined;
}

/** A fluid range in words: `48 to 96px`. */
export function range(name: string) {
  const ends = fluid(name);
  return ends ? `${ends.min} to ${ends.max}px` : "";
}
