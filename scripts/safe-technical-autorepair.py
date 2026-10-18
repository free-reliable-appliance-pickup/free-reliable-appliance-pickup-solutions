#!/usr/bin/env python3
"""Conservative, repeatable technical auto-repair. Never changes visible text or SEO intent."""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEL = re.compile(r'(?P<prefix>href\s*=\s*["\'])tel:(?P<number>[^"\'?#;]+)(?P<suffix>["\'])', re.I)
EXCLUDED = {'.git', 'node_modules', 'vendor', 'archive', 'backups', 'dist'}

def fix(text):
    def replace(match):
        raw = match.group('number')
        digits = re.sub(r'[^0-9]', '', raw)
        if len(digits) == 10:
            normalized = '+1' + digits
        elif len(digits) == 11 and digits.startswith('1'):
            normalized = '+' + digits
        else:
            return match.group(0)
        if raw == normalized:
            return match.group(0)
        return match.group('prefix') + 'tel:' + normalized + match.group('suffix')
    return TEL.sub(replace, text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changed = []
    for path in ROOT.rglob('*.html'):
        if any(part in EXCLUDED or part.startswith('.') for part in path.relative_to(ROOT).parts[:-1]):
            continue
        try:
            original = path.read_text(encoding='utf-8')
        except (UnicodeError, OSError):
            continue
        updated = fix(original)
        if updated != original:
            changed.append(str(path.relative_to(ROOT)))
            if not args.check:
                path.write_text(updated, encoding='utf-8')
    print(f"Telephone URI normalization: {len(changed)} file(s)")
    for path in changed[:50]:
        print(' -', path)
    if args.check and changed:
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
