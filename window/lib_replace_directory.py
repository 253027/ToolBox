from PySide6.QtWidgets import QVBoxLayout, QWidget
from ui.lib_replace_directory_ui import Ui_LibReplaceDirectory
from qfluentwidgets.common.style_sheet import setStyleSheet
from qfluentwidgets import Action, FluentIcon, FluentIconBase
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon


class LibReplaceDirectory(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)
        self._setupUi()
        self.setWindowFlag(Qt.WindowType.Window)

    def _setupUi(self) -> None:
        """initial ui components"""
        self.ui = Ui_LibReplaceDirectory()
        self.ui.setupUi(self)

    def setIcon(self, icon: str | QIcon | FluentIconBase) -> None:
        self.ui.IconWidget.setIcon(icon)
