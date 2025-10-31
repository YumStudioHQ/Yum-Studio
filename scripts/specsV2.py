#!/usr/bin/env python3
import os
import time, threading
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
  'MarkDown': ['md', 'todo'],
  'Godot Objects': ['gd', 'tscn', '.godot', '.import'],
}

EXCLUDE = ['.venv', '.godot', '.vs', '.vscode', '.idea', '.mono']

def specsof(path: str, pr: bool = False) -> dict[str, tuple[int, int]]:
  lines_and_files_per_language: dict[str, tuple[int, int]] = {}
  stop_loading = False
  
  def loading_anim():
    dots = 0
    while not stop_loading:
      print(f"\rloading{'.' * dots:<3}", end='', flush=True)
      dots = (dots + 1) % 4
      time.sleep(0.3)
    print("\r" + " " * 20 + "\r", end='')  # clear line

    # start animation thread if pr=True
  if pr:
    t = threading.Thread(target=loading_anim)
    t.start()
    
  try:
    for root, dirs, files in os.walk(path):
      dirs[:] = [d for d in dirs if d not in EXCLUDE]
      for file in files:
        ext = file.rsplit('.', 1)[-1] if '.' in file else ''
        for lang, exts in EXTENSION.items():
          if ext in exts:
            file_path = os.path.join(root, file)
            try:
              with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                line_count = sum(1 for _ in f)
              files_count, lines_count = lines_and_files_per_language.get(lang, (0, 0))
              lines_and_files_per_language[lang] = (files_count + 1, lines_count + line_count)
              if pr: print(f"\rScanning: {file_path[:60]:<60}", end='', flush=True)
            except Exception: pass
            break
  finally:
    if pr:
      stop_loading = True
      t.join() #type:ignore
      print("\rDone scanning files!" + (' ' * 14))

    return lines_and_files_per_language

def pretty_specs(path: str, prefix: str = '> ') -> str:
  try:
    specs = specsof(path, True)
    if not specs:
      return '<cannot get specs>'

    # items: list of (lang, (files, lines)), sorted by lines descending
    items = sorted(specs.items(), key=lambda kv: kv[1][1], reverse=True)

    total_lines = sum(lines for _, (_, lines) in items)
    total_files = sum(files for _, (files, _) in items)
    languages = len(items)

    # column widths
    lang_width = max(8, max(len(k) for k, _ in items))
    files_width = max(5, len(str(total_files)))
    lines_width = max(5, len(str(total_lines)))

    # build header
    s = f"{prefix}| {'Language':<{lang_width}} | {'Files':>{files_width}} | {'Lines':>{lines_width}} | {'Percent':>8} |\n"
    s += f"{prefix}|{'-' * (lang_width + 2)}|{'-' * (files_width + 2)}|{'-' * (lines_width + 2)}|{'-' * 10}|\n"

    # table body
    for key, (files, lines) in items:
        percent = (lines / total_lines) * 100 if total_lines > 0 else 0.0
        s += (
            f"{prefix}| {key:<{lang_width}} "
            f"| {Ansi.BRIGHT_GREEN}{files:>{files_width}}{Ansi.RESET} "
            f"| {Ansi.BRIGHT_BLUE}{lines:>{lines_width}}{Ansi.RESET} "
            f"| {Ansi.BRIGHT_CYAN}{percent:>7.2f}{Ansi.RESET}% |\n"
        )

    # footer
    if languages > 1:
        s += f"{prefix}|{'-' * (lang_width + 2)}|{'-' * (files_width + 2)}|{'-' * (lines_width + 2)}|{'-' * 10}|\n"
        s += (
            f"{prefix}| {'Total':<{lang_width}} "
            f"| {Ansi.BRIGHT_GREEN}{total_files:>{files_width}}{Ansi.RESET} "
            f"| {Ansi.BRIGHT_BLUE}{total_lines:>{lines_width}}{Ansi.RESET} "
            f"| {Ansi.BRIGHT_CYAN}{100:>7.2f}{Ansi.RESET}% |\n"
        )

    return s
  except:
    return '<cannot get specs>'



if __name__ == '__main__':
  print(pretty_specs('.'))