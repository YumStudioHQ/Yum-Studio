# Yang (You Are Not G++) Automation Script

This Python script is a lightweight build tool that automates compiling, downloading, and running commands defined in a configuration file.
It works like a simplified version of `make`, allowing you to define flexible build rules using plain text.

---

## Installation

No installation is needed. Just make the script executable:

```bash
chmod +x yang.py
```

Make sure you are using **Python 3.8+**.

---

## Usage

Run the script with a build configuration file:

```bash
./yang.py build.conf
```

You can also pass variables from the command line:

```bash
./yang.py build.conf mode:release platform:linux
```

---

## Configuration File Format (`build.conf`)

Each line defines an action or variable.
Empty lines and lines starting with `#` are ignored.

### Example

```ini
# Define variables
src: src/
out: build/

# Create output directory
mkdir: $out

# Download a dependency
download: https://example.com/lib.zip in $out/lib.zip

# Exclude certain files from compilation
exclude: $src/tests/

# Define a compile rule for .c files
for .c: gcc -c $file -o $out/$(basename $file .c).o

# Run an initial command
cmd: echo "Starting build on $platform"

# Conditional assignment
when: platform is linux do compiler: gcc else compiler: clang

# Run checks after build
check: pytest tests/
```

---

## Features

* **Variables** — Use `$var` to substitute values dynamically.
* **Includes** — Process other directories with `include:`.
* **Downloads** — Fetch external files with `download: <url> in <path>`.
* **Commands** — Run any shell command with `cmd:`.
* **Checks** — Run post-build or verification steps with `check:`.
* **Conditionals** — Use `when:` to change behavior based on variables.
* **Patterns** — Define compile rules for file extensions using `for .ext:`.

---

## Example Run

```bash
$ ./yang.py build.conf
* downloading https://example.com/lib.zip -> build/lib.zip...
* compiling file src/main.c...
* done 1 in /project
* [1/1] checking...
* [1/1] done!
* 2 checks done
```

---

## Exit Codes

* `0` — Success
* `1` — Error during download or command execution
* `-1` — Invalid configuration or syntax