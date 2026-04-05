import json
import os
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QCheckBox, QFileDialog, QTableWidgetItem, QWidget
from qfluentwidgets import FluentIcon, TransparentToolButton, setStyleSheet

from ui.lib_replace_content_ui import Ui_LibReplaceContent
from utils.module_resolver import ModuleResolver
from utils.ssh_worker import SSHTask


_STATUS_META: dict[str, tuple[str, str, str]] = {
    # status: (text, background_color, text_color)
    "ready": ("就绪", "#e8f5e9", "#388e3c"),
    "resolving": ("识别中", "#e3f2fd", "#1976d2"),
    "processing": ("处理中", "#e3f2fd", "#1976d2"),
    "done": ("完成", "#e8f5e9", "#388e3c"),
    "error": ("错误", "#ffebee", "#d32f2f"),
    "ignored": ("忽略", "#f5f5f5", "#757575"),
}

_SOURCE_EXTS = {".js", ".ts", ".py", ".c", ".cpp", ".h", ".java", ".go", ".rs"}


def _fileIcon(filename: str):
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return FluentIcon.CODE if ext in _SOURCE_EXTS else FluentIcon.DOCUMENT


class LibReplaceContent(QWidget):
    """Main content panel: shows the file list for the currently selected project."""

    def __init__(self, parent: QWidget, name: str):
        super().__init__(parent)
        self.name = name
        self._setupUi()
        self._installRequireSettings()
        self._installStyleSheet()
        self._projectPath: Path | None = None
        self._projectConfig: dict = {}
        self._resolvers: list[ModuleResolver] = []  # keep alive
        self._compileQueue: list[str] = []
        self._compileTotal = 0
        self._compileDone = 0
        self._sshTask: SSHTask | None = None
        self._syncingSelectAll = False

    def _setupUi(self) -> None:
        self.ui = Ui_LibReplaceContent()
        self.ui.setupUi(self)

    def _installRequireSettings(self) -> None:
        self.ui.breadcrumbBar.setSpacing(6)
        self.ui.breadcrumbBar.addItem("root", "我的项目")
        self.title = Path(self.name).name
        self.ui.breadcrumbBar.currentIndexChanged.connect(self.onBreadIndexChanged)
        self.ui.fileInput.returnPressed.connect(self._onAddFileClicked)
        self.ui.browseButton.clicked.connect(self._onBrowseClicked)
        self.ui.browseButton.setFont("")
        self.ui.addButton.clicked.connect(self._onAddFileClicked)
        self.ui.exportButton.clicked.connect(self._onExportClicked)
        self.ui.selectAllBox.setTristate(False)
        self.ui.selectAllBox.stateChanged.connect(self._onSelectAllChanged)
        self.ui.executeButton.clicked.connect(self._onExecuteClicked)
        self._setEnvDotState("idle")
        self.ui._repositionAllHeaderWidgets()
        self.ui.fileTable.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.ui.fileTable.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

    def onBreadIndexChanged(self, index: int) -> None:
        if index == 0:
            self.ui.breadcrumbBar.addItem("project", self.title)

    def _setEnvDotState(self, state: str) -> None:
        self.ui.envDot.setProperty("envState", state)
        self.ui.envDot.style().unpolish(self.ui.envDot)
        self.ui.envDot.style().polish(self.ui.envDot)
        self.ui.envDot.update()

    def _installStyleSheet(self, path: str = ":/style/lib_replace_content.qss") -> None:
        """style sheet installer"""
        setStyleSheet(self, path)

    def getName(self) -> str:
        return self.name

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def loadProject(self, path: str, config: dict) -> None:
        """Switch to the given project and render its file list."""
        self._projectPath = Path(path)
        self._projectConfig = config
        self._compileQueue.clear()
        self._clearItems()
        self._showEmptyState(False)

        name = self._projectPath.name
        if "root" not in self.ui.breadcrumbBar.itemMap:
            self.ui.breadcrumbBar.addItem("root", "我的项目")
        else:
            self.ui.breadcrumbBar.setCurrentItem("root")
        self.ui.breadcrumbBar.addItem("project", name)
        self.ui.exportButton.setEnabled(True)

        # Env status
        if config.get("type") == "ssh":
            host = config.get("host", "")
            self._setEnvDotState("ssh")
            self.ui.envLabel.setText(f"SSH: {host}")
        else:
            self._setEnvDotState("local")
            self.ui.envLabel.setText("本地环境")

        # Load existing files
        for entry in config.get("file", []):
            self._addRow(
                filename=entry.get("filename", ""),
                filepath=entry.get("filepath", ""),
                module=entry.get("module", ""),
                status=entry.get("status", "ready"),
                checked=entry.get("checked", True),
            )

        self._updateSelectionCount()

    # ------------------------------------------------------------------ #
    #  Slot handlers                                                       #
    # ------------------------------------------------------------------ #

    def _onBrowseClicked(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*)")
        if path:
            self.ui.fileInput.setText(path)

    def _onAddFileClicked(self) -> None:
        if self._projectPath is None:
            return

        raw = self.ui.fileInput.text().strip()
        if not raw:
            return

        filepath = raw
        filename = Path(filepath).name or filepath
        self.ui.fileInput.clear()

        # Check for duplicates
        if self._findRowByPath(filepath) >= 0:
            return

        self._addRow(filename=filename, filepath=filepath, status="resolving")
        self._saveProjectConfig()
        self._updateSelectionCount()

        # Async module resolution
        resolver = ModuleResolver(filepath)
        resolver.finished.connect(
            lambda module, fp=filepath: self._onResolveFinished(fp, str(module))
        )
        resolver.error.connect(lambda _, fp=filepath: self._onResolveError(fp))
        self._resolvers.append(resolver)
        resolver.resolve()

    def _onResolveFinished(self, filepath: str, module: str) -> None:
        row = self._findRowByPath(filepath)
        if row < 0:
            return
        self._setRowModule(row, module)
        self._setRowStatus(row, "ready")
        self._saveProjectConfig()

    def _onResolveError(self, filepath: str) -> None:
        row = self._findRowByPath(filepath)
        if row < 0:
            return
        self._setRowStatus(row, "error")
        self._saveProjectConfig()

    def _onSelectAllChanged(self, state: int) -> None:
        if self._syncingSelectAll:
            return

        checked = state == Qt.CheckState.Checked.value
        for row in range(self.ui.fileTable.rowCount()):
            box = self._rowCheckBox(row)
            if box is None:
                continue
            if box.isChecked() == checked:
                continue
            box.blockSignals(True)
            box.setChecked(checked)
            box.blockSignals(False)

        self._updateSelectionCount()

    def _onItemToggled(self) -> None:
        self._updateSelectionCount()

    def _onItemDeleted(self, filepath: str) -> None:
        row = self._findRowByPath(filepath)
        if row >= 0:
            self.ui.fileTable.removeRow(row)

        self._compileQueue = [p for p in self._compileQueue if p != filepath]
        QTimer.singleShot(0, self._saveProjectConfig)
        QTimer.singleShot(0, self._updateSelectionCount)

    def _onExecuteClicked(self) -> None:
        checked = self._checkedFilepaths()
        if not checked:
            return

        self._compileQueue = list(checked)
        self._compileTotal = len(checked)
        self._compileDone = 0
        self.ui.executeButton.setEnabled(False)
        self._showProgress(True)
        self._processNextInQueue()

    def _processNextInQueue(self) -> None:
        if not self._compileQueue:
            self._onAllCompileDone()
            return

        filepath = self._compileQueue.pop(0)
        row = self._findRowByPath(filepath)
        if row < 0:
            self._compileDone += 1
            self._updateProgress()
            self._processNextInQueue()
            return

        self._setRowStatus(row, "processing")
        command = f"# compile {self._rowModule(row)} {self._rowFilename(row)}"  # TODO: replace

        cfg = self._projectConfig
        if cfg.get("type") == "ssh":
            self._sshTask = SSHTask(
                hostname=cfg.get("host", ""),
                port=int(cfg.get("port", 22)),
                username=cfg.get("username", ""),
                password=cfg.get("password", ""),
            )
            connected = [False]
            task = self._sshTask

            def onFinished(_, fp=filepath, t=task):
                if not connected[0]:
                    connected[0] = True
                    t.execute(command)
                else:
                    self._setStatusByPath(fp, "done")
                    self._compileDone += 1
                    self._updateProgress()
                    self._saveProjectConfig()
                    self._processNextInQueue()

            def onError(_, fp=filepath):
                self._setStatusByPath(fp, "error")
                self._compileDone += 1
                self._updateProgress()
                self._saveProjectConfig()
                self._processNextInQueue()

            self._sshTask.finished.connect(onFinished)
            self._sshTask.error.connect(onError)
            self._sshTask.connect()
        else:
            # Local: placeholder — mark done immediately
            self._setRowStatus(row, "done")
            self._compileDone += 1
            self._updateProgress()
            self._saveProjectConfig()
            self._processNextInQueue()

    def _onAllCompileDone(self) -> None:
        self.ui.executeButton.setEnabled(True)
        QTimer.singleShot(2000, lambda: self._showProgress(False))

    def _onExportClicked(self) -> None:
        if self._projectPath is None:
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "导出清单",
            str(self._projectPath / "file_list.txt"),
            "文本文件 (*.txt)",
        )
        if not path:
            return

        lines = [f"{i['filename']}\t{i['module']}" for i in self._allItems()]
        Path(path).write_text("\n".join(lines), encoding="utf-8")

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #

    def _addRow(
        self,
        filename: str,
        filepath: str,
        module: str = "",
        status: str = "ready",
        checked: bool = True,
    ) -> None:
        row = self.ui.fileTable.rowCount()
        self.ui.fileTable.insertRow(row)
        self.ui.fileTable.setRowHeight(row, 40)

        checkBox = QCheckBox(self.ui.fileTable)
        checkBox.setChecked(checked)
        checkBox.stateChanged.connect(lambda _: self._onItemToggled())
        self.ui.fileTable.setCellWidget(row, 0, checkBox)

        filenameItem = QTableWidgetItem(filename)
        filenameItem.setData(Qt.ItemDataRole.UserRole, filepath)
        filenameItem.setIcon(_fileIcon(filename).icon())
        self.ui.fileTable.setItem(row, 1, filenameItem)

        statusItem = QTableWidgetItem("")
        statusItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.fileTable.setItem(row, 2, statusItem)
        self._setRowStatus(row, status)

        moduleItem = QTableWidgetItem(module)
        self.ui.fileTable.setItem(row, 3, moduleItem)

        deleteButton = TransparentToolButton(FluentIcon.DELETE, self.ui.fileTable)
        deleteButton.setFixedSize(28, 28)
        deleteButton.clicked.connect(lambda _, fp=filepath: self._onItemDeleted(fp))
        self.ui.fileTable.setCellWidget(row, 4, deleteButton)

    def _rowCheckBox(self, row: int) -> QCheckBox | None:
        widget = self.ui.fileTable.cellWidget(row, 0)
        if isinstance(widget, QCheckBox):
            return widget
        return None

    def _rowFilename(self, row: int) -> str:
        item = self.ui.fileTable.item(row, 1)
        return item.text() if item else ""

    def _rowFilepath(self, row: int) -> str:
        item = self.ui.fileTable.item(row, 1)
        if item is None:
            return ""
        return str(item.data(Qt.ItemDataRole.UserRole) or "")

    def _rowModule(self, row: int) -> str:
        item = self.ui.fileTable.item(row, 3)
        return item.text() if item else ""

    def _setRowModule(self, row: int, module: str) -> None:
        item = self.ui.fileTable.item(row, 3)
        if item is None:
            item = QTableWidgetItem("")
            self.ui.fileTable.setItem(row, 3, item)
        item.setText(module)

    def _rowStatus(self, row: int) -> str:
        item = self.ui.fileTable.item(row, 2)
        if item is None:
            return "ready"
        status = item.data(Qt.ItemDataRole.UserRole)
        return str(status or "ready")

    def _setRowStatus(self, row: int, status: str) -> None:
        text, bg, fg = _STATUS_META.get(status, (status, "#f5f5f5", "#757575"))
        item = self.ui.fileTable.item(row, 2)
        if item is None:
            item = QTableWidgetItem("")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.fileTable.setItem(row, 2, item)

        item.setData(Qt.ItemDataRole.UserRole, status)
        item.setText(text)
        item.setBackground(QColor(bg))
        item.setForeground(QColor(fg))

    def _setStatusByPath(self, filepath: str, status: str) -> None:
        row = self._findRowByPath(filepath)
        if row >= 0:
            self._setRowStatus(row, status)

    def _findRowByPath(self, filepath: str) -> int:
        for row in range(self.ui.fileTable.rowCount()):
            if self._rowFilepath(row) == filepath:
                return row
        return -1

    def _checkedFilepaths(self) -> list[str]:
        result: list[str] = []
        for row in range(self.ui.fileTable.rowCount()):
            box = self._rowCheckBox(row)
            if box is None or not box.isChecked():
                continue
            filepath = self._rowFilepath(row)
            if filepath:
                result.append(filepath)
        return result

    def _allItems(self) -> list[dict]:
        result = []
        for row in range(self.ui.fileTable.rowCount()):
            box = self._rowCheckBox(row)
            result.append(
                {
                    "filename": self._rowFilename(row),
                    "filepath": self._rowFilepath(row),
                    "module": self._rowModule(row),
                    "status": self._rowStatus(row),
                    "checked": box.isChecked() if box else False,
                }
            )
        return result

    def _clearItems(self) -> None:
        self.ui.fileTable.setRowCount(0)

    def _showEmptyState(self, show: bool) -> None:
        self.ui.addButton.setEnabled(not show)
        self.ui.browseButton.setEnabled(not show)
        self.ui.fileInput.setEnabled(not show)
        self.ui.selectAllBox.setEnabled(not show)
        self.ui.executeButton.setEnabled(False)

    def _updateSelectionCount(self) -> None:
        total = self.ui.fileTable.rowCount()
        checked = len(self._checkedFilepaths())

        self._syncingSelectAll = True
        if checked == total:
            self.ui.selectAllBox.setCheckState(Qt.CheckState.Checked)
        else:
            self.ui.selectAllBox.setCheckState(Qt.CheckState.Unchecked)
        self._syncingSelectAll = False

        if total:
            self.ui.selectionLabel.setText(f"已选中 {checked} 个项目")
            self.ui.executeButton.setEnabled(checked > 0 and not self._compileQueue)
        else:
            self.ui.selectionLabel.setText("")
            self.ui.executeButton.setEnabled(False)

    def _showProgress(self, show: bool) -> None:
        self.ui.progressBar.setVisible(show)
        self.ui.progressLabel.setVisible(show)
        if not show:
            self.ui.progressBar.setValue(0)
            self.ui.progressLabel.setText("")

    def _updateProgress(self) -> None:
        pct = (
            int(self._compileDone / self._compileTotal * 100)
            if self._compileTotal
            else 0
        )
        self.ui.progressBar.setValue(pct)
        self.ui.progressLabel.setText(
            f"处理中 {self._compileDone}/{self._compileTotal}"
        )

    def _saveProjectConfig(self) -> None:
        if self._projectPath is None:
            return

        configPath = self._projectPath / "config.json"
        bakPath = self._projectPath / "config.json.bak"
        self._projectConfig["file"] = self._allItems()
        with open(bakPath, "w", encoding="utf-8") as f:
            json.dump(self._projectConfig, f, indent=4, ensure_ascii=True)
        os.replace(bakPath, configPath)
