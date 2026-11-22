import shutil
import sys
from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import QProcess, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
)

from grubmgr import grubcfg, themelib
from grubmgr.gui.theme import CaelestiaTheme
from grubmgr.gui.ui_main_window import Ui_MainWindow


def set_combo(combo: QComboBox, value: str) -> None:
    """Selecciona value; si no está en la lista, lo añade."""
    idx = combo.findText(value)
    if idx < 0:
        combo.addItem(value)
        idx = combo.findText(value)
    combo.setCurrentIndex(idx)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.busy = False
        self.active_theme: str | None = None
        self.preview_pixmap: QPixmap | None = None
        self.proc: QProcess | None = None
        self.on_success: Callable[[], None] | None = None

        self.ui = Ui_MainWindow()
        ui = self.ui
        ui.setupUi(self)

        ui.labelPreview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ui.labelPreview.setMinimumSize(1, 1)

        ui.btnReloadCfg.clicked.connect(self.load_config)
        ui.btnApplyCfg.clicked.connect(self.apply_config)
        ui.btnSearch.clicked.connect(self.browse_source)
        ui.btnInstall.clicked.connect(self.install_theme)
        ui.editSource.returnPressed.connect(self.install_theme)
        ui.listWidget.currentItemChanged.connect(self.on_theme_selected)
        ui.btnApply.clicked.connect(self.apply_theme)
        ui.btnRemove.clicked.connect(self.remove_theme)

        self.update_theme_buttons()
        self.load_config()
        self.load_themes()
    
    def log(self, text: str) -> None:
        self.ui.logText.appendPlainText(text.rstrip())
    
    # ---------- leer ----------
    def load_config(self) -> None:
        ui = self.ui
        try:
            v = grubcfg.read_vars()
        except OSError as e:
            self.log(f"Cannot read {grubcfg.GRUB_FILE}: {e}")
            return
        
        timeout = v.get("GRUB_TIMEOUT", "5")
        ui.spinTimeout.setValue(int(timeout) if timeout.isdigit() else 5)
        set_combo(ui.comboTimeoutStyle, v.get("GRUB_TIMEOUT_STYLE", "menu"))
        set_combo(ui.comboDefault, v.get("GRUB_DEFAULT", "0"))
        set_combo(ui.comboGfxMode, v.get("GRUB_GFXMODE", "auto"))
        ui.gfxPayloadCheckBox.setChecked(v.get("GRUB_GFXPAYLOAD_LINUX") == "keep")

        params = v.get("GRUB_CMDLINE_LINUX_DEFAULT", "").split()
        ui.quietCheckBox.setChecked("quiet" in params)
        ui.kernelParametersLineEdit.setText(" ".join(p for p in params if p != "quiet"))

        ui.osProberCheckBox.setChecked(v.get("GRUB_DISABLE_OS_PROBER") == "false")
        ui.submenuCheckBox.setChecked(v.get("GRUB_DISABLE_SUBMENU") != "y")
        ui.recoveryCheckBox.setChecked(v.get("GRUB_DISABLE_RECOVERY") == "true")

        self.log("Loaded config.")
    
    # ---------- escribir ----------
    def apply_config(self) -> None:
        ui = self.ui
        params = ui.kernelParametersLineEdit.text().split()
        if ui.quietCheckBox.isChecked():
            params.insert(0, "quiet")
        default = ui.comboDefault.currentText().strip()

        args = [
            f"GRUB_TIMEOUT={ui.spinTimeout.value()}",
            f"GRUB_TIMEOUT_STYLE={ui.comboTimeoutStyle.currentText()}",
            f"GRUB_DEFAULT={default}",
            f"GRUB_SAVEDEFAULT={'true' if default == 'saved' else 'false'}",
            f"GRUB_GFXMODE={ui.comboGfxMode.currentText().strip()}",
            f"GRUB_CMDLINE_LINUX_DEFAULT={' '.join(params)}",
            f"GRUB_DISABLE_OS_PROBER={'false' if ui.osProberCheckBox.isChecked() else 'true'}",
            f"GRUB_DISABLE_RECOVERY={'true' if ui.recoveryCheckBox.isChecked() else 'false'}",
        ]
        unset: list[str] = []

        if ui.gfxPayloadCheckBox.isChecked():
            args.append("GRUB_GFXPAYLOAD_LINUX=keep")
        else:
            unset.append("GRUB_GFXPAYLOAD_LINUX")
        
        if ui.submenuCheckBox.isChecked():
            unset.append("GRUB_DISABLE_SUBMENU")
        else:
            args.append("GRUB_DISABLE_SUBMENU=y")
        
        for key in unset:
            args += ["--unset", key]
        self.run_privileged(["config", *args], on_success=self.load_config)
    
    def run_privileged(self, cli_args, on_success=None) -> None:
        if self.busy:
            self.log("Ya hay una operación en curso.")
            return
        exe = "/usr/bin/grubmgr" if Path("/usr/bin/grubmgr").exists() else shutil.which("grubmgr")
        if exe is None:
            self.log("No encuentro el comando 'grubmgr' en el PATH.")
            return

        proc = QProcess(self)
        proc.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        proc.readyReadStandardOutput.connect(self.on_output)
        proc.finished.connect(self.on_finished)
        self.proc = proc
        self.on_success = on_success

        self.set_busy(True)
        self.log("Ejecutando...")
        proc.start("pkexec", [exe, *cli_args])

    def on_output(self) -> None:
        if self.proc is None:
            return
        raw = bytes(self.proc.readAllStandardOutput().data())
        text = raw.decode(errors="replace").strip("\n")
        if text:
            self.log(text)
    
    def on_finished(self, code: int, _status: QProcess.ExitStatus) -> None:
            self.set_busy(False)
            callback, self.on_success = self.on_success, None
            if code == 0:
                self.log("Done.")
                if callback:
                    callback()
            elif code in (126, 127):
                self.log("Authentication cancelled or denied.")
            else:
                self.log(f"Failed with code {code}.")
    
    def set_busy(self, busy: bool) -> None:
        self.busy = busy
        self.ui.btnApplyCfg.setEnabled(not busy)
        self.ui.btnInstall.setEnabled(not busy)
        self.update_theme_buttons()
    
    def update_theme_buttons(self) -> None:
        enabled = self.selected_themes() is not None and not self.busy
        self.ui.btnApply.setEnabled(enabled)
        self.ui.btnRemove.setEnabled(enabled)
    
    # ---------- install ----------
    def browse_source(self) -> None:
        path = QFileDialog.getExistingDirectory(
            self, "Select theme folder", str(Path.home())
        )
        if path:
            self.ui.editSource.setText(path)
    
    def install_theme(self) -> None:
        source = self.ui.editSource.text().strip()
        if not source:
            self.log("Write an URL or select a folder.")
            return
        if not source.startswith(("https://", "http://")):
            source = str(Path(source).expanduser())
        self.run_privileged(["install", "--", source], on_success=self.load_themes)
    
    # ---------- themes ----------
    def selected_themes(self) -> str | None:
        item = self.ui.listWidget.currentItem()
        return item.data(Qt.ItemDataRole.UserRole) if item else None
    
    def load_themes(self) -> None:
        try:
            names = themelib.list_themes()
            active = themelib.current_theme()
        except OSError as e:
            self.log(f"Cannot read themes: {e}")
            return
        
        previous = self.selected_themes()
        self.active_theme = active

        lst = self.ui.listWidget
        lst.clear()
        for name in names:
            item = QListWidgetItem(f"{name}  (active)" if name == active else name)
            item.setData(Qt.ItemDataRole.UserRole, name)
            lst.addItem(item)
        
        wanted = previous or active
        if wanted is not None and wanted in names:
            lst.setCurrentRow(names.index(wanted))
        elif names:
            lst.setCurrentRow(0)
        self.update_theme_buttons()
        self.log(f"Themes found: {len(names)}.")

    def on_theme_selected(self, current: QListWidgetItem | None, _previous) -> None:
        self.preview_pixmap = None
        name = current.data(Qt.ItemDataRole.UserRole) if current else None
        if name:
            try:
                path = themelib.find_preview(name)
            except OSError:
                path = None
            if path:
                self.preview_pixmap = QPixmap(str(path))
        self.update_preview()
        self.update_theme_buttons()
    
    def update_preview(self) -> None:
        label = self.ui.labelPreview
        if self.preview_pixmap is None or self.preview_pixmap.isNull():
            label.setText("No preview")
            return
        label.setPixmap(
            self.preview_pixmap.scaled(
                label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
    
    def apply_theme(self) -> None:
        name = self.selected_themes()
        if name is None:
            return
        self.run_privileged(["theme", name], on_success=self.load_themes)
    
    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.update_preview()
    
    def remove_theme(self) -> None:
        name = self.selected_themes()
        if name is None:
            return
        text = f"Remove theme '{name}'?"
        if name == self.active_theme:
            text += "\n\nIt is currently in use: GRUB will go back its defautl look."
        answer = QMessageBox.question(
            self, "Remove theme", text,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.run_privileged(["remove", name], on_success=self.load_themes)

def main() -> int:
    app = QApplication(sys.argv)
    CaelestiaTheme(app)
    window = MainWindow()
    window.show()
    return app.exec()
    