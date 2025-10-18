class Table:
  def __init__(self, path: str) -> None:
    self.keys: dict[str, str] = {}
    self.path: str = path
    
    with open(path, "r+") as file:
      for line in file.readlines():
        if line.strip().startswith(';'): continue
        endp = line.find(':')
        
        if endp != -1:
          key: str = line[0:endp].strip()
          val: str = line[endp+1:].strip()
          self.keys[key] = val

      file.close()

  def get_key(self, key: str, default: str = "") -> str:
    if key in self.keys.keys(): return self.keys[key]
    return default
