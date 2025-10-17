#!/usr/bin/env python3

import os, sys, yaml
import datetime

VERSION_FILE = "version.yml"
CS_OUT = "Version/YumVersion.cs"

def read_version():
    with open(VERSION_FILE) as f:
        return yaml.safe_load(f)["version"]

def write_version(v): # type: ignore
    with open(VERSION_FILE, "w") as f:
        yaml.dump({"version": v}, f, sort_keys=False)

def bump(part: str ="patch"):
    v = read_version()
    v[part] += 1
    if part == "major":
        v["minor"], v["patch"] = 0, 0
    elif part == "minor":
        v["patch"] = 0
    v["build"] = v.get("build", 0) + 1
    write_version(v)
    return v

def generate_cs(v): # type: ignore
    content = f"""
// Auto-generated file.

namespace YumStudio.Version;

public static class YumStudioVersion
{{
  public const int Major = {v['major']};
  public const int Minor = {v['minor']};
  public const int Patch = {v['patch']};
  public const int Build = {v['build']};
  public static string String => $"{v['major']}.{v['minor']}.{v['patch']}+{v['build']}";
  public static string Full => $"{v['major']}.{v['minor']}.{v['patch']} (Build {v['build']}, {datetime.datetime.now(datetime.UTC)} UTC)";
}}
"""
    os.makedirs(os.path.dirname(CS_OUT), exist_ok=True)
    with open(CS_OUT, "w") as f:
        f.write(content.strip() + "\n")
    print(f"Generated {CS_OUT}")

def main(args: list[str] = []):
    part = args[1] if len(args) > 1 else "build"
    v = bump(part)
    generate_cs(v)
    print("New version:", f"{v['major']}.{v['minor']}.{v['patch']}+{v['build']}")
    print("Running")
    return os.system(f'dotnet build')

if __name__ == "__main__":
    main(sys.argv)