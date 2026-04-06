import json
import os
from pathlib import Path

from PySide6.QtCore import Qt, QTimer, QSortFilterProxyModel
from PySide6.QtGui import QColor, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (
    QFileDialog,
    QWidget,
    QHeaderView,
    QSizePolicy,
    QHBoxLayout,
)
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


class ModuleFilterProxyModel(QSortFilterProxyModel):
    """Proxy model that filters rows by module name set."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_modules: set[str] = set()
        self.module_column = LibReplaceContent.MODULE_COLUMN_INDEX

    def setActiveModules(self, modules: set[str]) -> None:
        self.active_modules = set(modules)
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent) -> bool:
        if not self.active_modules:
            return True
        idx = self.sourceModel().index(source_row, self.module_column, source_parent)
        module = self.sourceModel().data(idx, Qt.ItemDataRole.DisplayRole) or ""
        return module in self.active_modules


class LibReplaceContent(QWidget):
    """Main content panel: shows the file list for the currently selected project."""

    SELECT_COLUMN_INDEX = 0
    FILENAME_COLUMN_INDEX = 1
    STATUS_COLUMN_INDEX = 2
    MODULE_COLUMN_INDEX = 3
    ACTION_COLUMN_INDEX = 4
    COLUMN_COUNT = 5

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
        self.ui.executeButton.clicked.connect(self._onExecuteClicked)
        self._installTableModel()
        self._setEnvDotState("idle")

    def _installTableModel(self) -> None:
        self._model = QStandardItemModel(0, LibReplaceContent.COLUMN_COUNT, self)
        self._model.setHeaderData(
            LibReplaceContent.SELECT_COLUMN_INDEX, Qt.Orientation.Horizontal, ""
        )
        self._model.setHeaderData(
            LibReplaceContent.FILENAME_COLUMN_INDEX,
            Qt.Orientation.Horizontal,
            "文件名",
        )
        self._model.setHeaderData(
            LibReplaceContent.STATUS_COLUMN_INDEX, Qt.Orientation.Horizontal, "状态"
        )
        self._model.setHeaderData(
            LibReplaceContent.MODULE_COLUMN_INDEX, Qt.Orientation.Horizontal, "模块"
        )
        self._model.setHeaderData(
            LibReplaceContent.ACTION_COLUMN_INDEX, Qt.Orientation.Horizontal, ""
        )
        self._model.itemChanged.connect(self._onModelItemChanged)

        self._proxy = ModuleFilterProxyModel(self)
        self._proxy.setSourceModel(self._model)

        self.ui.fileTable.setModel(self._proxy)
        self.ui.fileTable.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.ui.fileTable.setColumnWidth(LibReplaceContent.SELECT_COLUMN_INDEX, 48)
        self.ui.fileTable.setColumnWidth(LibReplaceContent.STATUS_COLUMN_INDEX, 80)
        self.ui.fileTable.setColumnWidth(LibReplaceContent.ACTION_COLUMN_INDEX, 48)
        self.ui.fileTable.setAlternatingRowColors(True)
        self.ui.fileTable.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.ui.fileTable.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        header = self.ui.fileTable.horizontalHeader()
        header.setSectionResizeMode(
            LibReplaceContent.SELECT_COLUMN_INDEX, QHeaderView.ResizeMode.Fixed
        )
        header.setSectionResizeMode(
            LibReplaceContent.FILENAME_COLUMN_INDEX, QHeaderView.ResizeMode.Stretch
        )
        header.setSectionResizeMode(
            LibReplaceContent.STATUS_COLUMN_INDEX, QHeaderView.ResizeMode.Fixed
        )
        header.setSectionResizeMode(
            LibReplaceContent.MODULE_COLUMN_INDEX, QHeaderView.ResizeMode.Stretch
        )
        header.setSectionResizeMode(
            LibReplaceContent.ACTION_COLUMN_INDEX, QHeaderView.ResizeMode.Fixed
        )

        self._activeModuleFilters: set[str] = set()
        self._deleteButtons: dict[str, TransparentToolButton] = {}

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
        self._activeModuleFilters = set(self._projectConfig.get("moduleFilters", []))

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

    def _onItemToggled(self) -> None:
        self._updateSelectionCount()

    def _onModelItemChanged(self, item: QStandardItem) -> None:
        # React to changes in the source model: selection or module edits
        try:
            col = item.index().column()
        except Exception:
            return
        if col == LibReplaceContent.SELECT_COLUMN_INDEX:
            self._updateSelectionCount()
            self._saveProjectConfig()
        elif col == LibReplaceContent.MODULE_COLUMN_INDEX:
            # module changed -> module filter UI disabled, skip view update
            pass

    def _onItemDeleted(self, filepath: str) -> None:
        row = self._findRowByPath(filepath)
        if row >= 0:
            self._model.removeRow(row)
        self._deleteButtons.pop(filepath, None)

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
        # Column 0: checkable selection
        selItem = QStandardItem()
        selItem.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
        selItem.setCheckState(
            Qt.CheckState.Checked if checked else Qt.CheckState.Unchecked
        )
        selItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        # Column 1: filename (store filepath in UserRole)
        nameItem = QStandardItem(_fileIcon(filename).icon(), filename)
        nameItem.setData(filepath, Qt.ItemDataRole.UserRole)
        nameItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        # Column 2: status
        statusItem = QStandardItem("")
        statusItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        # Column 3: module
        module_item = QStandardItem(module)
        module_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        # Column 4: placeholder for delete widget
        actionItem = QStandardItem("")
        actionItem.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self._model.appendRow([selItem, nameItem, statusItem, module_item, actionItem])

        deleteButton = TransparentToolButton(FluentIcon.DELETE, self.ui.fileTable)
        deleteButton.setFixedSize(24, 24)
        deleteButton.setFont("")
        deleteButton.clicked.connect(lambda _, fp=filepath: self._onItemDeleted(fp))
        self._deleteButtons[filepath] = deleteButton
        self._rebuildIndexWidgets()

    # legacy placeholder removed: row-level widgets are now represented in the model

    def _rowFilename(self, row: int) -> str:
        item = self._model.item(row, LibReplaceContent.FILENAME_COLUMN_INDEX)
        return item.text() if item else ""

    def _rowFilepath(self, row: int) -> str:
        item = self._model.item(row, LibReplaceContent.FILENAME_COLUMN_INDEX)
        if item is None:
            return ""
        return str(item.data(Qt.ItemDataRole.UserRole) or "")

    def _rowModule(self, row: int) -> str:
        item = self._model.item(row, LibReplaceContent.MODULE_COLUMN_INDEX)
        return item.text() if item else ""

    def _setRowModule(self, row: int, module: str) -> None:
        item = self._model.item(row, LibReplaceContent.MODULE_COLUMN_INDEX)
        if item is None:
            item = QStandardItem("")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._model.setItem(row, LibReplaceContent.MODULE_COLUMN_INDEX, item)
        item.setText(module)

    def _rowStatus(self, row: int) -> str:
        item = self._model.item(row, LibReplaceContent.STATUS_COLUMN_INDEX)
        if item is None:
            return "ready"
        status = item.data(Qt.ItemDataRole.UserRole)
        return str(status or "ready")

    def _setRowStatus(self, row: int, status: str) -> None:
        text, bg, fg = _STATUS_META.get(status, (status, "#f5f5f5", "#757575"))
        item = self._model.item(row, LibReplaceContent.STATUS_COLUMN_INDEX)
        if item is None:
            item = QStandardItem("")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._model.setItem(row, LibReplaceContent.STATUS_COLUMN_INDEX, item)

        item.setData(status, Qt.ItemDataRole.UserRole)
        item.setText(text)
        item.setBackground(QColor(bg))
        item.setForeground(QColor(fg))

    def _setStatusByPath(self, filepath: str, status: str) -> None:
        row = self._findRowByPath(filepath)
        if row >= 0:
            self._setRowStatus(row, status)

    # ----------------- Module filter (QComboBox + proxy) ----------------- #
    def _rebuildModuleCombo(self) -> None:
        """Rebuild the combobox model with current modules (checkable items)."""
        model = getattr(self, "_moduleComboModel", None)
        if model is None:
            self._moduleComboModel = QStandardItemModel(self)
            model = self._moduleComboModel
        model.blockSignals(True)
        model.clear()
        modules = set()
        # gather from source model
        for src_row in range(self._model.rowCount()):
            item = self._model.item(src_row, LibReplaceContent.FILENAME_COLUMN_INDEX)
            m = str(item.text()).strip() if item else ""
            if m:
                modules.add(m)
        modules = sorted(modules)
        if not modules:
            it = QStandardItem("无模块")
            it.setEnabled(False)
            model.appendRow(it)
            return
        # add select/clear pseudo-actions as items
        # add module items
        for mod in modules:
            it = QStandardItem(mod)
            it.setFlags(it.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            it.setCheckState(
                Qt.CheckState.Checked
                if mod in self._activeModuleFilters
                else Qt.CheckState.Unchecked
            )
            model.appendRow(it)
        model.blockSignals(False)
        self._proxy.setActiveModules(self._activeModuleFilters)
        self._rebuildIndexWidgets()

    def _onModuleComboItemChanged(self, item: QStandardItem) -> None:
        # called when user toggles a module checkbox in combobox's model
        mod = str(item.text())
        checked = item.checkState() == Qt.CheckState.Checked
        if checked:
            self._activeModuleFilters.add(mod)
        else:
            self._activeModuleFilters.discard(mod)
        self._proxy.setActiveModules(self._activeModuleFilters)
        QTimer.singleShot(0, self._saveProjectConfig)

    def _applyModuleFilter(self) -> None:
        # backward-compat helper: apply active filters to proxy
        self._proxy.setActiveModules(self._activeModuleFilters)
        try:
            self._rebuildIndexWidgets()
        except Exception:
            pass
        self._updateSelectionCount()

    def _rebuildIndexWidgets(self) -> None:
        """Attach per-row widgets (delete buttons) to the view using proxy mapping."""
        for src_row in range(self._model.rowCount()):
            name_item = self._model.item(
                src_row, LibReplaceContent.FILENAME_COLUMN_INDEX
            )
            if name_item is None:
                continue
            filepath = str(name_item.data(Qt.ItemDataRole.UserRole) or "")
            btn = self._deleteButtons.get(filepath)
            if btn is None:
                continue
            src_index = self._model.index(
                src_row, LibReplaceContent.ACTION_COLUMN_INDEX
            )
            proxy_index = self._proxy.mapFromSource(src_index)
            if proxy_index.isValid():
                # create a container widget with centered layout so the button is centered
                container = QWidget(self.ui.fileTable)
                layout = QHBoxLayout(container)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                # reparent button into container and add to layout
                btn.setParent(container)
                layout.addWidget(btn)
                self.ui.fileTable.setIndexWidget(proxy_index, container)
                self.ui.fileTable.setRowHeight(proxy_index.row(), 40)

    def _findRowByPath(self, filepath: str) -> int:
        for src_row in range(self._model.rowCount()):
            item = self._model.item(src_row, LibReplaceContent.FILENAME_COLUMN_INDEX)
            if item is None:
                continue
            if str(item.data(Qt.ItemDataRole.UserRole) or "") == filepath:
                return src_row
        return -1

    def _checkedFilepaths(self) -> list[str]:
        result: list[str] = []
        # iterate over visible rows in proxy
        for proxy_row in range(self._proxy.rowCount()):
            proxy_index = self._proxy.index(
                proxy_row, LibReplaceContent.SELECT_COLUMN_INDEX
            )
            src_index = self._proxy.mapToSource(proxy_index)
            src_row = src_index.row()
            item = self._model.item(src_row, LibReplaceContent.SELECT_COLUMN_INDEX)
            if item is None:
                continue
            if item.checkState() != Qt.CheckState.Checked:
                continue
            fp_item = self._model.item(src_row, LibReplaceContent.FILENAME_COLUMN_INDEX)
            if fp_item is None:
                continue
            filepath = str(fp_item.data(Qt.ItemDataRole.UserRole) or "")
            if filepath:
                result.append(filepath)
        return result

    def _allItems(self) -> list[dict]:
        result = []
        for src_row in range(self._model.rowCount()):
            name_item = self._model.item(
                src_row, LibReplaceContent.FILENAME_COLUMN_INDEX
            )
            fp = (
                str(name_item.data(Qt.ItemDataRole.UserRole) or "") if name_item else ""
            )
            filename = name_item.text() if name_item else ""
            module_item = self._model.item(
                src_row, LibReplaceContent.MODULE_COLUMN_INDEX
            )
            module = module_item.text() if module_item else ""
            status_item = self._model.item(
                src_row, LibReplaceContent.STATUS_COLUMN_INDEX
            )
            status = (
                str(status_item.data(Qt.ItemDataRole.UserRole) or "ready")
                if status_item
                else "ready"
            )
            sel_item = self._model.item(src_row, LibReplaceContent.SELECT_COLUMN_INDEX)
            checked = (
                sel_item.checkState() == Qt.CheckState.Checked if sel_item else False
            )
            result.append(
                {
                    "filename": filename,
                    "filepath": fp,
                    "module": module,
                    "status": status,
                    "checked": checked,
                }
            )
        return result

    def _clearItems(self) -> None:
        # clear source model rows
        if self._model.rowCount() > 0:
            self._model.removeRows(0, self._model.rowCount())

    def _showEmptyState(self, show: bool) -> None:
        self.ui.addButton.setEnabled(not show)
        self.ui.browseButton.setEnabled(not show)
        self.ui.fileInput.setEnabled(not show)
        self.ui.executeButton.setEnabled(False)

    def _updateSelectionCount(self) -> None:
        total = self._proxy.rowCount()
        checked = len(self._checkedFilepaths())

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
        self._projectConfig["moduleFilters"] = list(self._activeModuleFilters)
        with open(bakPath, "w", encoding="utf-8") as f:
            json.dump(self._projectConfig, f, indent=4, ensure_ascii=True)
        os.replace(bakPath, configPath)
