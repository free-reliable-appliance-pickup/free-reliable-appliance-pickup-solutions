#!/usr/bin/env python3
"""Conservative, repeatable SEO link repair. Only repairs unambiguous local HTML paths."""
import argparse
import pathlib
import re
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parents[2]
HOSTS = {"freereliableappliancepickup.com", "www.freereliableappliancepickup.com"}
SKIP = {".git", "node_modules", ".venv"}

def repair(page, dry_run=True):
    original = page.read_text(encoding="utf-8")
    changes = []
    def replace(match):
        quote, href = match.group(1), match.group(2)
        parsed = urllib.parse.urlsplit(href)
        if parsed.scheme not in ("", "https", "http") or (parsed.netloc and parsed.netloc not in HOSTS):
            return match.group(0)
        if not parsed.path or parsed.path.endswith("/") or pathlib.PurePosixPath(parsed.path).suffix:
            return match.group(0)
        # Only change an extensionless URL when its .html file exists and
        # the existing directory/index target does not.
        if parsed.path.startswith("/"):
            local = ROOT / parsed.path.lstrip("/")
        else:
            local = page.parent / parsed.path
        local = local.resolve()
        if not local.is_relative_to(ROOT.resolve()):
            return match.group(0)
        if local.exists() or (local / "index.html").exists():
            return match.group(0)
        if not local.with_suffix(".html").is_file():
            return match.group(0)
        newpath = parsed.path + ".html"
        updated = urllib.parse.urlunsplit(parsed._replace(path=newpath))
        changes.append((href, updated))
        return "href=" + quote + updated + quote
    updated = re.sub(r'href=(["\'])([^"\']+)\1', replace, original, flags=re.I)
    if changes and not dry_run:
        page.write_text(updated, encoding="utf-8")
    return changes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    total = 0
    for page in sorted(ROOT.rglob("*.html")):
        if any(p in SKIP for p in page.relative_to(ROOT).parts):
            continue
        changes = repair(page, not args.apply)
        for old, new in changes:
            print(f"{page.relative_to(ROOT)}: {old} -> {new}")
        total += len(changes)
    print(f"{total} unambiguous extensionless links {'repaired' if args.apply else 'eligible for repair'}")
if __name__ == "__main__":
    main()
