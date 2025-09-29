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

The script outputs verbose, color-coded logs for professional debugging.
"""

import subprocess
import sys
import glob
from pathlib import Path
import shutil
import configparser
import re


class Ansi:
    """ANSI escape codes for colored terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"


# Fallback dependencies if no requirements.txt exists
DEFAULT_DEPS = ["requests"]


def run_command(cmd: str, cwd: Path | None = None) -> int:
    """Execute a shell command with verbose logging.

    Args:
        cmd: The shell command to execute.
        cwd: Optional working directory for the command.

    Returns:
        Exit code of the command.
    """
    print(f"{Ansi.CYAN}[CMD]{Ansi.RESET} {cmd}")
    try:
        subprocess.check_call(cmd, shell=True, cwd=str(cwd) if cwd else None)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"{Ansi.RED}[ERR]{Ansi.RESET} Command failed: {cmd}")
        return e.returncode


def run_python_script(python_exec: Path, script: str) -> None:
    """Run a Python script, auto-installing missing dependencies if needed.

    Args:
        python_exec: Path to the Python interpreter inside venv.
        script: Path to the Python script.
    """
    print(f"{Ansi.GREEN}[RUN]{Ansi.RESET} Executing script: {script}")
    result = run_command(f"{python_exec} {script}")

    if result != 0:
        # Check if error was due to ModuleNotFoundError
        print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} Attempting to detect missing modules in {script}...")
        with open(script, "r", encoding="utf-8") as f:
            code = f.read()

        missing_modules = re.findall(r"ModuleNotFoundError: No module named '([^']+)'", code)
        if not missing_modules:
            # Couldn’t auto-detect from source, just bail
            print(f"{Ansi.RED}[ERR]{Ansi.RESET} Script failed, no missing modules detected.")
            sys.exit(result)

        for module in missing_modules:
            print(f"{Ansi.YELLOW}[FIX]{Ansi.RESET} Installing missing package: {module}")
            run_command(f"{python_exec} -m pip install {module}")

        # Retry once
        print(f"{Ansi.YELLOW}[RETRY]{Ansi.RESET} Retrying script: {script}")
        result = run_command(f"{python_exec} {script}")
        if result != 0:
            print(f"{Ansi.RED}[ERR]{Ansi.RESET} Script still failed after retry: {script}")
            sys.exit(result)


def process_repo(repo_dir: Path) -> None:
    """Set up a repository: venv, dependencies, and run matching scripts.

    Args:
        repo_dir: Path to the repository directory.
    """
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
        return

    for script in scripts:
        run_python_script(python_exec, script)


def get_submodules(repo_dir: Path) -> list[Path]:
    """Extract submodule paths from .gitmodules.

    Args:
        repo_dir: Path to the main repository directory.

    Returns:
        A list of Path objects pointing to submodule directories.
    """
    submodules = []
    gitmodules_file = repo_dir / ".gitmodules"
    if not gitmodules_file.exists():
        return submodules # type: ignore

    config = configparser.ConfigParser()
    config.read(gitmodules_file)

    for section in config.sections():
        if "path" in config[section]:
            sub_path = repo_dir / config[section]["path"]
            submodules.append(sub_path) # type: ignore

    return submodules # type: ignore


def main() -> None:
    """Main entry point of the program."""
    repo_url = "https://github.com/YumStudioHQ/Yum4Godot.git"
    repo_name = "YumStudio"
    repo_dir = Path(repo_name)

    # Step 1: Clean existing repo
    if repo_dir.exists():
        print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} Removing existing repository at {repo_dir}")
        shutil.rmtree(repo_dir)

    # Step 2: Clone fresh repo with submodules
    print(f"{Ansi.CYAN}[CLONE]{Ansi.RESET} Cloning repository from {repo_url}")
    run_command(f"git clone --recurse-submodules {repo_url} {repo_name}")

    # Step 3: Process main repo
    process_repo(repo_dir)

    # Step 4: Process submodules
    submodules = get_submodules(repo_dir)
    if not submodules:
        print(f"{Ansi.YELLOW}[INFO]{Ansi.RESET} No submodules found.")
    else:
        print(f"{Ansi.BOLD}{Ansi.CYAN}[PROC]{Ansi.RESET} Found {len(submodules)} submodule(s).")
        for sub in submodules:
            print(f"{Ansi.BOLD}{Ansi.CYAN}[SUBM]{Ansi.RESET} Processing submodule: {sub}")
            process_repo(sub)

    print(f"{Ansi.BOLD}{Ansi.GREEN}[DONE]{Ansi.RESET} All repositories and submodules processed successfully.")


if __name__ == "__main__":
    main()
