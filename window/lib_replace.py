from PySide6.QtWidgets import QVBoxLayout, QWidget
from ui.lib_replace_ui import Ui_LibReplace
from .lib_replace_directory import LibReplaceDirectory
from qfluentwidgets.common.style_sheet import setStyleSheet
from qfluentwidgets import Action, FluentIcon
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon


class LibReplace(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)
        self._setupUi()
        self.setWindowFlag(Qt.WindowType.Window)
        self._installStyleSheet()
        self._installRequireSettings()

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
        height = 0
        nums = self.ui.ScrollAreaWidgetContentsLayout.count()
        for i in range(nums):
            item = self.ui.ScrollAreaWidgetContentsLayout.itemAt(i)
            if not item:
                continue
            widget = item.widget()
            if not widget:
                continue
            height += widget.height()
        self.ui.ScrollAreaWidgetContents.setFixedHeight(
            height + (nums - 1) * self.ui.ScrollAreaWidgetContentsLayout.spacing()
        )

    def onCreateActionTriggered(self) -> None:
        """create action handler"""
        widget = LibReplaceDirectory()
        widget.setIcon(FluentIcon.FOLDER)
        self._addContentWidget(widget)

    def onOpenActionTriggered(self) -> None:
        """open action handler"""
        pass
