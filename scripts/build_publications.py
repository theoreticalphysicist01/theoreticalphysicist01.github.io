#!/usr/bin/env python3
"""Generate semantic publication HTML from data/publications.json."""

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "publications.json"
OWNER_NAMES = {"Zeng-Zhao Li", "Z.-Z. Li"}


def author_list(authors):
    marked = []
    for name in authors:
        escaped = html.escape(name)
        bare_name = name.rstrip("*").strip()
        marked.append(f"<strong>{escaped}</strong>" if bare_name in OWNER_NAMES else escaped)
    if len(marked) < 2:
        return "".join(marked)
    return ", ".join(marked[:-1]) + " and " + marked[-1]


def entry(pub, indent, number=None):
    title_url = pub.get("journal_url") or pub.get("doi") or pub.get("arxiv") or pub.get("pdf")
    title = html.escape(pub["title"])
    title_html = f'<a href="{html.escape(title_url, quote=True)}">{title}</a>' if title_url else title
    bits = [str(pub.get(key, "")) for key in ("journal", "volume", "pages") if pub.get(key)]
    venue = f'{html.escape(", ".join(bits))} ({pub["year"]})'
    links = []
    for label, key in (("DOI", "doi"), ("Journal", "journal_url"), ("arXiv", "arxiv"), ("PDF", "pdf")):
        if pub.get(key):
            url = html.escape(pub[key], quote=True)
            links.append(f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>')
    number_html = f'<span class="publication-number">{number}.</span> ' if number is not None else ""
    lines = [
        f'{indent}<article class="publication">',
        f'{indent}  <h3>{number_html}{title_html}</h3>',
        f'{indent}  <p class="authors">{author_list(pub["authors"])}</p>',
        f'{indent}  <p class="venue">{venue}</p>',
    ]
    if links:
        lines.append(f'{indent}  <div class="citation-links">{"".join(links)}</div>')
    if pub.get("note"):
        lines.append(f'{indent}  <p class="publication-note">{html.escape(pub["note"])}</p>')
    lines.append(f'{indent}</article>')
    return "\n".join(lines)


def selected_markup(publications):
    return "\n".join(entry(pub, "        ") for pub in publications if pub.get("selected"))


def all_markup(publications):
    groups = []
    numbered = [(pub, len(publications) - index) for index, pub in enumerate(publications)]
    years = sorted({pub["year"] for pub in publications}, reverse=True)
    for year in years:
        items = "\n".join(entry(pub, "          ", number) for pub, number in numbered if pub["year"] == year)
        groups.append(
            f'      <section class="year-group" aria-labelledby="year-{year}">\n'
            f'        <h2 id="year-{year}">{year}</h2>\n'
            f'        <div class="publication-list">\n{items}\n        </div>\n'
            f'      </section>'
        )
    return "\n".join(groups)


def replace_block(path, name, markup):
    text = path.read_text(encoding="utf-8")
    pattern = rf"(?P<start><!-- PUBLICATIONS:{name}:START -->).*?(?P<end><!-- PUBLICATIONS:{name}:END -->)"
    updated, count = re.subn(pattern, rf"\g<start>\n{markup}\n        \g<end>", text, flags=re.DOTALL)
    if count != 1:
        raise RuntimeError(f"Expected one {name} publication block in {path}")
    path.write_text(updated, encoding="utf-8")


def replace_summary(path, publications):
    text = path.read_text(encoding="utf-8")
    summary = f'{len(publications)} publications · {min(pub["year"] for pub in publications)}–{max(pub["year"] for pub in publications)}'
    pattern = r"(?P<start><!-- PUBLICATIONS:SUMMARY:START -->).*?(?P<end><!-- PUBLICATIONS:SUMMARY:END -->)"
    updated, count = re.subn(pattern, rf"\g<start>{summary}\g<end>", text)
    if count != 1:
        raise RuntimeError(f"Expected one publication summary block in {path}")
    path.write_text(updated, encoding="utf-8")


def main():
    publications = json.loads(DATA.read_text(encoding="utf-8"))
    publications.sort(key=lambda pub: (-pub["year"], pub["title"].casefold()))
    replace_block(ROOT / "index.html", "SELECTED", selected_markup(publications))
    replace_block(ROOT / "publications.html", "ALL", all_markup(publications))
    replace_summary(ROOT / "publications.html", publications)
    print(f"Generated {sum(bool(p.get('selected')) for p in publications)} selected and {len(publications)} total publications.")


if __name__ == "__main__":
    main()
