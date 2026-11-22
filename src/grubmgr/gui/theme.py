import json
import os
from pathlib import Path

from PySide6.QtCore import QFileSystemWatcher, QObject, QTimer
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

STATE_HOME = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state"))
SCHEME_FILE = STATE_HOME / "caelestia" / "scheme.json"

# Material You oscuro de reserva, por si falta el archivo o alguna clave
FALLBACK = {
    "background": "141218", "onBackground": "e6e0e9",
    "surfaceContainerLowest": "0f0d13", "surfaceContainer": "211f26",
    "surfaceContainerHigh": "2b2930", "surfaceContainerHighest": "36343b",
    "onSurface": "e6e0e9", "onSurfaceVariant": "cac4d0",
    "primary": "d0bcff", "onPrimary": "381e72",
    "outline": "938f99", "outlineVariant": "49454f",
    "inverseSurface": "e6e0e9", "inverseOnSurface": "322f35",
    "shadow": "000000",
}


def read_colours() -> dict[str, str] | None:
    try:
        raw = json.loads(SCHEME_FILE.read_text())["colours"]
    except (OSError, ValueError, KeyError, TypeError):
        return None
    if not isinstance(raw, dict):
        return None
    return {k: v.lstrip("#") for k, v in raw.items() if isinstance(v, str)}


def _color(colours: dict[str, str], name: str) -> QColor:
    color = QColor(f"#{colours.get(name, FALLBACK[name])}")
    return color if color.isValid() else QColor(f"#{FALLBACK[name]}")


def build_palette(c: dict[str, str]) -> QPalette:
    R = QPalette.ColorRole
    roles = {
        R.Window: "background",
        R.WindowText: "onSurface",
        R.Base: "surfaceContainer",
        R.AlternateBase: "surfaceContainerHigh",
        R.Text: "onSurface",
        R.Button: "surfaceContainerHigh",
        R.ButtonText: "onSurface",
        R.Highlight: "primary",
        R.HighlightedText: "onPrimary",
        R.Link: "primary",
        R.ToolTipBase: "inverseSurface",
        R.ToolTipText: "inverseOnSurface",
        R.PlaceholderText: "onSurfaceVariant",
        R.Light: "surfaceContainerHighest",
        R.Midlight: "surfaceContainerHigh",
        R.Mid: "outlineVariant",
        R.Dark: "surfaceContainerLowest",
        R.Shadow: "shadow",
    }
    palette = QPalette()
    for role, name in roles.items():
        palette.setColor(role, _color(c, name))
    for role in (R.WindowText, R.Text, R.ButtonText):
        palette.setColor(QPalette.ColorGroup.Disabled, role, _color(c, "outline"))
    return palette


def build_stylesheet(c: dict[str, str]) -> str:
    h = lambda name: _color(c, name).name()
    return f"""
    QPushButton {{ background: {h('surfaceContainerHigh')}; color: {h('onSurface')};
        border: none; border-radius: 8px; padding: 8px 14px; }}
    QPushButton:hover {{ background: {h('surfaceContainerHighest')}; }}
    QPushButton:pressed {{ background: {h('primary')}; color: {h('onPrimary')}; }}
    QPushButton:disabled {{ background: {h('surfaceContainer')}; color: {h('outline')}; }}
    QLineEdit, QPlainTextEdit, QListWidget {{
        background: {h('surfaceContainer')}; color: {h('onSurface')};
        border: 1px solid {h('outlineVariant')}; border-radius: 8px; padding: 4px 6px; }}
    QLineEdit:focus {{ border-color: {h('primary')}; }}
    QListWidget::item {{ padding: 6px; border-radius: 6px; }}
    QListWidget::item:selected {{ background: {h('primary')}; color: {h('onPrimary')}; }}
    QGroupBox {{ border: 1px solid {h('outlineVariant')}; border-radius: 10px;
        margin-top: 14px; padding-top: 10px; }}
    QGroupBox::title {{ subcontrol-origin: margin; subcontrol-position: top center;
        padding: 0 8px; }}
    QTabWidget::pane {{ border: none; }}
    QTabBar::tab {{ padding: 8px 16px; margin: 2px; border-radius: 8px;
        color: {h('onSurfaceVariant')}; }}
    QTabBar::tab:selected {{ background: {h('surfaceContainerHigh')}; color: {h('onSurface')}; }}
    """


class CaelestiaTheme(QObject):
    """Aplica la paleta de Caelestia y la actualiza cuando cambia el esquema."""

    def __init__(self, app: QApplication) -> None:
        super().__init__(app)
        self.app = app
        self.last: dict[str, str] | None = None

        app.setStyle("Fusion")   # Fusion respeta la paleta; otros estilos pueden ignorarla

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.setInterval(150)          # agrupa ráfagas de cambios
        self.timer.timeout.connect(self.apply)

        self.watcher = QFileSystemWatcher(self)
        self.watcher.fileChanged.connect(self.schedule)
        self.watcher.directoryChanged.connect(self.schedule)

        self.apply()

    def schedule(self, _path: str = "") -> None:
        self.timer.start()

    def rewatch(self) -> None:
        # Un guardado atómico sustituye el archivo y el watcher lo pierde:
        # se vuelve a registrar el archivo y la carpeta tras cada cambio
        watched = set(self.watcher.files()) | set(self.watcher.directories())
        for path in (SCHEME_FILE.parent, SCHEME_FILE):
            if path.exists() and str(path) not in watched:
                self.watcher.addPath(str(path))

    def apply(self) -> None:
        self.rewatch()
        colours = read_colours()
        if colours is None or colours == self.last:
            return
        self.last = colours
        self.app.setPalette(build_palette(colours))
        self.app.setStyleSheet(build_stylesheet(colours))