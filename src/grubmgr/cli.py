import argparse
import sys

from grubmgr.commands import config, install, remove, themes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="grubmgr", description="Grub manager")
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    p = sub.add_parser("config", help="Ver o modificar la config de GRUB (/etc/default/grub)")
    p.add_argument("assignments", nargs="*", metavar="KEY=VALUE")
    p.add_argument("--unset", action="append", metavar="KEY")
    p.set_defaults(func=config.run)

    p = sub.add_parser("themes", aliases=["theme"], help="Listar themes o aplicar uno")
    p.add_argument("theme", nargs="?", help="Nombre del theme (si se omite, lista)")
    p.set_defaults(func=themes.run)

    p = sub.add_parser("install", help="Instalar un theme")
    p.add_argument("source", help="URL git o directorio con theme.txt")
    p.set_defaults(func=install.run)

    p = sub.add_parser("remove", help="Eliminar un theme")
    p.add_argument("theme")
    p.set_defaults(func=remove.run)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_help()
        return 1

    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())