# YumStudio Developer Tool (`ysdev.py`)

`ysdev.py` is a command-line utility that automates setup, updates, builds, and inspections for the **YumStudio Engine**.
It manages the YumStudio repository, handles dependencies, and runs developer-related tasks such as builds, validation, and maintenance.

---

## Installation

Clone this repository or copy `ysdev.py` into your project directory.
Make sure you are using **Python 3.8+** and have **Git** installed.

Make the script executable (optional on Windows):

```bash
chmod +x ysdev.py
```

---

## Usage

Run the tool with one of the available commands:

```bash
./ysdev.py <command>
```

Example:

```bash
./ysdev.py install
./ysdev.py update
./ysdev.py build
./ysdev.py specs
```

---

## Available Commands

| Command   | Description                                                                             |
| --------- | --------------------------------------------------------------------------------------- |
| `install` | Clones the YumStudio repository if missing and copies files into the current directory. |
| `update`  | Pulls the latest YumStudio changes and refreshes local files.                           |
| `build`   | Runs the build system (`scripts/Build.py`).                                             |
| `specs`   | Prints detailed information about the current project.                                  |
| `test`    | Runs validation scripts located in `validations/v_*.py`.                                |
| `pull`    | Updates YumStudio directly from the official Git repository (may overwrite changes).    |
| `nuke`    | Completely deletes YumStudio and reinstalls it from scratch.                            |

---

## Example Workflows

### First-Time Installation

```bash
./ysdev.py install
```

This command:

1. Clones the official YumStudio repository.
2. Copies all necessary files into the current directory.
3. Sets up Git and branches.
4. Updates and configures the environment automatically.

---

### Updating the Engine

```bash
./ysdev.py update
```

Fetches the latest version of YumStudio and refreshes local files.

---

### Building the Engine

```bash
./ysdev.py build
```

Runs the build pipeline using `scripts/Build.py`.

---

### Viewing Project Specifications

```bash
./ysdev.py specs
```

Prints formatted information about the code base and engine configuration.

---

### Running Validations

```bash
./ysdev.py test
```

Runs all scripts in the `validations/` folder that match `v_*.py`.

---

### Forcing a Full Reinstall

```bash
./ysdev.py nuke
```

Completely removes all YumStudio files and reinstalls the latest version from GitHub.
Use this only when you want to start clean.

---

## Extension System (Tayang Apps)

The tool supports loading external command modules called **Tayang Applications** (`*.tayang` directories).
Each app must contain:

```
<app>.tayang/
 ├── Resources/
 │   └── desc.txt
 └── Content/
     └── launch.py
```

You can add additional directories for Tayang apps in a `.ys-tayang` file:

```text
# Example .ys-tayang file
scripts/
devs/
custom_apps/
```

Each valid app appears in the command list automatically.

---

## Exit Codes

* `0` — Success
* `1` — General error or failed operation
* `130` — Keyboard interrupt

---

## Requirements

* **Python 3.8+**
* **Git**
* Internet access (for cloning and updating YumStudio)

---

## License

> This tool is part of the YumStudio development ecosystem.
> All rights reserved © YumStudioHQ.
> [see](./../LICENSE.md)