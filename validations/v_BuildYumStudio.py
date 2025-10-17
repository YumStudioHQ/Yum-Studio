import sys
import os
_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _parent not in sys.path:
  sys.path.insert(0, _parent)

import scripts.Build as build

if __name__ == "__main__":
  sys.exit(build.main([]))