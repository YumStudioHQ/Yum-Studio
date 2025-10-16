#!/usr/bin/env python3
import os

try:
  from scripts.colors import Ansi
except ImportError:
  from colors import Ansi

EXTENSION = {
  'C++': ['cpp', 'hpp', 'c++', 'h++'],
  'C': ['c', 'h'],
  'C#': ['cs'],
  'Python': ['py'],
  'Yaml': ['yml', 'yaml'],
  'CSS': ['css'],
  'HTML': ['html'],
  'JavaScript': ['js'],
  'YumStudio Object': ['yso', 'ysobject'],
  'Lua': ['lua']
}

EXCLUDE = ['.venv', '.godot', '.vs', '.vscode', '.idea']


def specsof(path: str) -> dict[str, int]:
  lines_per_language: dict[str, int] = {}
  
  for root, dirs, files in os.walk(path):
    # Exclude directories in-place
    dirs[:] = [d for d in dirs if d not in EXCLUDE]
    for file in files:
      ext = file.split('.')[-1]
      for lang, exts in EXTENSION.items():
        if ext in exts:
          file_path = os.path.join(root, file)
          try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
              line_count = sum(1 for _ in f)
            lines_per_language[lang] = lines_per_language.get(lang, 0) + line_count
          except Exception:
            pass
          break
  
  return lines_per_language

def pretty_specs(path: str, prefix: str = '> ') -> str:
  s = ''
  specs = specsof(path)
  largest = 4

  for key in specs.keys():
    if len(key) > largest: largest = len(key) + 2
  
  total = 0
  languages = 0
  
  for key in specs.keys():
    languages += 1
    count = specs[key]
    total += count
    s += f'{prefix}{key}{" " * (largest - len(key))}{Ansi.BRIGHT_BLUE}{count}{Ansi.RESET}\n'
  
  if languages > 1:
    s += f'{prefix}{Ansi.BRIGHT_BLUE}{languages}{Ansi.RESET} '
    s += f'languages\n{prefix}Total:{" " * (largest - 6)}{Ansi.BRIGHT_BLUE}{total}{Ansi.RESET}\n'
    
  return s

if __name__ == '__main__':
  print(pretty_specs('.'))