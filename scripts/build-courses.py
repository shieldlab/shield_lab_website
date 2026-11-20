"""Render the Director's Teaching links and dedicated course pages from data/courses.json."""
import html
import json
from pathlib import Path
import re

root = Path("dist")
courses = json.loads(Path("data/courses.json").read_text())
collections = json.loads(Path("data/course-highlight-collections.json").read_text())
publications = {p["index"]: p for p in json.loads(Path("data/publications.json").read_text())}
director = root / "director.html"
original = director.read_text()
template = (root / "join.html").read_text()
split = re.fullmatch(r"(.*?<main>).*?(</main>.*)", template, re.S)
assert split
head, tail = split.groups()
e = html.escape
assert len({c["slug"] for c in courses}) == len(courses)
mapping = {}
course_index = {c["slug"]: c for c in courses}

def render_list(items):
    return "<ul>" + "".join(f"<li>{e(text)}</li>" for text in items) + "</ul>"

def render_project(project):
    title = e(project["title"])
    description = f'<p>{e(project["description"])}</p>' if project.get("description") else ""
    linked = ""
    if "publicationId" in project:
        pub = publications[project["publicationId"]]
        assert pub["url"].startswith("https://")
        linked = f' <span>· <a class="text-link" href="{e(pub["url"], quote=True)}">{e(pub["type"])}: {e(pub["title"])}</a></span>'
    return f'<li>{title}{linked}{description}</li>'

for c in courses:
    assert re.fullmatch(r"[a-z0-9-]+", c["slug"])
    assert c.get("credits") in (None, 1, 2, 3, 4)
    filename = f'course-{c["slug"]}.html'
    for code in c["directorCodes"]:
        assert code not in mapping
        mapping[code] = (filename, c["title"])
    page_title = e(c["title"])
    profile = head.replace("<title>Join | SHIELD Lab</title>", f"<title>{page_title} | SHIELD Lab</title>")
    profile = profile.replace('<main>', '<main class="course-page">')
    profile = profile.replace('</head>', '<link rel="stylesheet" href="course-pages.css"></head>')
    metadata = [c["level"]]
    if c.get("credits"):
        metadata.append(f'{c["credits"]} credits')
    subtitle = "".join(f"<li>{e(label)}</li>" for label in metadata)
    offered = c["offered"]
    assert offered and len(offered) == len(set(offered))
    assert all(re.fullmatch(r"(Spring|Summer|Fall) [0-9]{4}", term) for term in offered)
    offered_line = f'<p class="course-offered"><strong>Offered:</strong> {e(", ".join(offered))}</p>'
    header = f'<section class="page-intro course-intro"><a class="text-link" href="director.html#teaching">Back to Teaching &amp; Experience</a><p class="course-code">{e(c["code"])}</p><h1>{page_title}</h1><ul class="course-facts" aria-label="Course details">{subtitle}</ul>{offered_line}<p>{e(c["overview"])}</p></section>'
    panels = (f'<div class="course-panels"><section class="section"><h2>Selected Topics</h2>{render_list(c["topics"])}</section>'
              f'<section class="section"><h2>Learning Objectives</h2>{render_list(c["objectives"])}</section></div>')
    related = ""
    if c.get("related"):
        targets = [course_index[slug] for slug in c["related"]]
        links = "".join(f'<li><a class="text-link" href="course-{e(t["slug"], quote=True)}.html">{e(t["code"])} · {e(t["title"])}</a></li>' for t in targets)
        related = f'<section class="section"><h2>Related Course</h2><ul>{links}</ul></section>'
    practice = f'<section class="section"><h2>Coursework &amp; Projects</h2><p>{e(c["practice"])}</p></section>'
    highlights = ""
    shared_key = c.get("highlightCollection")
    groups = collections[shared_key] if shared_key else c.get("highlights", [])
    if groups:
        terms = []
        for term in groups:
            projects = "".join(render_project(project) for project in term["projects"])
            context = f'<p>{e(term["context"])}</p>' if term.get("context") else ""
            terms.append(f'<h3>{e(term["term"])}</h3>{context}<ul>{projects}</ul>')
        highlights = '<section class="section" id="student-project-highlights"><h2>Student Project Highlights</h2>' + "".join(terms) + '</section>'
    (root / filename).write_text(profile + header + panels + practice + related + highlights + tail)

matched = set()
def add_links(match):
    def add_item(m):
        code, _ = m.groups()
        if code not in mapping:
            return m.group()
        matched.add(code)
        target, title = mapping[code]
        return f'<li><a class="text-link director-course-link" href="{e(target, quote=True)}"><strong>{code}</strong> · {e(title)}</a></li>'
    result = re.sub(r'<li>(?:<a class="text-link director-course-link" href="[^"]+">)?<strong>([^<]+)</strong> · ([^<]+)(?:</a>)?</li>', add_item, match[2])
    return match[1] + result + match[3]

updated, n = re.subn(r'(<ul class="director-course-list">)(.*?)(</ul>)', add_links, original, flags=re.S)
assert n == 1 and matched == set(mapping), f"Missing Director codes: {set(mapping) - matched}"
director.write_text(updated)
print(f"Rendered {len(courses)} course pages and linked {len(mapping)} Director entries.")
