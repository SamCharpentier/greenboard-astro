"""Case studies and blog posts -> Markdown entries with Sanity-shaped front matter."""
import json, re, shutil
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
    "Reponse Times": "Response Times",
    "their[company blog]": "their [company blog]",
    "channels.**In 2025": "channels.** In 2025",
    "Michel Kitces": "Michael Kitces",
    "$677 AUM": "$677M AUM",
    "**Trade Surveillance**No more": "**Trade Surveillance** No more",
    "announce the **The Trust Podcast**": "announce **The Trust Podcast**",
    "![__wf_reserved_inherit](": "![](",
}
fixed = []


def fix(text):
    for bad, good in TYPOS.items():
        if bad in text:
            fixed.append(bad)
            text = text.replace(bad, good)
    return text


def clean(text):
    # Webflow pads empty rich-text blocks with a zero-width joiner, which the
    # Markdown export leaves stuck to the asterisks around it, and a bold run
    # emptied that way leaves four asterisks behind
    text = text.replace("\u200d", "").replace("****", "")
    return fix(re.sub(r"[​ ]+", " ", text)).strip()


def yaml_value(value):
    return json.dumps(value, ensure_ascii=False)


def front_matter(data):
    out = ["---"]

    def emit(key, value, indent=""):
        if isinstance(value, dict):
            out.append(f"{indent}{key}:")
            for k, v in value.items():
                emit(k, v, indent + "  ")
        elif isinstance(value, list):
            out.append(f"{indent}{key}:")
            for item in value:
                if isinstance(item, dict):
                    first = True
                    for k, v in item.items():
                        prefix = f"{indent}  - " if first else f"{indent}    "
                        out.append(f"{prefix}{k}: {yaml_value(v)}")
                        first = False
                else:
                    out.append(f"{indent}  - {yaml_value(item)}")
        else:
            out.append(f"{indent}{key}: {yaml_value(value)}")

    for key, value in data.items():
        emit(key, value)
    out.append("---")
    return "\n".join(out) + "\n\n"


PEOPLE = {
    "Alex Stickelman": "alex-stickelman",
    "Adam Boyer": "adam-boyer",
    "Doug Thalhammer": "doug-thalhammer",
    "Steve Robinson": "steve-robinson",
    "Dave Feldman": "dave-feldman",
    "Ed Schembor": "ed-schembor",
    "Katie Tumurbat": "katie-tumurbat",
    "Cameron Burns": "cameron-burns",
    "PR Newswire": "pr-newswire",
}

# ------------------------------------------------------------- case studies
CASES = {
    "root-financial": ("Root Financial", "root-logo.svg"),
    "jmg-financial-group": ("JMG Financial Group", "jmg-financial-group.webp"),
    "fsg-ica": ("FSG and ICA", "fsg-logo-final-transparent.png"),
}
FACT_LABELS = ["Company Size", "Company", "Industry", "Solution", "Location", "Consulting Partner"]
cards = {i["slug"]: i for i in json.loads((CMS / "case-study.json").read_text())["items"]}


def is_number(line):
    return re.fullmatch(r"\**([$]?[\d,.]+[A-Z]?[%+]*( hours)?|Same Day)\**", line.strip()) is not None


def pull_quote(text, person_line, role_line):
    quote = clean(re.sub(r"\*+", "", text)).strip()
    quote = "“" + quote.strip('"“”') + "”"
    quote = re.sub(r"that(advisors)", r"that \1", quote)
    return [f"> {quote}", ">", f"> <cite>{person_line.strip()}, {role_line.strip()}</cite>"]


for slug, (customer, logo) in CASES.items():
    raw = (PAGES / "case-studies" / f"{slug}.md").read_text()
    head, body = raw.split("---", 2)[1:]
    meta = {}
    for line in head.strip().splitlines():
        key, value = line.split(":", 1)
        value = value.strip()
        meta[key.strip()] = json.loads(value) if value.startswith('"') else value
    parts = re.split(r"<!-- section: ([\w-]+) -->", body)
    secs = [parts[i + 1] for i in range(1, len(parts), 2)]
    hero = [l.strip() for l in secs[0].splitlines() if l.strip()]
    title_index = next(i for i, l in enumerate(hero) if l.startswith("# "))
    title = clean(hero[title_index][2:].strip("*"))
    stats = []
    for line in hero[title_index + 1:]:
        if is_number(line):
            value = line.strip("*")
            number, unit = (value.split(" ", 1) + [None])[:2] if value != "Same Day" else (value, None)
            stat = {"number": number}
            if unit:
                stat["unit"] = unit
            stat["label"] = ""
            stats.append(stat)
        else:
            stats[-1]["label"] = clean(f"{stats[-1]['label']} {line}")
    value_lines = [l.rstrip() for l in secs[1].splitlines() if l.strip()]
    summary = clean(value_lines[1])
    facts = []
    for line in value_lines[2:]:
        if line.strip() in FACT_LABELS:
            facts.append({"label": line.strip(), "value": ""})
        else:
            facts[-1]["value"] = clean((facts[-1]["value"] + "\n" + clean(line)).strip())

    story = secs[2]
    story = story.split("![](images/Favicon-2-3-1.png)")[0]
    story_lines = story.splitlines()
    start = next(i for i, l in enumerate(story_lines) if l.startswith(("*", "#")) and "Table of Contents" not in l)
    story_lines = story_lines[start:]
    out, featured = [], None
    i = 0
    content_lines = [l for l in story_lines]
    while i < len(content_lines):
        line = content_lines[i].rstrip()
        if re.match(r"^\*[“\"]", line):
            rest = [l for l in content_lines[i + 1:i + 12] if l.strip()]
            j = 1 if rest and rest[0].startswith("![") else 0
            if len(rest) < j + 2 or rest[j].strip() not in PEOPLE:
                out.append(clean(line))
                i += 1
                continue
            person, role = rest[j], rest[j + 1]
            block = pull_quote(line, person, role)
            if featured is None and not any(l.startswith("#") for l in out):
                featured = {"text": re.sub(r"^[“\"]|[”\"]$", "", block[0][2:]).strip(), "person": PEOPLE[person.strip()]}
            else:
                out.extend(block)
                out.append("")
            consumed = 0
            count = 0
            k = i + 1
            while count < j + 2:
                if content_lines[k].strip():
                    count += 1
                k += 1
            i = k
            continue
        heading = re.match(r"^(#{2,4}) \**(.+?)\**\s*$", line)
        if heading:
            level = {"##": "##", "###": "##", "####": "###"}[heading.group(1)]
            # A heading is bold already, so a bold run left open inside it goes
            out.append(f"{level} {clean(heading.group(2)).strip('*').strip()}")
        elif re.fullmatch(r"\*\*[^*]{3,90}\*\*", line.strip()):
            out.append(f"### {clean(line.strip()[2:-2])}")
        else:
            out.append(clean(line) if line.strip() else "")
        i += 1
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"

    card = cards[slug]["fields"]
    data = {
        "title": title,
        "customer": customer,
        "firmType": card["category-2"]["slug"],
        "logo": f"../../assets/images/case-studies/{slug}{Path(logo).suffix}",
        "summary": summary,
        "excerpt": clean(card["short-description"]),
        "stats": stats,
        "facts": facts,
    }
    # The headline figure on the story's card
    point = clean(card["data-point-1"])
    number, _, unit = point.partition(" ")
    data["highlight"] = {"number": number, **({"unit": unit} if unit else {}), "label": clean(card["data-point-1-description"])}
    who = card["quote-person-name"]["markdown"].split("\n")[0].strip()
    data["quote"] = {"text": clean(card["quote"]).strip('"“” '), "person": PEOPLE[who]}
    data["date"] = card["date-sort-order"][:10]
    seo = {"title": clean(meta["seo_title"]), "description": clean(meta["seo_description"])}
    if "noindex" in meta.get("robots", ""):
        seo["noindex"] = True
    data["seo"] = seo
    dest = ASSETS / "case-studies" / f"{slug}{Path(logo).suffix}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SITE_IMG / logo, dest)
    path = CONTENT / "case-studies" / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(front_matter(data) + text)

# ------------------------------------------------------------------- posts
posts = {i["slug"]: i for i in json.loads((CMS / "blog.json").read_text())["items"]}
for md in sorted((CMS / "blog").glob("*.md")):
    slug = md.stem
    item = posts[slug]
    f = item["fields"]
    body = md.read_text().split("---", 2)[2]
    body = body.replace("## [Post Body]", "", 1)
    out = []
    for line in body.splitlines():
        heading = re.match(r"^(#{1,4}) \**(.+?)\**\s*$", line)
        video = re.match(r"^\[Video embed: (\S+)\]$", line.strip())
        if heading:
            level = "##" if heading.group(1) == "#" else heading.group(1)
            # A heading is bold already, so a bold run left open inside it goes
            out.append(f"{level} {clean(heading.group(2)).strip('*').strip()}")
        elif video:
            out.append(f'<iframe src="{video.group(1)}" title="{clean(item["name"])}" loading="lazy" allow="fullscreen; picture-in-picture"></iframe>')
        elif re.fullmatch(r"\*\*[^*\[\]]{3,90}\*\*", line.strip()):
            out.append(f"## {clean(line.strip()[2:-2])}")
        else:
            out.append(clean(line) if line.strip() else "")
    # Webflow tables end in empty rows, and a stray divider row among them
    tidy, header_seen = [], False
    for line in out:
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else None
        if cells is None:
            header_seen = False
            tidy.append(line)
        elif not any(cells):
            continue
        elif set("".join(cells)) <= set("-: "):
            if not header_seen:
                tidy.append(line)
                header_seen = True
        else:
            tidy.append(line)
    out = tidy
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    # An attribution line under a quote joins it as a <cite>, as in the case studies
    text = re.sub(r"((?:^>.*\n)+)\n— (.+)$", lambda m: f"{m.group(1)}>\n> <cite>{m.group(2).strip()}</cite>", text, flags=re.M)
    # Links to pages of this site stay relative, so they work on any host
    text = text.replace("](https://www.greenboard.com/", "](/")
    author = f.get("author") or {}
    data = {
        "title": clean(item["name"]),
        "summary": clean(f.get("post-summary") or ""),
        "date": (f.get("date") or item["published"])[:10],
        "author": PEOPLE[author["name"]] if author else None,
        "featured": bool(f.get("featured")),
        "whitepaperForm": bool(f.get("turn-on-for-whitepaper-form")),
    }
    # Covers come from the design files, since the Webflow CDN is out of reach here
    if (ASSETS / "blog" / f"{slug}.jpg").exists():
        data["cover"] = f"../../assets/images/blog/{slug}.jpg"
    cover = (f.get("main-cover") or f.get("thumbnail-image") or {}).get("url")
    if cover:
        data["coverUrl"] = cover
    data["status"] = "published" if item["status"] == "published" else "draft"
    data["seo"] = {"description": clean(f.get("meta-description") or f.get("post-summary") or "")}
    data = {k: v for k, v in data.items() if v is not None}
    path = CONTENT / "posts" / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(front_matter(data) + text)

# ---------------------------------------------------------------- partners
from wordmark import wordmark_svg

for item in json.loads((CMS / "partners-category.json").read_text())["items"]:
    path = CONTENT / "partner-categories" / f"{item['slug']}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"name": clean(item["name"]), "order": item["fields"]["sort"]}
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

LOGO_TYPES = (".svg", ".png", ".webp", ".jpg")
wordmarks = []
for item in json.loads((CMS / "partners.json").read_text())["items"]:
    if item["status"] == "archived":
        continue
    slug, f = item["slug"], item["fields"]
    name = clean(item["name"])
    body = (CMS / "partners" / f"{slug}.md").read_text().split("---", 2)[2]
    body = body.replace("## [Content]", "", 1).replace("\u200d", "")
    out = []
    for line in body.splitlines():
        # Webflow wrote each list item as its own paragraph opening with a middle dot
        bullet = re.match(r"^\s*·\s+(.+)$", line)
        if bullet:
            if out and out[-1] == "" and len(out) > 1 and out[-2].startswith("- "):
                out.pop()
            out.append(f"- {clean(bullet.group(1))}")
        else:
            out.append(clean(line) if line.strip() else "")
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"
    text = re.sub(r"(^[^-\n].*\n)(- )", r"\1\n\2", text, flags=re.M)
    # The real logo when it is in the repo, otherwise the name set as a stand-in
    real = next((ASSETS / "partners" / f"{slug}{ext}" for ext in LOGO_TYPES if (ASSETS / "partners" / f"{slug}{ext}").exists()), None)
    if real:
        logo = f"../../assets/images/partners/{real.name}"
    else:
        mark = ASSETS / "partners" / "wordmarks" / f"{slug}.svg"
        mark.parent.mkdir(parents=True, exist_ok=True)
        mark.write_text(wordmark_svg(name))
        logo = f"../../assets/images/partners/wordmarks/{slug}.svg"
        wordmarks.append(slug)
    category = f.get("category") or {}
    data = {
        "name": name,
        "category": category.get("slug") if isinstance(category, dict) else category,
        "logo": logo,
        "logoUrl": (f.get("logo") or {}).get("url"),
        "summary": clean(f.get("short-description") or ""),
        "website": f.get("website"),
        "status": "published" if item["status"] == "published" else "draft",
        "seo": {
            "title": f"{name} Partners With Greenboard",
            "description": clean(f.get("short-description") or ""),
        },
    }
    data = {k: v for k, v in data.items() if v is not None}
    path = CONTENT / "partners" / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(front_matter(data) + text)
print("partner logos still set as wordmarks:", wordmarks)

print("typos fixed:", sorted(set(fixed)))
