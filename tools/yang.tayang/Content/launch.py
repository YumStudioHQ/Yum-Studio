#!/usr/bin/env python3

import random
import sys
import os
import urllib.request
from pathlib import Path

TT_EXCLUDE  = 'exclude:'
TT_INCLUDE  = 'include:'
TT_DOWNLOAD = 'download:'
TT_CHECK    = 'check:'
TT_CMD      = 'cmd:'

def download_file(url: str, path: str) -> int:
  """Download a file from url into path."""
  dest = Path(path)
  dest.parent.mkdir(parents=True, exist_ok=True)
  if dest.exists():
    print(f'* skipping download: {path} already exists')
    return 0
  print(f'* downloading {url} -> {path}...')
  try:
    urllib.request.urlretrieve(url, str(dest))
    print(f'* downloaded {url}')
    return 0
  except Exception as e:
    print(f'! download failed: {e}')
    return 1

def expand(on: str, config: dict[str, str]) -> str:
  s = on
  prev = None
  while prev != s:
    prev = s
    for key, val in config.items():
      s = s.replace(f'${key}', val)
    s = s.replace('$root', str(Path(__file__).parent))
    s = s.replace('$builtins.random', f'{''.join(random.choices('AZERTYUIOPQSDFGHJKLMWXCVBNazertyuiopqsdfghjklmwxcvbn', k=16))}')
  return s

def expand_list(on: list[str], config: dict[str, str]) -> list[str]:
  return [expand(x, config) for x in on]

def get_files(dir: str, excluded: list[str]) -> list[str]:
  files: list[str] = []
  for dirpath, _, filenames in os.walk(dir):
    for filename in filenames:
      full = str(Path(dirpath) / filename)
      for ex in excluded:
        if not full.startswith(ex):
          files.append(str(Path(dirpath) / filename))
  
  return files

def compile_dir(dir: str, config: dict[str, str], patterns: dict[str, str], exclude: list[str]) -> int:
  done_tasks = 0
  files = get_files(dir, exclude)
  for file in files:
    for ext, pattern in patterns.items():   
      if file.endswith(ext):
        cmd = (
          expand(pattern, config)
          .replace('$filename', f'{file}')
          .replace('$file', file)
        )
        print(f'compiling file {file}...')
        ret = os.system(cmd)
        if ret != 0:
          print(f'compilation for "{file}" failed with code {ret}')
          return ret
        done_tasks += 1

  print(f'* done {done_tasks} in {dir}')
  return 0

def compile(config: dict[str, str], patterns: dict[str, str], 
          commands: list[str], exclude: list[str], 
          check: list[str], include: list[str]) -> int:
  done_tasks = 0

  for cmd in commands:
    cmd = expand(cmd, config)
    ret = os.system(cmd)
    if ret != 0:
      return ret
    done_tasks += 1

  excluded_paths = [str(Path(e).resolve()) for e in expand_list(exclude, config)]
  for inc in include: 
    ret = compile_dir(str(Path(inc).absolute()), config, patterns, [])
    if ret != 0: return ret
    print(f'* done dependency {inc}')

  ret = compile_dir(str(Path(__file__).parent), config, patterns, excluded_paths)
  if ret != 0: return ret
  
  for i in range(0, len(check)):
    cmd = check[i]
    cmd = expand(cmd, config)
    print(f'* [{i}/{len(check)}] checking...')
    ret = os.system(cmd)
    if ret != 0:
      print(f'* [{i}/{len(check)}] fail!')
      return ret
    done_tasks += 1
    print(f'* [{i}/{len(check)}] done!')
  
  print(f'* {done_tasks} checks done')
  
  return 0


def parse(file: str, cfg: dict[str, str]) -> int:
  config: dict[str, str] = cfg
  patterns: dict[str, str] = {}
  commands: list[str] = []
  exclude: list[str] = []
  check: list[str] = []
  include: list[str] = []

  path = Path(file)
  if not path.exists():
    print(f'*** {file}: no such file!')
    return 1

  with open(path, "r") as f:
    for line in f:
      line = line.strip()
      if not line or line.startswith('#'):
        continue

      if line.startswith('for '):
        try:
          _, rest = line.split('for ', 1)
          ext, pat = rest.split(':', 1)
          patterns[ext.strip()] = pat.strip()
        except ValueError:
          print('err: ill-formed format. Use "for .ext : command"')
          return -1

      elif line.startswith(TT_CMD):
        commands.append(line[len(TT_CMD):].strip())

      elif line.startswith(TT_EXCLUDE):
        files = line[len(TT_EXCLUDE):].strip().split(',')
        exclude.extend(f.strip() for f in files if f.strip())

      elif line.startswith(TT_CMD):
        tcheck = line[len(TT_EXCLUDE):].strip()
        check.append(tcheck)

      elif line.startswith(TT_INCLUDE):
        inc = line[len(TT_INCLUDE)].strip()
        include.append(inc)
            
      elif line.startswith(TT_DOWNLOAD):
        rest = line[len(TT_DOWNLOAD):].strip()
        
        if not ' in ' in rest:
            print('err: ill-formed download statement')
            return -1
        atpos = rest.find(' in ')
        link = rest[0:atpos].strip()
        at = rest[atpos+len(' in '):].strip()
        ret = download_file(link, at)
        if ret != 0: return ret
                
      elif line.startswith('when:'):
        expr = line[len('when:'):].strip()
        
        # Basic syntax: when <key> is <value> do <action> [else <other_action>]
        if ' is ' not in expr or ' do ' not in expr:
            print('err: ill-formed when statement')
            print('use syntax: when <key> is <value> do <key>: <value> [else <key>: <value>]')
            return -1
        
        # Extract condition
        cond_part, rest = expr.split(' do ', 1)
        key_name, expected_val = cond_part.split(' is ', 1)
        key_name = key_name.strip()
        expected_val = expected_val.strip()

        # Split action and optional else
        if ' else ' in rest:
            then_action, else_action = rest.split(' else ', 1)
            else_action = else_action.strip()
        else:
            then_action, else_action = rest.strip(), None

        # Ensure condition variable exists
        if key_name not in config:
            print(f'err: making condition on undefined key "{key_name}"')
            return -1
        actual_val = expand(config[key_name], config)
        matched = (actual_val == expected_val)

        # Choose which side to run
        chosen_action = then_action.strip() if matched else (else_action or '').strip()
        if not chosen_action:
            print(f'* when: condition "{key_name} is {expected_val}" not met, skipping')
            continue

        print(f'* when: {key_name}="{actual_val}" → executing "{chosen_action}"')

        # Execute the chosen action like a regular line
        if ':' not in chosen_action:
            print(f'err: malformed action in when-statement ("{chosen_action}")')
            return -1
                
        act_key, act_val = chosen_action.split(':', 1)
        act_key, act_val = act_key.strip(), act_val.strip()

        if act_key in ('root', 'file'):
            print('err: redefinition of built-in variable')
            return -1
            
        config[act_key] = act_val

      elif line.startswith('mkdir:'):
        thatdir = expand(line[len('mkdir:'):].strip(), config)
        os.makedirs(thatdir, exist_ok=True)
                    
      elif ':' in line:
        key, val = line.split(':', 1)
        key = key.strip()
        if key in ('root', 'file'):
          print('err: redefinition of built-in variable')
          return -1
        config[key] = val.strip()
    
  return compile(config, patterns, commands, exclude, check, include)


def main(argv: list[str]) -> int:
  if len(argv) < 1:
    print('*** Expected a build file')
    return -1
    
  flags = argv[0:]
  defs: dict[str, str] = {}
  
  defs['windows'] = 'win32'
  defs['linux'] = 'linux'
  defs['macos'] = 'darwin'
  
  defs['platform'] = sys.platform
  defs['home'] = str(Path.home())
  
  for flag in flags:
    if ':' in flag:
      key, val = flag.split(':', 1)
      defs[key.strip()] = val.strip()
    else: defs[flag.strip()] = ''
  
  return parse(argv[0], defs)

if __name__ == '__main__': 
  try:
    sys.exit(main(sys.argv[1:]))
  except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)