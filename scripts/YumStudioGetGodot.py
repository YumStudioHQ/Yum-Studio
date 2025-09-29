import requests
import os
import zipfile

OWNER = "godotengine"
REPO = "godot"

API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"

OUTPUT_DIR = "godot"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class Ansi:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"

# Platforms we care about
TARGETS = {
    "win32": "win32",
    "win64": "win64",
    "linux.x86_32": "linux32",
    "linux.x86_64": "linux64",
    "macos.universal": "macos_universal",
}

def is_wanted_binary(asset_name: str):
    """Check if an asset is a Godot .NET/Mono runtime ZIP we care about."""
    name = asset_name.lower()
    if not name.endswith(".zip"):
        return False
    if "mono" not in name and "net" not in name:
        return False  # skip pure builds
    return any(t in name for t in TARGETS.keys())

def extract_zip(path: str, extract_to: str):
    """Extract a ZIP file into a target directory and delete the ZIP."""
    print(f"{Ansi.GREEN}Extracting {Ansi.YELLOW}{os.path.basename(path)}{Ansi.RESET}...")
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"{Ansi.GREEN}Extracted to {Ansi.CYAN}{extract_to}{Ansi.RESET}")

    # Delete the zip after extraction
    os.remove(path)
    print(f"{Ansi.GREEN}Removed {Ansi.RED}{path}{Ansi.RESET}")

def download_asset(asset: dict[str, str]):
    """Download and extract a single asset to its platform subfolder."""
    url = asset["browser_download_url"]
    name = asset["name"].lower()

    # Pick subfolder based on target keyword
    platform = None
    for key, folder in TARGETS.items():
        if key in name:
            platform = folder
            break

    if platform is None:
        return  # Not in our targets

    platform_dir = os.path.join(OUTPUT_DIR, platform)
    os.makedirs(platform_dir, exist_ok=True)

    path = os.path.join(platform_dir, asset["name"])

    print(f"{Ansi.GREEN}Downloading {Ansi.CYAN}{asset['name']}{Ansi.RESET} → {platform_dir}")
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=4096):
            f.write(chunk)
    print(f"{Ansi.GREEN}Saved to {Ansi.CYAN}{path}{Ansi.RESET}")

    # Extract automatically and remove zip
    extract_zip(path, platform_dir)

def GetGodot():
    print("Fetching latest Godot release...")
    r = requests.get(API_URL)
    r.raise_for_status()
    release = r.json()

    print(f"Latest release: {Ansi.CYAN}{release['tag_name']} - {release['name']}{Ansi.RESET}")

    assets = release.get("assets", [])
    binaries = [a for a in assets if is_wanted_binary(a["name"])]

    if not binaries:
        print(f"{Ansi.RED}[ERR] No matching binaries found in this release.{Ansi.RESET}")
        return

    for asset in binaries:
        download_asset(asset)

    print(f"{Ansi.GREEN}[DONE] All binaries downloaded and extracted!{Ansi.RESET}")

if __name__ == "__main__":
    GetGodot()
