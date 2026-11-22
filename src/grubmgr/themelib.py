import re
from pathlib import Path

from grubmgr import grubcfg

THEMES_DIR = Path("/boot/grub/themes")
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
PREVIEW_STEMS = ("preview", "screenshot", "background")
PREVIEW_EXTS = (".png", ".jpg", ".jpeg", ".gif")

def list_themes() -> list[str]:
    """Themes instalados: carpetas con theme.txt y nombre válido."""
    if not THEMES_DIR.is_dir():
        return []
    return sorted(
        p.name
        for p in THEMES_DIR.iterdir()
        if p.is_dir()
        and not p.is_symlink()
        and NAME_RE.match(p.name)
        and (p / "theme.txt").is_file()
    )

def theme_file(name: str) -> Path:
    return THEMES_DIR / name / "theme.txt"

def current_theme() -> str | None:
    """Nombre del theme activo según GRUB_THEME, o None si no hay."""
    value = grubcfg.read_vars().get("GRUB_THEME")
    if not value:
        return None
    path = Path(value)
    return path.parent.name if path.parent.parent == THEMES_DIR else None

def find_preview(name: str) -> Path | None:
    base = THEMES_DIR / name
    for stem in PREVIEW_STEMS:
        for ext in PREVIEW_EXTS:
            candidate = base / f"{stem}{ext}"
            if candidate.is_file():
                return candidate
    return None
