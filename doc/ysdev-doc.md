# Yum-Studio — Developer README

This README explains `ysdev.py`, how to add dependencies, and the build system used by the repository.

## Quick overview — ysdev.py
`ysdev.py` is a small development tool that automates common tasks:

- Commands:
  - `install` — clone `Yum-Studio` (if missing), copy files into the current dir, initialize a git repo and run update.
  - `update` — runs the script manager `scripts/s_YumStudio.py` to pull and process submodules/repos.
  - `build` — runs `scripts/Build.py` to bump versions and run build tasks.
  - `specs` — prints project specs (uses `scripts/specsV2` if available).
  - `test` — runs validation scripts in `validations/v_*.py`.

Usage examples:
- `python3 ysdev.py install`
- `python3 ysdev.py update`
- `python3 ysdev.py build`
- `python3 ysdev.py test`

`ysdev.py` uses simple colored console output and provides helper functions to run subprocesses, create virtual environments, install dependencies, execute validation scripts, and clean temporary files.

## How dependencies are handled

There are three places you can add dependencies, depending on scope:

1. Per-repository (recommended)
   - Put a `requirements.txt` in the target repository root.
   - `ysdev.py` / `process_repo()` will detect it and run:
     - `<venv>/bin/pip install -r requirements.txt`
   - This is the normal way to specify Python dependencies for a project.

2. Fallback / global defaults
   - `ysdev.py` defines a `DEFAULT_DEPS` list near the top. If a repository has no `requirements.txt`, `ysdev.py` will install those default packages into the created virtualenv.
   - Edit `DEFAULT_DEPS` in `ysdev.py` to add global fallback packages.

3. Script-level / runtime installation
   - Some runner scripts try to auto-detect missing modules and install them on-the-fly while executing scripts. That approach is less reliable; prefer declaring dependencies explicitly in `requirements.txt`.

Notes about `scripts/s_YumStudio.py`:
- It reads `.ys-deps` to obtain a list of repositories to add as submodules. The expected line format is:
  - `repo_url@repo_name`
  - Example: `https://github.com/some/repo.git@some-repo-dir`
- `s_YumStudio.py` will:
  - `git submodule add -f <repo_url> <repo_name>`
  - create a `.venv`, install requirements or fallback deps, run `scripts/s_*.py` inside each repo, and clean up.

## Build system (scripts/Build.py)

Purpose:
- Manage version metadata, bumping, and generating a C# version file.
- Parse and run a simple list of build tasks.

Key files and behavior:
- `version.yml` — YAML file storing semantic version components:
  ```yaml
  version:
    major: 0
    minor: 1
    patch: 2
    build: 5
  ```
- `scripts/Build.py`:
  - `read_version()` reads `version.yml` and returns the `version` mapping.
  - `bump(part)` increments one of `major|minor|patch|build`. When bumping `major` or `minor`, lower-order parts are zeroed. `build` is incremented on every bump.
    - Call via command line: `python3 scripts/Build.py major` (or `minor`, `patch`, `build`)
    - `ysdev.py build` calls `scripts/Build.py` with default behavior (bump `build`).
  - `generate_cs(v)` writes `Version/YumVersion.cs` with constants and human-readable strings reflecting the version.
    - Output example: `Version/YumVersion.cs` gets constants `Major`, `Minor`, `Patch`, `Build` and `String`/`Full` properties.
  - `parse_build_file("build/tasks.txt")` reads `build/tasks.txt` (simple "task: command" lines) and executes each command with `os.system`.
    - Format example (`build/tasks.txt`):
      ```
      clean: rm -rf build/
      compile: dotnet build -c Release
      package: zip -r YumStudio.zip build/
      ```
  - After bumping and C# generation, `scripts/Build.py` runs each task defined in `build/tasks.txt` in order.

Validation scripts:
- `validations/v_*.py` are small checks or runtime validations. `ysdev.py test` runs them sequentially and reports pass/fail.
- Example: `validations/v_RunYumStudio.py` launches Godot using a path defined in `validations/metadata.txt`.

## Examples

- Bump build number and run tasks:
  - `python3 scripts/Build.py build`
  - or `python3 ysdev.py build`

- Add a dependency to a subproject:
  - Create `repo/requirements.txt`:
    ```
    requests==2.31.0
    numpy>=1.25
    ```

- Add a repo to be managed by `s_YumStudio`:
  - Edit `.ys-deps` with lines like:
    ```
    https://github.com/SomeOrg/SomeRepo.git@some-repo-dir
    ```
  - Then run: `python3 scripts/s_YumStudio.py` or `python3 ysdev.py update`

## Validations & metadata

- `validations/metadata.txt` stores small key:value entries used by validation scripts (e.g., path to Godot).
  - Format:
    ```
    ; comments start with ;
    godot: /Applications/Godot Mono.app/Contents/MacOS/Godot
    ```

## Troubleshooting / Notes

- Always prefer an explicit `requirements.txt` for reproducible environments.
- `scripts/Build.py` expects `version.yml` with `version` mapping. Missing fields may raise errors.
- `s_YumStudio.py` and `ysdev.py` create and remove `.venv` directories — be aware this deletes per-repo virtualenvs on cleanup.
- Validation scripts should return non-zero on failure so `ysdev.py test` can report failures correctly.

---

This README provides the main touchpoints for working with the dev tooling. For code-level details inspect:
- `ysdev.py` — CLI and orchestration
- `scripts/Build.py` — versioning and build tasks
- `scripts/s_YumStudio.py` — repo/submodule runner
- `validations/` — runnable validation scripts
