import sys

from grubmgr.cli import main

__all__ = ["main"]
if "linux" not in sys.platform:
  sys.exit("This program is intended for Linux only")
