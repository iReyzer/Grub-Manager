import sys

from grubmgr.gui.app import main


if "linux" not in sys.platform:
  sys.exit("This program is intended for Linux only")
__all__ = ["main"]
