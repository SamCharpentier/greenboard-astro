"""Webflow extraction -> Astro content collections shaped like the planned Sanity documents.

Reads /home/claude/gb/wf/package (content only) and writes src/content/** and
src/assets/images/** in the repo. Copy is carried verbatim apart from the typo
fixes listed in TYPOS, which are reported.
"""
import json, os, re, shutil
from pathlib import Path

PKG = Path("/home/claude/gb/wf/package")
PAGES = PKG / "content/pages"
CMS = PKG / "content/cms"
SITE_IMG = PKG / "assets/site/images"
REPO = Path("/home/claude/greenboard-astro")
CONTENT = REPO / "src/content"
ASSETS = REPO / "src/assets/images"

TYPOS = {
    "Comprehenisve": "Comprehensive",
    "rapidiy": "rapidly",
    "previosuly": "previously",
    "reccomend": "recommend",
    "Reponse Times": "Response Times",
    "their[company blog]": "their [company blog]",
    "channels.**In 2025": "channels.** In 2025",
    "Michel Kitces": "Michael Kitces",
}
fixed = []


def fix(text):
    for bad, good in TYPOS.items():
        if bad in text:
            fixed.append(bad)
            text = text.replace(bad, good)
    return text


def clean(text):
    """Webflow leaves zero-width spaces and trailing spaces behind."""
    return fix(re.sub(r"[​ ]+", " ", text).strip())


def body_of(path):
    return path.read_text().split("---", 2)[2]


def front(path):
    head = path.read_text().split("---", 2)[1]
    out = {}
    for line in head.strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = json.loads(value)
            out[key.strip()] = value
    return out


def sections(body):
    parts = re.split(r"<!-- section: ([\w-]+) -->", body)
    return [(parts[i], parts[i + 1]) for i in range(1, len(parts), 2)]


def lines(text):
    return [l.rstrip() for l in text.splitlines() if l.strip()]


def write_json(folder, slug, data):
    path = CONTENT / folder / f"{slug}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def copy_image(name, folder, target):
    src = SITE_IMG / name
    if not src.exists():
        raise SystemExit(f"missing image {name}")
    dest = ASSETS / folder / f"{target}{src.suffix.lower()}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    return f"../../assets/images/{folder}/{dest.name}"


def seo(meta, fallback_title):
    title = clean(meta.get("seo_title") or fallback_title)
    title = re.sub(r"\s*\|\s*Greenboard\s*$", "", title)
    out = {"title": title, "description": clean(meta.get("seo_description", ""))}
    if "noindex" in meta.get("robots", ""):
        out["noindex"] = True
    return out


# ---------------------------------------------------------------- products
PRODUCT_ORDER = [
    "platform",
    "communications-archiving-supervision",
    "employee-compliance",
    "marketing-compliance",
    "firm-compliance",
    "third-party-compliance",
]
overview = {}
body = body_of(PAGES / "products.md")
for match in re.finditer(r"<!-- link block → /products/([\w-]+) -->\s*\n\s*\n?(.+?)\n\s*\n?(.+?)\n", body):
    overview[match.group(1)] = (clean(match.group(2)), clean(match.group(3)))

for order, slug in enumerate(PRODUCT_ORDER, 1):
    path = PAGES / "products" / f"{slug}.md"
    meta = front(path)
    secs = dict(sections(body_of(path)))
    hero = [l for l in lines(secs["hero_wrap"]) if not l.startswith("[Link")]
    title = clean(next(l for l in hero if l.startswith("# "))[2:])
    lead = clean(hero[-1].strip("*"))
    features = []
    current = None
    for line in lines(secs["feature_wrap"]):
        if line.startswith("## "):
            current = {"heading": clean(line[3:]), "text": []}
            features.append(current)
        elif line.startswith("!["):
            name = re.search(r"images/([^)]+)", line).group(1)
            current["image"] = copy_image(name, "products", f"{slug}-{len(features)}")
        elif line.startswith("[Video:"):
            current["video"] = f"/video/products/{slug}-{len(features)}.mp4"
        elif line.startswith("[Link"):
            continue
        else:
            current["text"].append(clean(line))
    name, summary = overview[slug]
    write_json("products", slug, {
        "name": name,
        "title": title,
        "lead": lead,
        "summary": summary,
        "order": order,
        "features": features,
        "seo": seo(meta, title),
    })

# -------------------------------------------------------------- firm types
# The case study categories. Ordered as the solution pages are, then the rest.
FIRM_TYPE_ORDER = [
    "financial-advisors", "private-funds", "hedge-funds", "broker-dealers",
    "service-partners", "asset-managers", "private-equity", "fintech",
]
for item in json.loads((CMS / "case-study-category.json").read_text())["items"]:
    write_json("firm-types", item["slug"], {
        "name": clean(item["name"]),
        "order": FIRM_TYPE_ORDER.index(item["slug"]) + 1,
    })

# --------------------------------------------------------------- solutions
SOLUTION_FIRM_TYPES = {
    "financial-advisors": "financial-advisors",
    "private-funds": "private-funds",
    "hedge-funds": "hedge-funds",
    "broker-dealers": "broker-dealers",
    "service-provider-platform": "service-partners",
}
SOLUTION_IMAGES = {
    "financial-advisors": "financial-advisors.jpg",
    "ria-registration": "registration.jpg",
    "private-funds": "private-funds.jpg",
    "hedge-funds": "hedge-funds.jpg",
    "broker-dealers": "broker-dealers.jpg",
    "service-provider-platform": "service-partners.jpg",
}
SOLUTION_ALTS = {
    "financial-advisors": "Two advisors reviewing a report together at a laptop",
    "ria-registration": "A team talking through a plan around a table",
    "private-funds": "A fund professional working at his desk",
    "hedge-funds": "A portfolio manager working on a laptop outdoors",
    "broker-dealers": "A hand pointing at a trading chart on a screen",
    "service-provider-platform": "A compliance consultant working at her laptop",
}
overview = {}
body = body_of(PAGES / "solutions.md")
for match in re.finditer(r"## ([^\n]+)\n\n([^\n]+)\n\n\[Link: Learn more\]\(/solutions/([\w-]+)\)", body):
    overview[match.group(3)] = (clean(match.group(1)), clean(match.group(2)))

for order, slug in enumerate(SOLUTION_IMAGES, 1):
    path = PAGES / "solutions" / f"{slug}.md"
    meta = front(path)
    secs = dict(sections(body_of(path)))
    hero = [l for l in lines(secs["hero_wrap"]) if not l.startswith("[Link")]
    title = clean(next(l for l in hero if l.startswith("# "))[2:])
    tagline = clean(next(l for l in hero if not l.startswith(("#", "!["))))
    benefits = []
    for line in lines(secs["benefits_wrap"]):
        if line.startswith("### "):
            benefits.append({"heading": clean(line[4:]), "text": ""})
        elif line.startswith("## "):
            continue
        else:
            benefits[-1]["text"] = clean(line)
    name, summary = overview[slug]
    write_json("solutions", slug, {
        "name": name,
        "title": title,
        "tagline": tagline,
        "summary": summary,
        "image": f"../../assets/images/solutions/{SOLUTION_IMAGES[slug]}",
        "imageAlt": SOLUTION_ALTS[slug],
        "order": order,
        **({"firmType": SOLUTION_FIRM_TYPES[slug]} if slug in SOLUTION_FIRM_TYPES else {}),
        "benefits": benefits,
        "seo": seo(meta, title),
    })

# ------------------------------------------------------------- comparisons
for path in sorted((PAGES / "compare").glob("*.md")):
    slug = path.stem
    meta = front(path)
    secs = dict(sections(body_of(path)))
    hero = lines(secs["hero_wrap"])
    logo_name = re.search(r"images/([^)]+)", next(l for l in hero if l.startswith("!["))).group(1)
    heading = clean(re.sub(r"^#+ ", "", next(l for l in hero if l.startswith("#"))))
    competitor = re.sub(r"^See why experts choose Greenboard over ", "", heading)
    solution = lines(secs["solution_wrap"])
    summary = clean(next(l for l in solution if not l.startswith(("#", "|"))))
    rows = []
    for line in solution:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if line.startswith("|") and cells[0] not in ("Feature",) and not set(cells[0]) <= set("-"):
            rows.append({"feature": clean(cells[0]), "greenboard": cells[1] == "yes", "competitor": cells[2] == "yes"})
    as_of = re.search(r"accurate as of (\d\d)/(\d\d)/(\d{4})", secs["testimonial_wrap"])
    write_json("comparisons", slug, {
        "competitor": clean(meta.get("webflow_page_title", competitor)),
        "heading": heading,
        "logo": copy_image(logo_name, "compare", slug),
        "summary": summary,
        "rows": rows,
        "asOf": f"{as_of.group(3)}-{as_of.group(1)}-{as_of.group(2)}",
        "status": "published" if meta.get("status") == "live" else "draft",
        "seo": seo(meta, heading),
    })

# ------------------------------------------------------------------ people
PEOPLE = {
    "dave-feldman": {"name": "Dave Feldman", "role": "Co-founder and CEO", "company": "Greenboard", "image": "../../assets/images/about/dave-feldman.jpg"},
    "ed-schembor": {"name": "Ed Schembor", "role": "Co-founder & CTO", "company": "Greenboard", "image": "../../assets/images/about/ed-schembor.jpg"},
    "katie-tumurbat": {"name": "Katie Tumurbat", "role": "Director of Marketing", "company": "Greenboard"},
    "cameron-burns": {"name": "Cameron Burns", "role": "Founding GTM & CS", "company": "Greenboard"},
    "pr-newswire": {"name": "PR Newswire", "role": "Press release"},
    "alex-stickelman": {"name": "Alex Stickelman", "role": "CCO & COO", "company": "Root Financial", "image": copy_image("alex-stickelman.jpeg", "people", "alex-stickelman")},
    "adam-boyer": {"name": "Adam Boyer", "role": "COO & CCO", "company": "JMG Financial Group", "image": copy_image("08be2ad0266a1e8fac8913ca71c09ffff0d2b6d4.jpg", "people", "adam-boyer")},
    "doug-thalhammer": {"name": "Doug Thalhammer", "role": "CCO", "company": "FSG", "image": copy_image("Doug-24.png", "people", "doug-thalhammer")},
    "steve-robinson": {"name": "Steve Robinson", "role": "Director of Technology and Logistics", "company": "FSG", "image": copy_image("Steve-21.png", "people", "steve-robinson")},
    "brook-powers": {"name": "Brook Powers", "role": "CEO", "company": "Fiduciary Financial"},
    "maranda-leonard": {"name": "Maranda Leonard", "role": "Director, Risk Management", "company": "S2 Capital"},
}
for slug, person in PEOPLE.items():
    write_json("people", slug, person)

# --------------------------------------------------------------- customers
clients = json.loads((CMS / "client.json").read_text())["items"]
PERSON_BY_NAME = {p["name"]: slug for slug, p in PEOPLE.items()}
for item in clients:
    if item["status"] != "published":
        continue
    f = item["fields"]
    data = {"name": fix(item["name"])}
    who = (f.get("testimonial-name") or "").strip()
    if who and f.get("testimonial"):
        data["testimonial"] = {
            "quote": clean(f["testimonial"]).strip('"“”'),
            "person": PERSON_BY_NAME[who],
        }
    write_json("customers", item["slug"], data)

print("typos fixed:", sorted(set(fixed)))
