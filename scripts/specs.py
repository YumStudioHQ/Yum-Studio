#!/usr/bin/env python3
import os
from collections import defaultdict

EXCLUDES = {'node_modules', 'venv', '.git', '__pycache__'}
KNOWN_EXTS = {
    'py': 'Python', 'js': 'JavaScript', 'ts': 'TypeScript',
    'html': 'HTML', 'css': 'CSS', 'cpp': 'C++', 'c': 'C',
    'h': 'C header', 'java': 'Java', 'go': 'Go', 'rs': 'Rust', 'sh': 'Shell',
    'cs': 'C#', 'gd': 'GDScript', 'hpp': 'C++ header'
}

counts = defaultdict(lambda: {'lines': 0, 'files': 0}) # type: ignore

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in EXCLUDES]
    for f in files:
        ext = f.split('.')[-1]
        if ext in KNOWN_EXTS:
            path = os.path.join(root, f)
            try:
                with open(path, 'r', errors='ignore') as fh:
                    lines = sum(1 for _ in fh)
                counts[ext]['lines'] += lines
                counts[ext]['files'] += 1
            except Exception:
                pass

for ext, data in sorted(counts.items(), key=lambda x: x[1]['lines'], reverse=True): # type: ignore
    name = KNOWN_EXTS.get(ext, ext) # type: ignore
    print(f"{data['lines']:>7} lines of {name:<12} ({data['files']} files)")

total_lines = sum(data['lines'] for data in counts.values())
print(f"\nTotal: {total_lines} lines in all files")