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
  'Lua': ['lua'],
  'MarkDown': ['md', 'todo']
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
  try:
    specs = specsof(path)
    items = sorted(specs.items(), key=lambda kv: kv[1], reverse=True)

    total = sum(count for _, count in items)
    languages = len(items)

    # column widths
    lang_width = max(8, max(len(k) for k, _ in items))
    num_width = max(5, len(str(total)))

    # build header
    s = f"{prefix}| {'Language':<{lang_width}} | {'Lines':>{num_width}} | {'Percent':>8} |\n"
    s += f"{prefix}|{'-' * (lang_width + 2)}|{'-' * (num_width + 2)}|{'-' * 10}|\n"

    # table body
    for key, count in items:
        percent = (count / total) * 100
        s += (
            f"{prefix}| {key:<{lang_width}} "
            f"| {Ansi.BRIGHT_BLUE}{count:>{num_width}}{Ansi.RESET} "
            f"| {Ansi.BRIGHT_CYAN}{percent:>7.2f}{Ansi.RESET}% |\n"
        )

    # footer
    if languages > 1:
        s += f"{prefix}|{'-' * (lang_width + 2)}|{'-' * (num_width + 2)}|{'-' * 10}|\n"
        s += (
            f"{prefix}| {'Total':<{lang_width}} "
            f"| {Ansi.BRIGHT_BLUE}{total:>{num_width}}{Ansi.RESET} "
            f"| {Ansi.BRIGHT_CYAN}{100:>7.2f}{Ansi.RESET}% |\n"
        )

    return s
  except:
    return ''



if __name__ == '__main__':
  print(pretty_specs('.'))