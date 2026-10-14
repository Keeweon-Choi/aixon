#!/usr/bin/env python3
"""Small, deliberately strict static output auditor."""
from __future__ import annotations
import argparse, re
from pathlib import Path

def target(root: Path, source: Path, value: str):
    value=value.split('#',1)[0].split('?',1)[0]
    if not value or value.startswith(('mailto:','tel:','javascript:','http:','https:','data:')): return None
    p=(root/value.lstrip('/')) if value.startswith('/') else source.parent/value
    if p.is_dir(): p=p/'index.html'
    elif not p.suffix: p=p/'index.html'
    return p
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('dist'); args=ap.parse_args(); root=Path(args.dist); errors=[]
    for fixed in ('sitemap-index.xml','robots.txt'):
        if not (root/fixed).exists(): errors.append(f'missing {fixed}')
    for page in root.rglob('*.html'):
        text=page.read_text(encoding='utf8',errors='replace')
        if not re.search(r'<html\b[^>]*\blang=["\']ko["\']',text,re.I): errors.append(f'{page}: lang=ko')
        if not re.search(r'<title>[^<]+</title>',text,re.I): errors.append(f'{page}: title')
        if not re.search(r'<meta\b[^>]*name=["\']description["\']',text,re.I): errors.append(f'{page}: description')
        if len(re.findall(r'<h1\b',text,re.I)) != 1: errors.append(f'{page}: exactly one h1')
        if 'katex-error' in text: errors.append(f'{page}: katex-error')
        for tag, attr, val in re.findall(r'<(a|img|script|link)\b[^>]*?\b(href|src)=["\']([^"\']+)',text,re.I):
            if tag.lower() == 'script' and val.startswith(('http://','https://')): errors.append(f'{page}: external asset {val}')
            p=target(root,page,val)
            if p is not None and not p.exists(): errors.append(f'{page}: missing {val}')
    print('\n'.join(errors) if errors else 'check-dist: OK')
    return bool(errors)
if __name__=='__main__': raise SystemExit(main())
