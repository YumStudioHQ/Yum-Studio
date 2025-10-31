#!/usr/bin/env python3
"""
Repo and Submodule Runner
=========================

This script automates the setup and execution of Python scripts inside a GitHub repository
and its submodules. It performs the following steps:

1. Deletes any existing copy of the repository.
2. Clones the repository recursively (with submodules).
3. For each repository (main + submodules):
   - Creates a virtual environment (`.venv`) if it does not exist.
   - Installs dependencies from `requirements.txt` if present,
     otherwise installs fallback dependencies.
   - Finds and executes Python scripts matching `scripts/s_*.py`.
   - If a script fails due to a missing module, automatically installs it and retries.
   - Cleans up `.venv` and junk files after execution.

Additionally:
- Before processing repos, executes all scripts under local `./scripts/s_*.py`.
"""

import subprocess
import sys
import glob
from pathlib import Path
import shutil
import configparser
import re
import os

try:
  import scripts.specsV2 as specs
  import scripts.get_gh as get_gh
  from scripts.colors import Ansi
except ImportError:
  import specsV2 as specs
  import get_gh as get_gh
  from colors import Ansi

# Fallback dependencies if no requirements.txt exists
DEFAULT_DEPS = ["requests"]
CREDITS_FILE = "CREDITS.md"

def run_command(cmd: str, cwd: Path | None = None) -> int:
  """Execute a shell command with verbose logging."""
  print(f"{Ansi.CYAN}[CMD]{Ansi.RESET} {cmd}")
  try:
    subprocess.check_call(cmd, shell=True, cwd=str(cwd) if cwd else None)
    return 0
  except subprocess.CalledProcessError as e:
    print(f"{Ansi.RED}[ERR]{Ansi.RESET} Command failed: {cmd}")
    return e.returncode

def get_infos_of_git(url: str) -> tuple[str, str, str]:
  clean = url.replace(":", "/").rstrip("/")
  parts = clean.split("/")

  repo_name = os.path.splitext(parts[-1])[0]  # 'repo'
  author = parts[-2]                          # 'author' or 'org'

  # Try to infer the domain (GitHub, GitLab, etc.)
  domain = "github.com"
  for known in ("github.com", "gitlab.com", "bitbucket.org"):
    if known in url:
      domain = known
      break

  author_profile = f"https://{domain}/{author}"

  return repo_name, author, author_profile

def run_python_script(python_exec: Path, script: str) -> None:
  """Run a Python script, auto-installing missing dependencies if needed."""
  print(f"{Ansi.GREEN}[RUN]{Ansi.RESET} Executing script: {script}")
  result = run_command(f"{python_exec} {script}")

  if result != 0:
    print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} Attempting to detect missing modules in {script}...")
    with open(script, "r", encoding="utf-8") as f:
      code = f.read()

      missing_modules = re.findall(r"ModuleNotFoundError: No module named '([^']+)'", code)
      if not missing_modules:
        print(f"{Ansi.RED}[ERR]{Ansi.RESET} Script failed, no missing modules detected.")
        sys.exit(result)

      for module in missing_modules:
        print(f"{Ansi.YELLOW}[FIX]{Ansi.RESET} Installing missing package: {module}")
        run_command(f"{python_exec} -m pip install {module}")

      print(f"{Ansi.YELLOW}[RETRY]{Ansi.RESET} Retrying script: {script}")
      result = run_command(f"{python_exec} {script}")
      if result != 0:
        print(f"{Ansi.RED}[ERR]{Ansi.RESET} Script still failed after retry: {script}")
        sys.exit(result)


def cleanup_repo(repo_dir: Path) -> None:
  """Remove virtual environment and temporary files."""
  venv_dir = repo_dir / ".venv"
  if venv_dir.exists():
    print(f"{Ansi.YELLOW}[CLEAN]{Ansi.RESET} Removing virtual environment in {repo_dir}")
    shutil.rmtree(venv_dir, ignore_errors=True)

  for pattern in ["**/__pycache__", "**/.pytest_cache", "**/*.pyc"]:
    for path in repo_dir.glob(pattern):
      try:
        if path.is_dir():
          shutil.rmtree(path, ignore_errors=True)
        else:
          path.unlink(missing_ok=True)
        print(f"{Ansi.GREEN}[CLEAN]{Ansi.RESET} Removed {path}")
      except Exception as e:
        print(f"{Ansi.RED}[ERR]{Ansi.RESET} Could not remove {path}: {e}")


def process_repo(repo_dir: Path) -> None:
  """Set up a repository: venv, dependencies, run matching scripts, and cleanup."""
  print(f"{Ansi.BOLD}{Ansi.CYAN}[PROC]{Ansi.RESET} Processing repository at {repo_dir}")

  # Virtual environment
  venv_dir = repo_dir / ".venv"
  if venv_dir.exists():
    print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} Virtual environment already exists in {repo_dir}")
  else:
    print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} Creating virtual environment in {repo_dir}...")
    run_command(f"python3 -m venv {venv_dir}")

  python_exec = venv_dir / "bin" / "python"
  pip_exec = venv_dir / "bin" / "pip"

  # Dependencies
  req_file = repo_dir / "requirements.txt"
  if req_file.exists():
    print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} Installing dependencies in {repo_dir}...")
    run_command(f"{pip_exec} install -r {req_file}")
  else:
    print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} No requirements.txt found in {repo_dir}")
    if DEFAULT_DEPS:
      print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} Installing fallback dependencies: {', '.join(DEFAULT_DEPS)}")
      run_command(f"{pip_exec} install {' '.join(DEFAULT_DEPS)}")

  # Script execution
  pattern = str(repo_dir / "scripts" / "s_*.py")
  scripts = glob.glob(pattern)

  if not scripts:
    print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} No matching scripts found in {repo_dir}")
  else:
    for script in scripts:
      run_python_script(python_exec, script)
      
  # Cleanup
  cleanup_repo(repo_dir)
  print(specs.pretty_specs(f'{repo_dir}', f'{Ansi.CYAN}[SpecsV2]: {Ansi.RESET}'))

def generate_inner_doc(link: str, dir: Path, name: str, author: str) -> None:
  print(f'{Ansi.YELLOW}[DOC]{Ansi.RESET}: Generating documentation for {str(dir.absolute())}: ', end="")
  repo_license = dir / "LICENSE.md"
  repo_readme = dir / "README.md"

  try:
    with open(CREDITS_FILE, "a") as credit_file:
      credit_file.write(
        f'- [{name}]({link}) from {author} installed at {dir}.\n' +
        (f'\t- [license]({repo_license})\n' if repo_license.exists() else '') +
        (f'\t- [readme]({repo_readme})\n' if repo_readme.exists() > 0 else '')
      )
      credit_file.close()
    print(f'{Ansi.GREEN}DONE{Ansi.RESET}')
  except:
    print(f'{Ansi.RED}FAIL{Ansi.RESET}')

def include_font_credits():
  print(f'{Ansi.YELLOW}[DOC]{Ansi.RESET}: Generating credits for fonts: ', end="")

  try:  
    with open('.ys-assets', 'r') as ys:
      with open(CREDITS_FILE, "a") as out:
        out.write('\n# Fonts\n')
        for line in ys.readlines():
          line = line.strip()
          if line.startswith('font:'):
            beg = line.find('font:') + len('font:')
            parts = line[beg:].strip().split('@')
            if len(parts) > 1:
              out.write(f'- font [{parts[0].strip()}]({parts[1].strip()})\n')
      out.close()
      ys.close()
    print(f'{Ansi.GREEN}DONE{Ansi.RESET}')
  except:
    print(f'{Ansi.RED}FAIL{Ansi.RESET}')

def get_submodules(repo_dir: Path) -> list[Path]:
  """Extract submodule paths from .gitmodules."""
  submodules: list[Path] = []
  gitmodules_file = repo_dir / ".gitmodules"
  if not gitmodules_file.exists():
    return submodules

  config = configparser.ConfigParser()
  config.read(gitmodules_file)

  for section in config.sections():
    if "path" in config[section]:
      sub_path = repo_dir / config[section]["path"]
      submodules.append(sub_path)

  return submodules

def gen_credits(dcredits: list[tuple[str, str, str, str, str]]):
  for repo_url, repo_dir, git_name, author, profile in dcredits:
    generate_inner_doc(repo_url, Path(repo_dir), git_name, f'[{author}]({profile})')

def gen_licenses():
  include_font_credits()
  
  with open(CREDITS_FILE, "a") as thankYouGodot:
    thankYouGodot.write(f'\nAnd of course, thanks a *lot* to the Godot project! <3\n')
    thankYouGodot.close()

def gen_docs(dcredits: list[tuple[str, str, str, str, str]]):
  print(f'{Ansi.YELLOW}[DOC]{Ansi.RESET}: Generating licenses')
  gen_licenses()
  gen_credits(dcredits)

def get_YumStudio(enable_const: bool = False, doc_only: bool = False):
  """Main entry point of the program."""
  deps: list[tuple[str, str, str]] = []
  credit_list: list[tuple[str, str, str, str, str]] = []

  with open(".ys-deps", "r") as ysdeps:
    linecount = 0
    for line in ysdeps.readlines():
      linecount += 1
      line = line.strip()
      if line.startswith('#'): continue
      elif line == '': continue
      elif line.startswith('const '):
        if enable_const: line = line[len('const ')]
        else: continue
      
      if not line.startswith('from') or not '@' in line or not ' in ' in line: 
        print(f'{Ansi.RED}err: parse error at line {linecount}:{line} in file .ys-deps{Ansi.RESET}')
        return
      
      nameend = line.find('@')
      tin = line.find(' in ')
      branch = line[len('from'):tin].strip()
      name = line[tin + len(' in '):nameend].strip()
      link = line[nameend+1:].strip()
      
      deps.append((name, branch, link))

  with open(CREDITS_FILE, "w", encoding="utf-8") as f:
    f.write("# Credits\n\n")
    f.write("This project uses the following dependencies (or assets):\n\n")

  with open(".gitmodules", "+a") as gsubmds:
    gsubmds.write('')
    gsubmds.close()

  for repo_url, branch, repo_name in deps:
    repo_dir = Path(repo_name)

    if not doc_only:
      if repo_dir.exists():
        print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} Removing existing repository at {repo_dir}")
        shutil.rmtree(repo_dir)

      print(f"{Ansi.CYAN}[CLONE]{Ansi.RESET} Cloning repository from {repo_url}")
      run_command(f"git submodule add -f -b {branch} {repo_url} {repo_name}")
      run_command("git submodule sync --recursive")
      run_command("git submodule update --init --recursive")
      process_repo(repo_dir)

      submodules = get_submodules(repo_dir)
      if not submodules:
        print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} No submodules found.")
      else:
        print(f"{Ansi.BOLD}{Ansi.CYAN}[PROC]{Ansi.RESET} Found {len(submodules)} submodule(s).")
        for sub in submodules:
          print(f"{Ansi.BOLD}{Ansi.CYAN}[SUBM]{Ansi.RESET} Processing submodule: {sub}")
          process_repo(sub)

      get_gh.main([
        '-o', 'YumStudioHQ', '-r', 
        'Yum-Studio', '--tag yum-gdextension-1.0-b4.5', '--needed-extensions .a',
        '--output', 'libraries/godot/'
      ])
      print(f"{Ansi.BOLD}{Ansi.GREEN}[DONE]{Ansi.CYAN} Dependency {repo_name} resolved{Ansi.RESET}")
    
    credit_list.append((repo_url, str(repo_dir), *get_infos_of_git(repo_url)))
  
  if not doc_only:  
    print(f"{Ansi.BOLD}{Ansi.GREEN}[DONE]{Ansi.RESET} All repositories and submodules processed successfully.")
    print(f'{Ansi.YELLOW}[INFO]{Ansi.RESET} Updating installed packages')
    run_command("git submodule foreach git pull")
    print(f"{Ansi.BOLD}{Ansi.GREEN}[DONE]{Ansi.RESET} All repositories and submodules updated.")

    print(f'{Ansi.YELLOW}[INFO]{Ansi.RESET} Generating docs and licenses')

  gen_docs(credit_list)
  
  if not doc_only:
    print(f'Sum up:')
    for repo_url, branch, repo_name in deps:
      print(f'- {repo_name} (branch {branch}) ({Ansi.CYAN}{repo_url}{Ansi.RESET})')
    
    print(f'Specs:\n{specs.pretty_specs(".", f'{Ansi.CYAN}[SpecsV2]: {Ansi.RESET}')}')

def main(argv: list[str]):
  get_YumStudio(
    '-const' in argv,
    '-doc-only' in argv
  )

if __name__ == "__main__":
  main(sys.argv)