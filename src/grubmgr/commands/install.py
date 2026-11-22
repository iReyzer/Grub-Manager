import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from grubmgr.common import require_root
from grubmgr.themelib import NAME_RE, THEMES_DIR

MAX_DEPTH = 3

def is_url(source: str) -> bool:
    return source.startswith(("https://", "http://"))

def clone(url: str, dest: Path) -> None:
    env = {
        **os.environ,
        "GIT_ALLOW_PROTOCOL": "https:http",
        "GIT_TERMINAL_PROMPT": "0",
    }
    subprocess.run(
        ["git", "clone", "--depth", "1", "--", url, str(dest)],
        check=True,
        env=env,
    )

def find_themes(root: Path) -> list[Path]:
    """Carpetas que contienen un theme.txt (hasta MAX_DEPTH niveles)."""
    found = []
    for txt in root.rglob("theme.txt"):
        rel = txt.relative_to(root)
        if ".git" in rel.parts or txt.is_symlink() or len(rel.parts) - 1 > MAX_DEPTH:
            continue
        found.append(txt.parent)
    return sorted(found)

def _ignore(directory: str, names: list[str]) -> list[str]:
    # Fuera .git y cualquier enlace simbólico: como root, un symlink dentro de un
    # repo ajeno podría apuntar a /etc/shadow y acabaría copiado en /boot (legible).
    return [n for n in names if n == ".git" or os.path.islink(os.path.join(directory, n))]

def install_dir(src: Path, name: str) -> None:
    if not NAME_RE.match(name):
        raise ValueError(f"Theme name invalid: {name!r}")
    THEMES_DIR.mkdir(parents=True, exist_ok=True)
    dest = THEMES_DIR / name
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=_ignore)


def run(args) -> int:
    require_root()
    source = args.source.strip()

    try:
        with tempfile.TemporaryDirectory() as tmp:
            if is_url(source):
                root = Path(tmp) / "repo"
                print(f"Clonning in {source}", flush=True)
                clone(source, root)
                fallback = source.rstrip("/").removesuffix(".git").rsplit("/", 1)[-1]
            else:
                root = Path(source).resolve()
                if root.is_file() and root.name == "theme.txt":
                    root = root.parent
                if not root.is_dir():
                    print(f"Folder does not exists: {root}", file=sys.stderr)
                    return 2
                fallback = root.name
            
            themes = find_themes(root)
            if not themes:
                print("Could not find any theme.txt.", file=sys.stderr)
                return 1
            
            for d in themes:
                name = fallback if d == root else d.name
                install_dir(d, name)
                print(f"Instalado: {name}", flush=True)
    except (subprocess.CalledProcessError, ValueError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    print("For using it apply it from Themes tab", flush=True)
    return 0