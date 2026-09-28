/** Site navigation: one source for the nav, the mobile menu and the footer. */

export type NavLink = { label: string; href: string };
export type NavGroup = { label: string; links: NavLink[] };
export type NavMenu = { label: string; groups: NavGroup[]; stats?: boolean };

const home = (anchor: string) => `/#${anchor}`;

const productLinks: NavLink[] = [
  { label: "GreenboardGo", href: home("platform") },
  { label: "Go Agents", href: home("platform") },
];

const modules: NavLink[] = [
  { label: "Archiving & supervision", href: home("platform") },
  { label: "Employee compliance", href: home("platform") },
  { label: "Firm compliance", href: home("platform") },
  { label: "Third-party diligence", href: home("platform") },
  { label: "Content reviews", href: home("platform") },
  { label: "Unified books & records", href: home("platform") },
];

const firmTypes: NavLink[] = [
  { label: "Solutions overview", href: "/solutions" },
  { label: "Financial advisors", href: home("segments") },
  { label: "Private funds", href: home("segments") },
  { label: "Hedge funds", href: home("segments") },
  { label: "Broker dealers", href: home("segments") },
  { label: "Service partners", href: home("segments") },
  { label: "Partnerships", href: home("segments") },
];

const firmSizes: NavLink[] = [
  { label: "Small firms", href: home("firm-sizes") },
  { label: "Growing businesses", href: home("firm-sizes") },
  { label: "Enterprise", href: home("firm-sizes") },
];

const customerLove: NavLink[] = [
  { label: "Case studies", href: home("case-studies") },
  { label: "In their words", href: home("testimonials") },
];

const company: NavLink[] = [
  { label: "About", href: "/about" },
  { label: "Our fiduciary commitment", href: "#" },
  { label: "Security & privacy", href: "#" },
  { label: "Contact the team", href: "#" },
];

export const menus: NavMenu[] = [
  {
    label: "Product",
    groups: [
      {
        label: "Platform",
        links: [{ label: "Product overview", href: "/products" }, ...productLinks],
      },
      { label: "Modules", links: modules },
    ],
  },
  {
    label: "Customers",
    groups: [
      { label: "Firm types", links: firmTypes },
      { label: "By firm size", links: firmSizes },
      { label: "Customer love", links: customerLove },
    ],
    stats: true,
  },
  {
    label: "Company",
    groups: [{ label: "Company", links: company }],
  },
];

/** Shown beside the Customers menu. Real figures only. */
export const navStats = [
  { number: "703+", label: "Regulated financial firms served last quarter, and counting" },
  { number: "32 367+", label: "People served last quarter, and counting" },
];

export const demoHref = home("demo");
export const loginHref = "#";

export const footerGroups: NavGroup[] = [
  {
    label: "Product",
    links: [{ label: "Product overview", href: "/products" }, ...modules],
  },
  {
    label: "GreenboardGo",
    links: [
      { label: "Overview", href: "#" },
      { label: "Capabilities", href: "#" },
      { label: "Go Agents", href: "#" },
      { label: "Slack & Teams", href: "#" },
      { label: "Book a demo", href: demoHref },
    ],
  },
  {
    label: "Customers",
    links: [
      { label: "Solutions overview", href: "/solutions" },
      { label: "Financial advisors", href: "#" },
      { label: "Private funds", href: "#" },
      { label: "Hedge funds", href: "#" },
      { label: "Broker dealers", href: "#" },
      { label: "Partnerships", href: "#" },
      { label: "Small firms", href: "#" },
      { label: "Growing businesses", href: "#" },
      { label: "Enterprise", href: "#" },
    ],
  },
  {
    label: "Customer love",
    links: [
      { label: "Case studies", href: "#" },
      { label: "In their words", href: "#" },
      { label: "Trusted by 500+ firms", href: "#" },
    ],
  },
  {
    label: "Company",
    links: [
      { label: "About", href: "/about" },
      { label: "Our fiduciary commitment", href: "#" },
      { label: "Security & privacy", href: "#" },
      { label: "Trust Center", href: "#" },
      { label: "Contact", href: "#" },
    ],
  },
];

export const legalLinks: NavLink[] = [
  { label: "Privacy policy", href: "#" },
  { label: "Terms", href: "#" },
  { label: "Security", href: "#" },
  { label: "Trust Center", href: "#" },
];

/** True when `href` is the page being viewed. Anchors and placeholders never are. */
export const isCurrent = (href: string, pathname: string) =>
  href.startsWith("/") &&
  !href.includes("#") &&
  pathname.replace(/\/+$/, "") === href.replace(/\/+$/, "");
