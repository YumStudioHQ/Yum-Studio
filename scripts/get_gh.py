import requests
import sys
import os
import argparse

from colors import Ansi

owner = ""
repo = ""
chunk_size = 4096
output = "output"
tag = None

strict_cmp:           bool      = False
excluded_extensions:  list[str] = []
excluded_names:       list[str] = []
excluded_strings:     list[str] = []
needed_extensions:    list[str] = []
needed_names:         list[str] = []
needed_strings:       list[str] = []


def get_url() -> str:
  """Return API URL for latest or specific tagged release."""
  if tag:
    return f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}"
  return f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

def is_searched(asset_name: str) -> bool:
  part: str = asset_name if strict_cmp else asset_name.lower()
  
  for eleminator in excluded_extensions: 
    if part.endswith(eleminator): return False
  
  for eleminator in excluded_names: 
    if part == eleminator: return False
  
  for eleminator in excluded_strings: 
    if eleminator in part: return False
  
  for need in needed_extensions:
    if not part.endswith(need): return False
  
  for need in needed_names:
    if not part == need: return False
    
  for need in needed_strings:
    if not need in part: return False
  
  return True


def download_asset(asset: dict[str, str]):
  """Download a single asset with live progress updates."""
  url = asset["browser_download_url"]
  name = asset["name"]
  path = os.path.join(output, name)

  print(f"Downloading {Ansi.CYAN}{name}{Ansi.RESET} ...")

  with requests.get(url, stream=True) as r:
    r.raise_for_status()
    total = int(r.headers.get("Content-Length", 0))
    downloaded = 0
    last_percent = -1

    with open(path, "wb") as f:
      for chunk in r.iter_content(chunk_size=chunk_size):
        if not chunk:
          continue
        f.write(chunk)
        downloaded += len(chunk)
        if total > 0:
          percent = int(downloaded * 100 / total)
          if percent != last_percent:
            sys.stdout.write(f"\r{Ansi.YELLOW}→ {percent}%{Ansi.RESET}")
            sys.stdout.flush()
            last_percent = percent
              
  print(f"\rSaved to {Ansi.GREEN}{path}{Ansi.RESET} ({Ansi.CYAN}100%{Ansi.RESET})")


def parse_args():
  parser = argparse.ArgumentParser(
    description="Download selected assets from a GitHub release (latest or specific tag)."
  )

  parser.add_argument("-o", "--owner", required=True, help="GitHub repository owner.")
  parser.add_argument("-r", "--repo", required=True, help="GitHub repository name.")
  parser.add_argument("--tag", help="Specific release tag to download (e.g. yum-gdextension-1.0-b4.5).")
  parser.add_argument("--output", default="output", help="Output folder for downloaded assets.")
  parser.add_argument("--strict", action="store_true", help="Enable strict name comparison (case-sensitive).")
  parser.add_argument("--chunk-size", type=int, default=4096, help="Download chunk size (bytes).")

  parser.add_argument("--excluded-extensions", nargs="*", default=[], help="File extensions to exclude.")
  parser.add_argument("--excluded-names", nargs="*", default=[], help="Exact file names to exclude.")
  parser.add_argument("--excluded-strings", nargs="*", default=[], help="Strings that exclude files containing them.")
  parser.add_argument("--needed-extensions", nargs="*", default=[], help="Only include files with these extensions.")
  parser.add_argument("--needed-names", nargs="*", default=[], help="Only include exact file names.")
  parser.add_argument("--needed-strings", nargs="*", default=[], help="Only include files containing these strings.")

  return parser.parse_args()


def main(argv: list[str]):
  global owner, repo, output, chunk_size, tag
  global strict_cmp, excluded_extensions, excluded_names, excluded_strings
  global needed_extensions, needed_names, needed_strings

  args = parse_args()

  # Apply CLI args
  owner = args.owner
  repo = args.repo
  output = args.output
  chunk_size = args.chunk_size
  strict_cmp = args.strict
  tag = args.tag

  excluded_extensions = [e.lower() for e in args.excluded_extensions]
  excluded_names = [e.lower() for e in args.excluded_names]
  excluded_strings = [e.lower() for e in args.excluded_strings]
  needed_extensions = [e.lower() for e in args.needed_extensions]
  needed_names = [e.lower() for e in args.needed_names]
  needed_strings = [e.lower() for e in args.needed_strings]

  os.makedirs(output, exist_ok=True)
  print(f"{Ansi.BOLD}Fetching release info...{Ansi.RESET}")

  r = requests.get(get_url())
  if r.status_code == 404:
    print(f"{Ansi.RED}Release not found (check tag name or repo).{Ansi.RESET}")
    sys.exit(1)
  r.raise_for_status()
  release = r.json()

  print(f"Release: {Ansi.CYAN}{release['tag_name']} - {release['name']}{Ansi.RESET}")

  assets = release.get("assets", [])
  binaries = [a for a in assets if is_searched(a["name"])]

  if not binaries:
    print(f"{Ansi.RED}No candidate binaries found in this release.{Ansi.RESET}")
    return

  for asset in binaries:
    download_asset(asset)

  print(f"{Ansi.GREEN}All binaries downloaded successfully.{Ansi.RESET}")


if __name__ == "__main__":
  main(sys.argv[1:])
