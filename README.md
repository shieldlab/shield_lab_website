# SHIELD Lab website

GitHub-ready static website exported from SHIELD Lab preview v161 (source revision `927e295e45fe1926ffc30e3372a5adaf25581800`). Includes the rendered site and the editable files used to maintain it. Nothing has been uploaded to GitHub or published from this package.

## Preview locally

Unzip the download, open a terminal in the extracted **SHIELD-Lab** folder (next to this README), and start a local server. No Node.js, package installation, or build is needed to preview.

**Windows PowerShell:**

```powershell
py -3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

**macOS or Linux:**

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Use the HTTP address instead of double-clicking an HTML file so the browser can load the news and publication catalogs. Press Ctrl+C to stop the server.

## Make edits

Use Python 3.10 or newer from the repository root. Commands below use `python3`; on Windows, use `py -3` instead. Keep the changed `data/` or `scripts/` files **and** the regenerated `dist/` files in the same commit. The supplied Pages workflow publishes the reviewed, committed output, not a fresh build.

| What to change | Edit | Rebuild |
| --- | --- | --- |
| Publications, author matching, topic tags, or venue ratings | `data/publications.json`, `data/members.json`, `data/publication-topics.json`, `data/venue-rankings.json` | `python3 scripts/build-publications.py` |
| News and homepage highlights | `data/news.json` | `python3 scripts/build-news.py` |
| Standalone Director grants | `data/director-additional-grants.json` | `python3 scripts/build-director-grants.py` |
| Course descriptions, offered semesters, project highlights | `data/courses.json` and `data/course-highlight-collections.json` | `python3 scripts/build-courses.py` |
| Member bios, research interests, approved profile links | `data/members.json` | `python3 scripts/build-members.py`; review the result and update `dist/team.html` if changing roster roles or groupings |
| Page layout, static sections, branding, or illustration | Matching HTML, CSS, JavaScript and assets in `dist/` | No build for direct edits outside generated sections |

- The publication build refreshes the bibliography, the shared data used on member pages, linked research-area publication lists, and the rolling three-year topic chart. The Director page does not show a publication list. Preserve stable publication IDs and verified author matches. A paper referenced by a course highlight also needs `build-courses.py` after its linked record changes.
- `archiveOnly: true` makes a news item visible on the News page but not in homepage Latest News. For events without an exact known date, use verified year/month precision. Photos go in `dist/assets/` with descriptive alt text in `data/news.json`.
- The site is intentionally hybrid: some HTML is hand-maintained and some sections are generated in place. Do not delete `dist/` expecting to rebuild the whole site from scratch. Rebuild only the area you changed and preview the diff. Research migration scripts and the bibliography importer are legacy tooling for intentional migrations, not routine publishing steps. The optional research formatting script uses Beautiful Soup 4; the preview and routine rebuilds use no third-party Python packages.

## Publish on GitHub Pages when ready

**Privacy:** The exported site was an owner-only preview. A private GitHub repository does not automatically make its Pages website private. If you want a private site, keep Pages disabled unless your account and organization explicitly support private Pages access. Review content and asset publication rights before making the repository or site public.

1. Create a repository under your account or organization, on the `main` branch. Upload the **contents** of the extracted folder, including the hidden `.github` folder, to the repository root. GitHub's web uploader may not reliably include hidden folders; Git or GitHub Desktop is recommended.
2. In the repository, open **Settings → Pages → Build and deployment → Source → GitHub Actions**. The included workflow is `.github/workflows/pages.yml`. It uploads only `dist/`.
3. Open **Actions → Publish SHIELD Lab to GitHub Pages → Run workflow**, select `main`, or push a new commit to `main`. When deployment succeeds, use the Pages URL shown under **Settings → Pages**. For a project repository, the normal address includes the repository name: `https://OWNER.github.io/REPOSITORY/`. Relative links in the site support that subpath.
4. After deployment, open the homepage and test Publications filters, a member profile, and a course page. If your default branch is not `main`, update both the workflow branch trigger and its ref guard before using it.

If uploading via Git to a new empty GitHub repository:

```sh
git init -b main
git add .
git commit -m "Add SHIELD Lab website"
git remote add origin https://github.com/OWNER/REPOSITORY.git
git push -u origin main
```

Those commands upload files to the named repository; run them only after confirming the repository destination and visibility. [GitHub Pages publishing guide](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Export boundaries

The ZIP omits the hidden Collaborations draft and its exclusive assets, unused original team portraits, internal research/evidence notes, cached bytecode, Git history and private preview hosting configuration. It contains no original CVs, syllabi or signed certificates. The ICTAI paper PDF already linked in the approved preview remains to preserve paper links. Existing site portraits, news photos, figures and logos are included for this website; the export does not grant separate redistribution rights.
# shield_lab_website
