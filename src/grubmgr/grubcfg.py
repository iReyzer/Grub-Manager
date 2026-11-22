import re
import shutil
import subprocess
from pathlib import Path

GRUB_FILE = Path("/etc/default/grub")

_GFX_ITEM = r"(auto|\d+x\d+(x\d+)?)"
_GFX_RE = re.compile(rf"^{_GFX_ITEM}(,{_GFX_ITEM})*$")

def _safe(v: str) -> bool:
    """Evita caracteres que el shell interpretaría al leer /etc/default/grub."""
    return not any(c in v for c in '"$`\\\n\r')


ALLOWED = {
    "GRUB_TIMEOUT": lambda v: v.isdigit() and int(v) <= 600,
    "GRUB_TIMEOUT_STYLE": lambda v: v in ("menu", "countdown", "hidden"),
    "GRUB_DEFAULT": lambda v: v == "saved" or v.isdigit(),
    "GRUB_SAVEDEFAULT": lambda v: v in ("true", "false"),
    "GRUB_GFXMODE": lambda v: bool(_GFX_RE.match(v)),
    "GRUB_GFXPAYLOAD_LINUX": lambda v: v in ("keep", "text"),
    "GRUB_CMDLINE_LINUX_DEFAULT": _safe,
    "GRUB_DISABLE_OS_PROBER": lambda v: v in ("true", "false"),
    "GRUB_DISABLE_RECOVERY": lambda v: v in ("true", "false"),
    "GRUB_DISABLE_SUBMENU": lambda v: v == "y",
}

def read_vars(path: Path = GRUB_FILE) -> dict[str, str]:
    """Variables activas (no comentadas). Legible sin root."""
    values: dict[str, str] = {}
    for line in path.read_text().splitlines():
        m = re.match(r"^([A-Z_]+)=(.*)$", line)
        if m:
            values[m.group(1)] = m.group(2).strip().strip("\"'")
    return values

def apply_changes(text: str, changes: dict[str, str | None]) -> str:
    """value=None comenta la variable; si no existe, la añade al final."""
    for key, value in changes.items():
        active = rf"^{key}=.*$"
        commented = rf"^#\s*{key}=.*s"
        if value is None:
            text = re.sub(active, lambda m: "#" + m.group(0), text, flags=re.MULTILINE)
            continue
        line = f'{key}="{value}"'
        if re.search(active, text, re.MULTILINE):
            text = re.sub(active, lambda m: line, text, flags=re.MULTILINE)  # noqa: B023
        elif re.search(commented, text, re.MULTILINE):
            text = re.sub(commented, lambda m: line, text, count=1, flags=re.MULTILINE)  # noqa: B023
        else:
            text = text.rstrip("\n") + f"\n{line}\n"
    return text

def save_changes(changes: dict[str, str | None]) -> int:
    shutil.copy2(GRUB_FILE, GRUB_FILE.with_suffix(".bak"))
    text = GRUB_FILE.read_text()
    GRUB_FILE.write_text(apply_changes(text, changes))
    return subprocess.run(["grub-mkconfig", "-o", "/boot/grub/grub.cfg"], check=True).returncode