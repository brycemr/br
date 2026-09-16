#!/usr/bin/env python3
"""Build the resume: resume.md -> resume.html -> PDF.

Zero third-party dependencies. Needs Python 3.8+ and a Chrome/Chromium binary
for the PDF step (HTML is always written, so you can also just open it and
print to PDF from the browser).

    python3 build.py                  # html + pdf
    python3 build.py --html-only      # skip the PDF step
    python3 build.py --chrome /path/to/chrome

The markdown subset understood here is deliberately small, because that is all
the resume uses:

    ---            YAML-ish frontmatter (name, tagline, contact fields)
    ## Section     section heading
    ### Title      entry heading (job, degree)
    plain line     the line right after ### is the entry's meta line
    - item         bullet
    **bold**       bold
    *italic*       italic
"""

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "resume.md"
CSS = HERE / "style.css"
OUT_HTML = HERE / "resume.html"
OUT_PDF = HERE.parent / "Bryce Richard's Resume.pdf"

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    "google-chrome",
    "chromium",
    "chromium-browser",
]


def split_frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw, body = text[3:end], text[end + 4 :]
    meta = {}
    for line in raw.strip().splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta, body.lstrip("\n")


def inline(text):
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", text)
    return text


def render_body(body):
    # Join soft-wrapped lines. A line continues the previous one when both are
    # non-empty, the new line does not open a block, and the previous line is
    # not a heading (so an entry's meta line stays on its own).
    joined = []
    for line in body.splitlines():
        stripped = line.strip()
        previous = joined[-1] if joined else ""
        is_continuation = (
            stripped
            and previous
            and not stripped.startswith(("#", "-", "|"))
            and not previous.startswith("#")
        )
        if is_continuation:
            joined[-1] = previous.rstrip() + " " + stripped
        else:
            joined.append(stripped)

    out, in_list, pending_meta = [], False, False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for line in joined:
        if not line:
            close_list()
            pending_meta = False
            continue
        if line.startswith("### "):
            close_list()
            out.append(f'<h3>{inline(line[4:])}</h3>')
            pending_meta = True
            continue
        if line.startswith("## "):
            close_list()
            out.append(f'<h2>{inline(line[3:])}</h2>')
            pending_meta = False
            continue
        if line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(line[2:])}</li>")
            pending_meta = False
            continue
        close_list()
        css_class = "meta" if pending_meta else "para"
        out.append(f'<p class="{css_class}">{inline(line)}</p>')
        pending_meta = False

    close_list()
    return "\n".join(out)


def render_header(meta):
    contact_keys = ["location", "email", "phone", "portfolio", "github", "linkedin"]
    parts = []
    for key in contact_keys:
        value = meta.get(key)
        if not value:
            continue
        if key in ("portfolio", "github", "linkedin"):
            href = value if value.startswith("http") else "https://" + value
            parts.append(f'<a href="{html.escape(href)}">{html.escape(value)}</a>')
        elif key == "email":
            parts.append(f'<a href="mailto:{html.escape(value)}">{html.escape(value)}</a>')
        else:
            parts.append(html.escape(value))
    tagline = meta.get("tagline", "")
    return (
        f'<header>\n<h1>{html.escape(meta.get("name", ""))}</h1>\n'
        + (f'<p class="tagline">{html.escape(tagline)}</p>\n' if tagline else "")
        + '<p class="contact">' + '<span class="sep">·</span>'.join(parts) + "</p>\n</header>"
    )


def find_chrome(explicit=None):
    if explicit:
        return explicit if Path(explicit).exists() or shutil.which(explicit) else None
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
        found = shutil.which(candidate)
        if found:
            return found
    return None


def to_pdf(html_path, pdf_path, chrome):
    with tempfile.TemporaryDirectory() as profile:
        subprocess.run(
            [
                chrome,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                f"--user-data-dir={profile}",
                "--no-pdf-header-footer",
                f"--print-to-pdf={pdf_path}",
                html_path.as_uri(),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--html-only", action="store_true")
    parser.add_argument("--chrome", default=os.environ.get("CHROME_BIN"))
    args = parser.parse_args()

    meta, body = split_frontmatter(SRC.read_text(encoding="utf-8"))
    page = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        f"<title>{html.escape(meta.get('name', 'Resume'))}</title>\n"
        f"<style>\n{CSS.read_text(encoding='utf-8')}\n</style>\n</head>\n<body>\n"
        f"{render_header(meta)}\n<main>\n{render_body(body)}\n</main>\n</body>\n</html>\n"
    )
    OUT_HTML.write_text(page, encoding="utf-8")
    print(f"wrote {OUT_HTML}")

    if args.html_only:
        return 0

    chrome = find_chrome(args.chrome)
    if not chrome:
        print(
            "No Chrome/Chromium found. The HTML is written — open it and print to PDF,\n"
            "or pass --chrome /path/to/chrome.",
            file=sys.stderr,
        )
        return 1
    to_pdf(OUT_HTML, OUT_PDF, chrome)
    print(f"wrote {OUT_PDF}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
