#!/usr/bin/env python3
"""Render the bibliography from the reviewed primary-source ledger."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sources = json.loads((ROOT / 'research/sources.json').read_text())


def tex(text):
    return text.replace('&', r'\&').replace('_', r'\_').replace('%', r'\%')


entries = []
for s in sources:
    entries.append('@misc{' + s['key'] + ',\n'
                   + '  title={{' + tex(s['title']) + '}},\n'
                   + '  author={' + tex(s['author']) + '},\n'
                   + '  year={' + s['year'] + '},\n'
                   + '  url={' + s['url'] + '},\n'
                   + '  note={Accessed ' + s.get('accessed', '2026-09-21') + '}\n}')
(ROOT / 'references.bib').write_text('\n\n'.join(entries) + '\n')
print(f'Rendered {len(entries)} bibliography entries.')
