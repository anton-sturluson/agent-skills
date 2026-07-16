#!/usr/bin/env python3
"""Fetch or read article-like HTML, extract the main content, clean it, and save readable markdown/text.

Examples:
  clean_article_html.py --out-dir /tmp/archive https://example.com/article
  clean_article_html.py --out-dir /tmp/archive page.html another-page.html --update-index --update-manifest
"""

from __future__ import annotations

import argparse
import datetime as dt
import html as html_lib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

UA = "Mozilla/5.0 (compatible; article-archive-cleaner/1.0)"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"&", " and ", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-") or "article"


def fetch_url(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as response:
        content_type = response.headers.get("Content-Type", "")
        charset = response.headers.get_content_charset() or "utf-8"
        data = response.read()
    try:
        return data.decode(charset, "ignore")
    except LookupError:
        return data.decode("utf-8", "ignore")


def read_local(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_title(page_html: str, fallback: str = "Article") -> str:
    patterns = [
        r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\'](.*?)["\']',
        r'<meta[^>]+name=["\']twitter:title["\'][^>]+content=["\'](.*?)["\']',
        r'<title[^>]*>(.*?)</title>',
        r'<h1[^>]*>(.*?)</h1>',
    ]
    for pattern in patterns:
        match = re.search(pattern, page_html, flags=re.I | re.S)
        if match:
            title = strip_tags(match.group(1))
            if title:
                return title
    return fallback


def extract_embedded_body(page_html: str) -> Tuple[Optional[str], Optional[str]]:
    patterns = [
        ("substack-body-html", r'body_html\\":\\"((?:\\.|[^"\\])*)\\"', "html"),
        ("articleBody-json", r'"articleBody"\s*:\s*"((?:\\.|[^"\\])*)"', "text"),
    ]
    for name, pattern, kind in patterns:
        match = re.search(pattern, page_html, flags=re.I | re.S)
        if not match:
            continue
        raw = match.group(1)
        try:
            value = json.loads('"' + raw + '"')
        except json.JSONDecodeError:
            continue
        if kind == "text":
            paras = [p.strip() for p in re.split(r"\n{2,}", value) if p.strip()]
            html = "".join(f"<p>{html_lib.escape(p)}</p>" for p in paras)
        else:
            html = value
        if html.strip():
            return name, html
    return None, None


def extract_structural_block(page_html: str, mode: str) -> Tuple[str, str]:
    if mode in {"embedded"}:
        name, html = extract_embedded_body(page_html)
        if html:
            return name or "embedded", html
        return "body", extract_body(page_html)

    if mode == "article":
        html = first_block(page_html, "article") or extract_body(page_html)
        return "article", html
    if mode == "main":
        html = first_block(page_html, "main") or extract_body(page_html)
        return "main", html
    if mode == "body":
        wiki = extract_wikipedia_content(page_html)
        if wiki:
            return "wikipedia-content", wiki
        td = extract_largest_td(page_html)
        if td:
            return "largest-td", td
        return "body", extract_body(page_html)

    name, html = extract_embedded_body(page_html)
    if html:
        return name or "embedded", html

    wiki = extract_wikipedia_content(page_html)
    if wiki:
        return "wikipedia-content", wiki

    for tag in ("article", "main"):
        block = first_block(page_html, tag)
        if block:
            return tag, block

    td = extract_largest_td(page_html)
    if td:
        return "largest-td", td

    return "body", extract_body(page_html)


def extract_wikipedia_content(page_html: str) -> Optional[str]:
    if "wikipedia.org" not in page_html and "mw-content-text" not in page_html:
        return None

    start = -1
    for token in ['<div id="mw-content-text"', 'class="mw-content-ltr mw-parser-output"']:
        start = page_html.find(token)
        if start != -1:
            break
    if start == -1:
        return None

    end_candidates = []
    for token in [
        'id="References"',
        'id="Notes"',
        'id="External_links"',
        'id="Further_reading"',
        'id="Bibliography"',
        'id="Sources"',
        'id="catlinks"',
    ]:
        pos = page_html.find(token, start)
        if pos != -1:
            end_candidates.append(pos)

    end = min(end_candidates) if end_candidates else len(page_html)
    return page_html[start:end]


def extract_largest_td(page_html: str, min_text_length: int = 800) -> Optional[str]:
    body = extract_body(page_html)
    best_fragment = None
    best_len = 0
    for match in re.finditer(r"<td\b[^>]*>(.*?)</td>", body, flags=re.I | re.S):
        fragment = match.group(1)
        text_len = len(strip_tags(fragment))
        if text_len > best_len:
            best_len = text_len
            best_fragment = fragment
    if best_fragment and best_len >= min_text_length:
        return best_fragment
    return None


def first_block(page_html: str, tag: str) -> Optional[str]:
    match = re.search(rf"<{tag}\b[^>]*>(.*?)</{tag}>", page_html, flags=re.I | re.S)
    return match.group(1) if match else None


def extract_body(page_html: str) -> str:
    match = re.search(r"<body\b[^>]*>(.*?)</body>", page_html, flags=re.I | re.S)
    return match.group(1) if match else page_html


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = html_lib.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def simplify_html(fragment: str, source: str = "", extractor: str = "") -> str:
    fragment = fragment.replace('\\"', '"')
    fragment = html_lib.unescape(fragment)
    fragment = re.sub(r"<!--.*?-->", "", fragment, flags=re.S)
    base_url = source if urllib.parse.urlparse(source).scheme in {"http", "https"} else ""

    def normalize_anchor(match: re.Match[str]) -> str:
        href = match.group(1).strip()
        label = match.group(2)
        if base_url:
            href = urllib.parse.urljoin(base_url, href)
        return f'<a href="{html_lib.escape(href, quote=True)}">{label}</a>'

    fragment = re.sub(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', normalize_anchor, fragment, flags=re.I | re.S)

    fragment = re.sub(r"<sup[^>]*>(.*?)</sup>", r"^\1", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<sub[^>]*>(.*?)</sub>", r"_\1", fragment, flags=re.I | re.S)

    fragment = re.sub(r"<(script|style|noscript|iframe|svg|canvas|button|form|map|picture|audio|video)[^>]*>.*?</\1>", "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"</?(nav|aside|footer)\b[^>]*>.*?</\1>", "", fragment, flags=re.I | re.S)
    fragment = re.sub(r'<div class="digest-post-embed"[^>]*></div>', "", fragment, flags=re.I | re.S)
    fragment = re.sub(r'<a\b[^>]*class="[^"]*button[^"]*"[^>]*>.*?</a>', "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<link\b[^>]*>", "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<area\b[^>]*>", "", fragment, flags=re.I | re.S)

    fragment = re.sub(r'<div\b[^>]*(class|id)="[^"]*(shortdescription|mw-editsection|catlinks|toc|navbox|authority-control|sistersitebox|side-box|mw-references-wrap|reflist|thumb|metadata)[^"]*"[^>]*>.*?</div>', "", fragment, flags=re.I | re.S)
    fragment = re.sub(r'<table\b[^>]*(class|id)="[^"]*(infobox|navbox|toc|metadata)[^"]*"[^>]*>.*?</table>', "", fragment, flags=re.I | re.S)
    fragment = re.sub(r'<div\b[^>]*class="[^"]*hatnote[^"]*"[^>]*>.*?</div>', "", fragment, flags=re.I | re.S)

    def replace_figure(match: re.Match[str]) -> str:
        block = match.group(0)
        cap = re.search(r"<figcaption[^>]*>(.*?)</figcaption>", block, flags=re.I | re.S)
        if not cap:
            return ""
        caption = strip_tags(cap.group(1))
        return f"<p><em>[Figure omitted. {caption}]</em></p>" if caption else ""

    fragment = re.sub(r"<figure\b[^>]*>.*?</figure>", replace_figure, fragment, flags=re.I | re.S)
    fragment = re.sub(r"<img\b[^>]*>", "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"</?(div|span|section|article|header|footer|main)\b[^>]*>", "", fragment, flags=re.I | re.S)

    if extractor == "largest-td" or "paulgraham.com" in source:
        fragment = re.sub(r"</?(table|tbody|thead|tr|td|th|colgroup|col|font|center)\b[^>]*>", "", fragment, flags=re.I | re.S)

    fragment = re.sub(r"<a\b[^>]*></a>", "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"\n{3,}", "\n\n", fragment)
    return fragment.strip()


def convert_with_pandoc(clean_html: str, out_format: str) -> str:
    if not shutil_which("pandoc"):
        raise RuntimeError("pandoc is required for clean_article_html.py but was not found in PATH")

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as handle:
        handle.write(f'<!doctype html><html><head><meta charset="utf-8"></head><body>{clean_html}</body></html>')
        in_path = handle.name
    out_path = in_path + (".md" if out_format == "markdown" else ".txt")
    try:
        target = "gfm" if out_format == "markdown" else "plain"
        subprocess.run(["pandoc", "--wrap=none", "-f", "html", "-t", target, in_path, "-o", out_path], check=True)
        text = Path(out_path).read_text(encoding="utf-8")
    finally:
        for path in (in_path, out_path):
            try:
                os.unlink(path)
            except FileNotFoundError:
                pass
    return text


def clean_output(text: str, out_format: str) -> str:
    if out_format == "markdown":
        text = re.sub(r'\*\\\[(Figure omitted\.[^\n]*?)\\\]\*', r'*[\1]*', text)
        text = re.sub(r"\\\n", "\n", text)
        text = re.sub(r"(?m)^[ \t]*\\[ \t]*$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def shutil_which(cmd: str) -> Optional[str]:
    for path in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(path) / cmd
        if candidate.exists() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


def build_file_content(title: str, source_label: str, out_format: str, extractor: str, body: str) -> str:
    date_str = dt.date.today().isoformat()
    return (
        f"# {title}\n\n"
        f"Source: {source_label}\n\n"
        f"Downloaded: {date_str}\n\n"
        f"Format: cleaned {out_format} generated by clean_article_html.py using extractor `{extractor}`. Images and embeds were omitted for readability.\n\n"
        f"---\n\n"
        + body
    )


def note_from_input(source: str, title: str) -> str:
    short = title.strip()
    if len(short) > 80:
        short = short[:77] + "..."
    return short or source


def write_index(out_dir: Path) -> None:
    rows: List[Tuple[str, str]] = []
    for child in sorted(out_dir.iterdir()):
        if child.name.startswith("."):
            continue
        if child.name == "INDEX.md":
            continue
        if child.is_dir():
            rows.append((f"[{child.name}/]({child.name})", "Subdirectory"))
        else:
            note = "Archive source file" if child.suffix in {".md", ".txt", ".html"} else "File"
            rows.append((f"[{child.name}]({child.name})", note))

    lines = ["# Index", "", "| Item | Note |", "|------|------|"]
    lines.extend(f"| {item} | {note} |" for item, note in rows)
    lines += ["", "## Notes", "- Updated by clean_article_html.py."]
    (out_dir / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(out_dir: Path, records: List[dict]) -> None:
    lines = [
        "# Download Manifest",
        "",
        f"Downloaded: {dt.date.today().isoformat()}",
        "",
        "| File | Title | Source | Extractor |",
        "|------|-------|--------|-----------|",
    ]
    for record in records:
        lines.append(
            f"| {record['file_name']} | {record['title']} | {record['source']} | {record['extractor']} |"
        )
    lines += ["", "## Notes", "- Updated by clean_article_html.py."]
    (out_dir / "download-manifest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def target_name(index: int, total: int, title: str, out_format: str) -> str:
    stem = slugify(title)
    suffix = ".md" if out_format == "markdown" else ".txt"
    if total == 1:
        return f"{stem}{suffix}"
    return f"{index:02d}-{stem}{suffix}"


def source_label(source: str) -> str:
    return source if urllib.parse.urlparse(source).scheme else str(Path(source).resolve())


def process_one(source: str, out_dir: Path, index: int, total: int, out_format: str, mode: str) -> dict:
    if urllib.parse.urlparse(source).scheme in {"http", "https"}:
        page_html = fetch_url(source)
    else:
        page_html = read_local(Path(source))

    title = extract_title(page_html, fallback=Path(source).stem if not urllib.parse.urlparse(source).scheme else "Article")
    extractor, fragment = extract_structural_block(page_html, mode)
    simplified = simplify_html(fragment, source=source, extractor=extractor)
    converted = convert_with_pandoc(simplified, out_format)
    cleaned = clean_output(converted, out_format)

    file_name = target_name(index, total, title, out_format)
    content = build_file_content(title, source_label(source), out_format, extractor, cleaned)
    (out_dir / file_name).write_text(content, encoding="utf-8")

    return {
        "title": title,
        "source": source,
        "extractor": extractor,
        "file_name": file_name,
        "note": note_from_input(source, title),
    }


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", help="URL(s) or local HTML file(s)")
    parser.add_argument("--out-dir", required=True, help="Directory for cleaned output files")
    parser.add_argument("--format", choices=["markdown", "text"], default="markdown", help="Output format")
    parser.add_argument("--mode", choices=["auto", "embedded", "article", "main", "body"], default="auto", help="Extraction mode")
    parser.add_argument("--update-index", action="store_true", help="Write or refresh INDEX.md in the output directory")
    parser.add_argument("--update-manifest", action="store_true", help="Write or refresh download-manifest.md in the output directory")
    return parser.parse_args(argv)


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    records = []
    total = len(args.inputs)
    for index, source in enumerate(args.inputs, start=1):
        record = process_one(source, out_dir, index, total, args.format, args.mode)
        records.append(record)
        print(f"[ok] {source} -> {record['file_name']} ({record['extractor']})")

    if args.update_manifest:
        write_manifest(out_dir, records)
        print("[ok] updated download-manifest.md")
    if args.update_index:
        write_index(out_dir)
        print("[ok] updated INDEX.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
