import shutil
import sys

from grubmgr import grubcfg, themelib
from grubmgr.common import require_root


def run(args) -> int:
    require_root()
    name = args.theme

    if name not in themelib.list_themes():
        print(f"Theme not found: {name}", file=sys.stderr)
        return 1
    
    if themelib.current_theme() == name:
        print("Theme is in use: going to grub's default", flush=True)
        code = grubcfg.save_changes({"GRUB_THEME": None})
        if code != 0:
            return code
    
    shutil.rmtree(themelib.THEMES_DIR / name)
    print(f"Removed: {name}", flush=True)
    return 0