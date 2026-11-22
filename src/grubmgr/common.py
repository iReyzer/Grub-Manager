import os
import sys


def require_root() -> None:
    if os.getuid() != 0:
        print("Se necesita ejecutar como root")
        sys.exit(1)