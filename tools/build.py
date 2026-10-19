"""Dyrhald website - refresh the pages after you change something.

    python Website/tools/build.py                    (every release in the notes)
    python Website/tools/build.py --max-release 6    (leave out releases above 6, e.g. one still being finished)

1. Copies the game's release notes (Assets/Resources/ReleaseNotes.json) into data/ReleaseNotes.json, when the
   game folder is next door, and writes them into news.html (all releases) and index.html (the latest one).
2. Puts partials/header.html and partials/footer.html into every page, so the menu is the same everywhere.

It only rewrites what sits between the <!-- X:START --> and <!-- X:END --> markers in each page.
Plain Python 3, nothing to install.
"""
import html, json, os, re, shutil, sys
from datetime import date

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME_NOTES = os.path.join(os.path.dirname(SITE), "Assets", "Resources", "ReleaseNotes.json")
NOTES = os.path.join(SITE, "data", "ReleaseNotes.json")
PAGES = ["index.html", "world.html", "media.html", "news.html", "join.html", "faq.html", "404.html"]


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def fill(page, marker, body):
    pat = re.compile(r"(<!-- %s:START -->)(.*?)(<!-- %s:END -->)" % (marker, marker), re.S)
    if not pat.search(page):
        return page, False
    return pat.sub(lambda m: m.group(1) + "\n" + body.rstrip() + "\n" + m.group(3), page), True


def nice_date(s):
    try:
        d = date.fromisoformat(s)
        return d.strftime("%d %B %Y").lstrip("0")
    except ValueError:
        return s


def release_html(r, level=2):
    h, out = "h%d" % level, []
    out.append('<article class="release" id="release-%s">' % html.escape(str(r.get("id", ""))))
    out.append('  <header><%s>%s</%s><time datetime="%s">%s</time></header>'
               % (h, html.escape(r.get("title", "")), h, html.escape(r.get("date", "")), nice_date(r.get("date", ""))))
    for sec in r.get("sections", []):
        name = sec.get("name", "")
        out.append('  <h3 class="%s">%s</h3>' % (html.escape(name.lower()), html.escape(name)))
        out.append("  <ul>")
        for item in sec.get("items", []):
            out.append("    <li>%s</li>" % html.escape(item))
        out.append("  </ul>")
    out.append("</article>")
    return "\n".join(out)


def main():
    os.makedirs(os.path.dirname(NOTES), exist_ok=True)
    if os.path.exists(GAME_NOTES):
        shutil.copyfile(GAME_NOTES, NOTES)
        print("copied release notes from the game")
    releases = json.loads(read(NOTES)).get("releases", [])
    if "--max-release" in sys.argv:  # hold back notes for a release that isn't out yet
        top = int(sys.argv[sys.argv.index("--max-release") + 1])
        releases = [r for r in releases if int(r.get("id", 0)) <= top]
    releases.sort(key=lambda r: (r.get("date", ""), r.get("id", 0)), reverse=True)

    header = read(os.path.join(SITE, "partials", "header.html"))
    footer = read(os.path.join(SITE, "partials", "footer.html"))
    news_all = "\n".join(release_html(r) for r in releases) or "<p>No news yet.</p>"
    latest = release_html(releases[0], level=3) if releases else "<p>No news yet.</p>"

    for name in PAGES:
        path = os.path.join(SITE, name)
        if not os.path.exists(path):
            continue
        page = read(path)
        page, _ = fill(page, "HEADER", header)
        page, _ = fill(page, "FOOTER", footer)
        page, _ = fill(page, "NEWS", news_all)
        page, _ = fill(page, "LATEST", latest)
        write(path, page)
        print("built", name)
    print("%d release(s) on the news page" % len(releases))


if __name__ == "__main__":
    sys.exit(main())
