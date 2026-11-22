import sys

from grubmgr import grubcfg
from grubmgr.common import require_root


def run(args) -> int:
    unset = args.unset or []
    
    if not args.assignments and not unset:
        for key, value in grubcfg.read_vars().items():
            if key in grubcfg.ALLOWED:
                print(f"{key}={value}")
        return 0
    
    require_root()

    changes: dict[str, str | None] = {}
    for item in args.assignments:
        key, sep, value = item.partition("=")
        check = grubcfg.ALLOWED.get(key)
        if not sep or check is None or not check(value):
            print(f"Invalid Value: {item}", file=sys.stderr)
            return 2
        changes[key] = value
    for key in unset:
        if key not in grubcfg.ALLOWED:
            print(f"Key not allowed: {key}", file=sys.stderr)
            return 2
        changes[key] = None
    
    return grubcfg.save_changes(changes)