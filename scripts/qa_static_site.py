#!/usr/bin/env python3
"""Static QA checks for this GitHub Pages site."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = [ROOT / "index.html"]
CSS_FILES = sorted((ROOT / "stylesheets").glob("*.css"))
SKIP_SCHEMES = {"http", "https", "mailto", "tel", "data"}


class SiteParser(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.links = []
        self.ids = []
        self.images = []
        self.title_seen = False
        self.description_seen = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "title":
            self.title_seen = True
        if tag == "meta" and attrs.get("name") == "description" and attrs.get("content"):
            self.description_seen = True
        for attr in ("href", "src"):
            if attr in attrs:
                self.links.append((tag, attr, attrs[attr]))
        if tag == "img":
            self.images.append((attrs.get("src", ""), attrs.get("alt")))


def is_external(target):
    parsed = urlparse(target)
    return parsed.scheme in SKIP_SCHEMES or target.startswith("#")


def local_path(source_file, target):
    path = target.split("#", 1)[0].split("?", 1)[0]
    if not path or is_external(target):
        return None
    if path.startswith("/"):
        return ROOT / path.lstrip("/")
    return source_file.parent / path


def check_html(path):
    errors = []
    parser = SiteParser(path)
    parser.feed(path.read_text(encoding="utf-8"))

    if not parser.title_seen:
        errors.append(f"{path.relative_to(ROOT)}: missing <title>")
    if not parser.description_seen:
        errors.append(f"{path.relative_to(ROOT)}: missing meta description")

    seen = set()
    for anchor in parser.ids:
        if anchor in seen:
            errors.append(f"{path.relative_to(ROOT)}: duplicate id #{anchor}")
        seen.add(anchor)

    for src, alt in parser.images:
        if alt is None or not alt.strip():
            errors.append(f"{path.relative_to(ROOT)}: image missing alt text: {src}")

    for tag, attr, target in parser.links:
        resolved = local_path(path, target)
        if resolved and not resolved.exists():
            errors.append(
                f"{path.relative_to(ROOT)}: missing local {tag} {attr} target: {target}"
            )

    return errors


def check_css(path):
    errors = []
    text = path.read_text(encoding="utf-8")
    for match in re.finditer(r"url\(([^)]+)\)", text):
        target = match.group(1).strip().strip("\"'")
        resolved = local_path(path, target)
        if resolved and not resolved.exists():
            errors.append(f"{path.relative_to(ROOT)}: missing CSS url target: {target}")
    return errors


def main():
    errors = []
    for path in HTML_FILES:
        if not path.exists():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")
            continue
        errors.extend(check_html(path))

    for path in CSS_FILES:
        errors.extend(check_css(path))

    if errors:
        print("Static QA failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Static QA passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
