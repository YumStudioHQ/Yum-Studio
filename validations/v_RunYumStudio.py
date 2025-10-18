import subprocess
import sys
from tables import Table

if __name__ == "__main__":
  print("[VALIDATION] Running YumStudio...")
  try:
    godot = Table("validations/metadata.txt").get_key("godot", "godot") # Gonna default to godot if aliased.
    print("[VALIDATION] Launching Godot:", godot)
    subprocess.run([godot], check=True)
    print("[VALIDATION] Godot finished successfully.")
  except:
    sys.exit(1)
