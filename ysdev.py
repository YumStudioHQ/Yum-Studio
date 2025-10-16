#!/usr/bin/env python3
"""
YumStudio Dev Tool — handles building, updating, installing, and inspecting YumStudio Engine.

Usage:
    ./ysdev.py install   # clones Yum-Studio/ if missing and copies it to current dir
    ./ysdev.py update    # pulls latest from GitHub and re-copies files
    ./ysdev.py build     # runs scripts/Build.py
    ./ysdev.py specs     # shows specs info
"""

import sys
import subprocess
import shutil
from pathlib import Path

REPO_URL = "https://github.com/YumStudioHQ/Yum-Studio.git"
REPO_DIR = Path("Yum-Studio")
SCRIPTS_DIR = REPO_DIR / "scripts"

# ------------------------------------------------
# Colors fallback
# ------------------------------------------------
class Ansi:
    RESET = "\033[0m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"

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
      specs.pretty_specs("./", f'{ME}: > ')
    except ImportError:
        print(f"{Ansi.BRIGHT_RED}{ME}: scripts.specsV2 not found. Try 'install'.{Ansi.RESET}")


# ------------------------------------------------
# Dispatcher
# ------------------------------------------------
COMMANDS = { # type: ignore
    "install": cmd_install,
    "update": cmd_update,
    "build": cmd_build,
    "specs": cmd_specs,
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
    main()
