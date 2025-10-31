from pathlib import Path

EXTENSION_FOLDER: Path = Path('GDExtensions/')
SUPPORTS = [
  'macos.release', 'macos.debug',
  'linux.release.x86_64', 
  'linux.debug.x86_64', 
  'linux.release.x86_32', 
  'linux.debug.x86_32', 
  'windows.release.x86_64', 
  'windows.debug.x86_64', 
  'windows.release.x86_32', 
  'windows.debug.x86_32', 
]

def write_extension(name: str, path: Path):
  gd_extension_name = f'{name}.gdextension'

  if not path.exists(): 
    print(f'No such path: {path}')
    return
  
  with open(EXTENSION_FOLDER / gd_extension_name, 'w') as file:
    file.write(f'''[configuration]'
'entry_symbol = "{name}_init"'
'compatibility_minimum = "4.5"'
'reloadable = true'
'[libraries]''')
    
    for sup in SUPPORTS: file.write(f'{sup} = "res://{path / f'{name}.{sup}'}"')
    file.close()
    
def main(argv: list[str]) -> int:
  if len(argv) != 3:
    print("Usage: launch.py <extension_name> <path_to_extension>")
    return 1

  name = argv[1]
  path = Path(argv[2])
  write_extension(name, path)
  return 0