from PySide6.QtWidgets import QVBoxLayout, QWidget, QFileDialog
from ui import noticeBox
from ui.lib_replace_ui import Ui_LibReplace
from .lib_replace_directory import LibReplaceDirectory
from qfluentwidgets.common.style_sheet import setStyleSheet
from qfluentwidgets import Action, FluentIcon
from PySide6.QtCore import QDate, QDateTime, QTimer, Qt
from PySide6.QtGui import QFont, QIcon
from pathlib import Path
import json


class LibReplace(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)
        self._setupUi()
        self.setWindowFlag(Qt.WindowType.Window)
        self._installStyleSheet()
        self._installRequireSettings()
        self._initialContentWidgets()
        self._createrTime()

    def _setupUi(self) -> None:
        """initial ui components"""
        self.ui = Ui_LibReplace()
        self.ui.setupUi(self)
        self.ui.ProjectsHeaderButton.setIcon(FluentIcon.ADD_TO)
        # escape: QFont::setPointSize: Point size <= 0 (-1), must be greater than 0
        self.ui.ProjectsHeaderButton.setFont("")

    def _installStyleSheet(self, path: str = ":/style/lib_replace.qss") -> None:
        """style sheet installer"""
        setStyleSheet(self.ui.LeftSideBarWidget, path)

    def _installRequireSettings(self) -> None:
        """require settings installer"""
        self.ui.ProjectsHeaderButton.menu().addAction(
            Action(
                FluentIcon.ADD,
                "新建工程",
                triggered=self.onCreateActionTriggered,
                parent=self.ui.ProjectsHeaderButton.menu(),
            ),
        )
        self.ui.ProjectsHeaderButton.menu().addAction(
            Action(
                FluentIcon.FOLDER_ADD,
                "打开工程",
                triggered=self.onOpenActionTriggered,
                parent=self.ui.ProjectsHeaderButton.menu(),
            )
        )

    def _addContentWidget(self, widget: QWidget) -> None:
        """add content widget to ScrollArea"""
        widget.setParent(self.ui.ScrollArea)
        self.ui.ScrollAreaWidgetContentsLayout.addWidget(widget)
        self._updateContent()

    def _updateContent(self) -> None:
        nums = self.ui.ScrollAreaWidgetContentsLayout.count()
        if nums == 0:
            self.ui.ScrollAreaWidgetContents.setFixedHeight(self.ui.ScrollArea.height())
            return
        height = (nums - 1) * self.ui.ScrollAreaWidgetContentsLayout.spacing() + 6
        for widget in self.getAllContentWidgets():
            height += widget.height()
        self.ui.ScrollAreaWidgetContents.setFixedHeight(height)

    def onCreateActionTriggered(self) -> None:
        """create action handler"""
        from .lib_replace_project_creater import ProjectCreater

        creater = ProjectCreater(self)
        creater.input.connect(self.onProjectInput)
        creater.show()

    def onProjectInput(
        self,
        root: str,
        name: str,
        remote: str,
        host: str,
        port: str,
        username: str,
        password: str,
        type: str,
    ) -> None:
        """project input handler"""

        # Create project directory path
        projectPath = Path(root) / name
        projectPath.mkdir(parents=True, exist_ok=True)

        # Prepare config data with timestamp
        configData = {
            "type": type,
            "create_time": QDateTime()
            .currentDateTime()
            .toString("yyyy-MM-dd HH:mm:ss"),
            "file": [],
            "remote": remote,
            "host": host,
            "port": port,
            "username": username,
            "password": password,
        }

        # Write config to config.json file in project directory
        configPath = projectPath / "config.json"
        with open(configPath, "w", encoding="utf-8") as file:
            json.dump(configData, file, indent=4, ensure_ascii=True)

        widget = self._addProject(projectPath, configData)
        if widget:
            widget.installStyle()
            self._saveToConfig()

    def onOpenActionTriggered(self) -> None:
        """open a existing directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择目录",
            "",
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks,
        )
        if not directory:
            return
        config = self.parseConfig(Path(directory) / "config.json")
        widget = self._addProject(Path(directory), config)
        if widget:
            widget.installStyle()
            self._saveToConfig()

    def getAllContentWidgets(self) -> list[LibReplaceDirectory]:
        widgetsRecord = []
        nums = self.ui.ScrollAreaWidgetContentsLayout.count()
        for i in range(nums):
            item = self.ui.ScrollAreaWidgetContentsLayout.itemAt(i)
            if not item:
                continue
            widget = item.widget()
            if not widget or not isinstance(widget, LibReplaceDirectory):
                continue
            widgetsRecord.append(widget)
        return widgetsRecord

    def _addProject(self, path: Path, config: dict) -> LibReplaceDirectory | None:
        """add a project to the list, only verify the project don't create"""
        if len(config) == 0:
            noticeBox("错误", "配置文件不存在", self)
            return None

        for widget in self.getAllContentWidgets():
            if Path(widget.getName()) == path:
                return None

        configPath = path / "config.json"
        content = self._verify(configPath)
        if not content:
            noticeBox("错误", "配置文件格式错误", self)
            return None

        widget = LibReplaceDirectory()
        widget.setIcon(FluentIcon.FOLDER)
        widget.setDate(
            QDateTime.fromString(content["create_time"], "yyyy-MM-dd HH:mm:ss")
        )
        widget.setTitle(configPath.parent.name)
        widget.setName(str(path))
        widget.setConfig(config)
        self._addContentWidget(widget)
        return widget

    def _verify(self, path: Path) -> dict | None:
        """verify the config and return config dict if valid"""
        if not path.exists() or not path.is_file():
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                config = json.load(f)
                if "create_time" not in config:
                    return None

                if "file" not in config or not isinstance(config["file"], list):
                    return None

                if "type" not in config or config["type"] not in ["local", "ssh"]:
                    return None

                return config
        except Exception:
            return None

    def _saveToConfig(self) -> None:
        """save current project paths to config file"""
        import os

        configPath = Path("config.json.bak").absolute()
        with open(configPath, "w", encoding="utf-8") as file:
            config = {"projects": []}
            for widget in self.getAllContentWidgets():
                config["projects"].append(widget.getName())
            json.dump(config, file, indent=4, ensure_ascii=False)
        os.replace(configPath, Path("config.json").absolute())

    def _initialContentWidgets(self) -> None:
        """initialize content widgets and load projects from config file"""
        configPath = Path("config.json").absolute()

        try:
            with open(configPath, "r", encoding="utf-8") as file:
                config = json.load(file)
                for project in config["projects"]:
                    path = Path(project)
                    self._addProject(path, self.parseConfig(path / "config.json"))
            self._saveToConfig()  # update the config file
        except FileNotFoundError:
            config = {"projects": []}
            with open(configPath, "w", encoding="utf-8") as file:
                json.dump(config, file, indent=4)
        except Exception:
            raise RuntimeError("read system config failed")

    def parseConfig(self, path: Path) -> dict:
        """parse config file, the path must be end with 'config.json'"""
        try:
            with open(path, "r", encoding="utf-8") as file:
                config = json.load(file)
                return {
                    "type": config["type"],
                    "create_time": config["create_time"],
                    "file": config["file"],
                    "remote": config["remote"],
                    "host": config["host"],
                    "port": config["port"],
                    "username": config["username"],
                    "password": config["password"],
                }
        except Exception:
            return {}

    def _createrTime(self) -> None:
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.onTimeout)
        self.timer.start(1000)  # 1 second

    def onTimeout(self) -> None:
        widgets = self.getAllContentWidgets()
        for widget in widgets:
            config = widget.getConfig()
            if "create_time" not in config:
                continue
            widget.setDate(
                QDateTime.fromString(config["create_time"], "yyyy-MM-dd HH:mm:ss")
            )
