import sys

from grubmgr import grubcfg, themelib
from grubmgr.common import require_root


def run(args) -> int:
    if args.theme is None:
        active = themelib.current_theme()
        for name in themelib.list_themes():
            print(f"{'*' if name == active else ' '} {name}")
        return 0
    
    require_root()
    name = args.theme
    if name not in themelib.list_themes():
        print(f"Theme not found: {name}", file=sys.stderr)
        return 1
    
    changes: dict[str, str | None] = { "GRUB_THEME": str(themelib.theme_file(name)) }

    if grubcfg.read_vars().get("GRUB_TERMINAL_OUTPUT") == "console":
        print("Disactivating GRUB_TERMINAL_OUTPUT=console (prevented the theme to shows).", flush=True)
        changes["GRUB_TERMINAL_OUTPUT"] = None
    
    print(f"Applying {name}...", flush=True)
    return grubcfg.save_changes(changes)