#!/usr/bin/env python3
"""
YumStudio Dev Tool — handles building, updating, installing, and inspecting YumStudio Engine.

Usage:
    ./ysdev.py install   # clones Yum-Studio/ if missing and copies it to current dir
    ./ysdev.py update    # pulls latest from GitHub and re-copies files
    ./ysdev.py build     # runs scripts/Build.py
    ./ysdev.py specs     # shows specs info
"""

import glob
import re
import sys
import subprocess
import shutil
from pathlib import Path

REPO_URL = "https://github.com/YumStudioHQ/Yum-Studio.git"
REPO_DIR = Path("Yum-Studio")
SCRIPTS_DIR = REPO_DIR / "scripts"
DEFAULT_DEPS = ["requests"]

# ------------------------------------------------
# Colors fallback
# ------------------------------------------------
class Ansi:
  RESET = "\033[0m"
  BOLD = "\033[1m"
  UNDERLINE = "\033[4m"
  BLACK = "\033[30m"
  RED = "\033[31m"
  GREEN = "\033[32m"
  YELLOW = "\033[33m"
  BLUE = "\033[34m"
  MAGENTA = "\033[35m"
  CYAN = "\033[36m"
  WHITE = "\033[37m"
  BRIGHT_BLACK = "\033[90m"
  BRIGHT_RED = "\033[91m"
  BRIGHT_GREEN = "\033[92m"
  BRIGHT_YELLOW = "\033[93m"
  BRIGHT_BLUE = "\033[94m"
  BRIGHT_MAGENTA = "\033[95m"
  BRIGHT_CYAN = "\033[96m"
  BRIGHT_WHITE = "\033[97m"

ME = f"{Ansi.BRIGHT_MAGENTA}[YumStudio-Devs]{Ansi.RESET}"

# ------------------------------------------------
# Helpers
# ------------------------------------------------
def run(cmd: list[str], cwd: str|None=None):
  """Run a subprocess with live output."""
  try:
    subprocess.run(cmd, cwd=cwd, check=True)
    return True
  except subprocess.CalledProcessError:
    print(f"{Ansi.BRIGHT_RED}{ME}: Command failed — {' '.join(cmd)}{Ansi.RESET}")
    return False

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


def run_python_script(python_exec: Path, script: str) -> None:
  """Run a Python script, auto-installing missing dependencies if needed."""
  print(f"{Ansi.GREEN}[RUN]{Ansi.RESET} Executing script: {script}")
  result = run([f"{python_exec}", f"{script}"])

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
        run([f"{python_exec}", "-m", "pip", "install", "module"])

      print(f"{Ansi.YELLOW}[RETRY]{Ansi.RESET} Retrying script: {script}")
      result = run([f"{python_exec}", "{script}"])
      if result != 0:
        print(f"{Ansi.RED}[ERR]{Ansi.RESET} Script still failed after retry: {script}")
        sys.exit(result)

def process_repo(repo_dir: Path) -> None:
  """Set up a repository: venv, dependencies, run matching scripts, and cleanup."""
  print(f"{Ansi.BOLD}{Ansi.CYAN}[PROC]{Ansi.RESET} Processing repository at {repo_dir}")

  # Virtual environment
  venv_dir = repo_dir / ".venv"
  if venv_dir.exists():
    print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} Virtual environment already exists in {repo_dir}")
  else:
    print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} Creating virtual environment in {repo_dir}...")
    run([f"python3 -m venv {venv_dir}"])

  python_exec = venv_dir / "bin" / "python"
  pip_exec = venv_dir / "bin" / "pip"

  # Dependencies
  req_file = repo_dir / "requirements.txt"
  if req_file.exists():
    print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} Installing dependencies in {repo_dir}...")
    run([f"{pip_exec} install -r {req_file}"])
  else:
    print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} No requirements.txt found in {repo_dir}")
    if DEFAULT_DEPS:
      print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} Installing fallback dependencies: {', '.join(DEFAULT_DEPS)}")
      run([f"{pip_exec} install {' '.join(DEFAULT_DEPS)}"])

  # Script execution
  pattern = str(repo_dir / "validations" / "v_*.py")
  scripts = glob.glob(pattern)

  if not scripts:
    print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} No matching scripts found in {repo_dir}")
  else:
    for script in scripts:
      run_python_script(python_exec, script)

  # Cleanup
  cleanup_repo(repo_dir)

def ensure_repo():
  """Clone Yum-Studio if missing."""
  if REPO_DIR.exists():
    print(f"{Ansi.BRIGHT_YELLOW}{ME}: Repo already exists, skipping clone.{Ansi.RESET}")
    return True
  
  print(f"{ME}: Cloning YumStudio from GitHub...")
  return run(["git", "clone", REPO_URL])


def copy_repo_contents():
  """Copy all files from Yum-Studio/* into current directory."""
  if not REPO_DIR.exists():
    print(f"{Ansi.BRIGHT_RED}{ME}: Repo not found, cannot copy files.{Ansi.RESET}")
    return False

  print(f"{ME}: Copying YumStudio files to current directory...")

  for item in REPO_DIR.iterdir():
    dest = Path(".") / item.name

    # Skip .git and existing repo folder
    if item.name == ".git":
      continue

    # If destination exists, remove it first
    if dest.exists():
      if dest.is_dir():
        shutil.rmtree(dest)
      else:
        dest.unlink()

    # Copy folder or file
    if item.is_dir():
      shutil.copytree(item, dest)
    else:
      shutil.copy2(item, dest)

  print(f"{Ansi.BRIGHT_GREEN}{ME}: Files copied successfully!{Ansi.RESET}")
  return True


def pull_repo():
  """Update the repo if it exists."""
  if not REPO_DIR.exists():
    print(f"{Ansi.BRIGHT_YELLOW}{ME}: Repo not found. Run 'install' first.{Ansi.RESET}")
    return False


  return True


# ------------------------------------------------
# Commands
# ------------------------------------------------
def cmd_install(_args: list[str]):
  if ensure_repo():
    copy_repo_contents()
    print(f"{Ansi.BRIGHT_GREEN}{ME}: YumStudio installed successfully!{Ansi.RESET}")
    run(['git', 'init'])
    run(['git', 'branch', '-m', 'main'])
    print(f'{Ansi.BRIGHT_YELLOW}{ME}{Ansi.RESET}: Updating YumStudio...')
    cmd_update(_args)
  else:
    print(f"{Ansi.BRIGHT_RED}{ME}: Installation failed!{Ansi.RESET}")


def cmd_update(_args: list[str]):
  try:
    import scripts.s_YumStudio as YS
    YS.main()
  except ImportError:
    print(f"{Ansi.BRIGHT_RED}{ME}: scripts.s_YumStudio not found. Try 'install'.{Ansi.RESET}")

def cmd_build(_args: list[str]):
  try:
    import scripts.Build as build
    build.main()
  except ImportError:
    print(f"{Ansi.BRIGHT_RED}{ME}: scripts.Build not found. Try 'install'.{Ansi.RESET}")


def cmd_specs(_args: list[str]):
  try:
    import scripts.specsV2 as specs
    print(specs.pretty_specs("./", f'{ME}: > '))
  except ImportError:
    print(f"{Ansi.BRIGHT_RED}{ME}: scripts.specsV2 not found. Try 'install'.{Ansi.RESET}")

def cmd_validate(_args: list[str]):
  """Run all validation scripts (validations/v_*.py)."""
  validations_dir = Path("validations")

  if not validations_dir.exists():
    print(f"{Ansi.BRIGHT_RED}{ME}: No 'validations' directory found!{Ansi.RESET}")
    return

  scripts = sorted(validations_dir.glob("v_*.py"))
  if not scripts:
    print(f"{Ansi.BRIGHT_YELLOW}{ME}: No validation scripts found in {validations_dir}{Ansi.RESET}")
    return

  print(f"{Ansi.BRIGHT_CYAN}{ME}: Starting validations...{Ansi.RESET}")

  for script_path in scripts:
    # Extract readable name
    name = script_path.stem.replace("v_", "")
    print(f"{Ansi.BRIGHT_BLUE}[VAL]{Ansi.RESET} Running validation: {Ansi.BOLD}{name}{Ansi.RESET}")
    result = run(["python3", str(script_path)])

    if result:
      print(f"{Ansi.BRIGHT_GREEN}[OK]{Ansi.RESET} Validation passed: {name}")
    else:
      print(f"{Ansi.BRIGHT_RED}[FAIL]{Ansi.RESET} Validation failed: {name}")

  print(f"{Ansi.BRIGHT_MAGENTA}{ME}: All validations finished!{Ansi.RESET}")

def cmd_update_upstream(_args: list[str]):
  sys.exit(run(["git", "pull", f'{REPO_URL}', "main"]))

def cmd_force_update(_args: list[str]):
    """Completely removes Yum-Studio and reinstalls it fresh from GitHub."""
    confirm = input(f"{Ansi.BRIGHT_RED}{ME}: This will DELETE Yum-Studio and reinstall it. Continue? (y/N) {Ansi.RESET}")
    if confirm.lower().strip() != "y":
        print(f"{Ansi.YELLOW}{ME}: Aborted.{Ansi.RESET}")
        return

    print(f"{Ansi.BRIGHT_RED}{ME}: Nuking everything...{Ansi.RESET}")

    if REPO_DIR.exists():
        shutil.rmtree(REPO_DIR, ignore_errors=True)
        print(f"{Ansi.RED}[NUKE]{Ansi.RESET} Removed {REPO_DIR}")

    for path in Path(".").iterdir():
        if path.name in {".git", "ysdev.py"}:
            continue
        if path.is_dir() and path.name.startswith("Yum") or path.name == "scripts":
            shutil.rmtree(path, ignore_errors=True)
            print(f"{Ansi.RED}[NUKE]{Ansi.RESET} Removed dir {path}")
        elif path.name.startswith("Yum") and path.suffix in {".py", ".md"}:
            path.unlink(missing_ok=True)
            print(f"{Ansi.RED}[NUKE]{Ansi.RESET} Removed file {path}")

    print(f"{Ansi.BRIGHT_MAGENTA}{ME}: Reinstalling Yum-Studio from scratch...{Ansi.RESET}")
    if ensure_repo():
        copy_repo_contents()
        print(f"{Ansi.BRIGHT_GREEN}{ME}: Fresh install complete!{Ansi.RESET}")
        cmd_update(_args)
    else:
        print(f"{Ansi.BRIGHT_RED}{ME}: Force update failed!{Ansi.RESET}")


# ------------------------------------------------
# Dispatcher
# ------------------------------------------------
COMMANDS = { # type: ignore
  "install": cmd_install,
  "update": cmd_update,
  "build": cmd_build,
  "specs": cmd_specs,
  "test": cmd_validate,
  "pull": cmd_update_upstream,
  "force-update": cmd_force_update,
}

def main():
  if len(sys.argv) < 2:
    print(f"{Ansi.BRIGHT_YELLOW}{ME}: No command given! Try 'install' or 'build'.{Ansi.RESET}")
    return

  cmd = sys.argv[1].lower().strip()
  func = COMMANDS.get(cmd) # type: ignore
  if func:
    func(sys.argv[2:])
  else:
    print(f"{Ansi.BRIGHT_RED}{ME}: Unknown command '{cmd}'!{Ansi.RESET}")
    print("Available commands:", ", ".join(COMMANDS.keys())) # type: ignore


if __name__ == "__main__":
  try:
    main()
  except KeyboardInterrupt:
    print(f'{ME}: KeyboardInterrupt.')
    sys.exit(0)
