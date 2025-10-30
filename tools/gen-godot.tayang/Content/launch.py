import subprocess

def main(_: list[str]) -> int:
  print('Generating Godot C++...')
  ret = subprocess.run(['scons', '-f', 'GodotC++/SConstruct', ]).returncode
  
  if ret != 0:
    print('Failled...')
    return ret
  
  return 0