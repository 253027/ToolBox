from PySide6.QtWidgets import QVBoxLayout, QWidget
from ui.lib_replace_directory_ui import Ui_LibReplaceDirectory
from qfluentwidgets.common.style_sheet import setStyleSheet
from qfluentwidgets import Action, FluentIcon, FluentIconBase
from PySide6.QtCore import QDate, QEvent, Qt
from PySide6.QtGui import QEnterEvent, QFocusEvent, QFont, QIcon


class LibReplaceDirectory(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)
        self._setupUi()
        self.setWindowFlag(Qt.WindowType.Window)
        self._installRequireSettings()
        self._installStyleSheet()

    def _setupUi(self) -> None:
        """initial ui components"""
        self.ui = Ui_LibReplaceDirectory()
        self.ui.setupUi(self)

    def _installStyleSheet(
        self, path: str = ":/style/lib_replace_directory.qss"
    ) -> None:
        """style sheet installer"""
        setStyleSheet(self.ui.Content, path)

    def _installRequireSettings(self) -> None:
        """require settings installer"""
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

    def setIcon(self, icon: str | QIcon | FluentIconBase) -> None:
        self.ui.IconWidget.setIcon(icon)

    def setTitle(self, title: str) -> None:
        self.ui.Directory.setText(title)

    def setDate(self, date: QDate) -> None:
        pass

    def updateStyle(self) -> None:
        self.ui.Content.style().polish(self.ui.Content)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.ui.Content.setProperty("hover", True)
        self.updateStyle()
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self.ui.Content.setProperty("hover", False)
        self.updateStyle()
        super().leaveEvent(event)

    def focusInEvent(self, event: QFocusEvent) -> None:
        self.ui.Content.setProperty("focused", True)
        self.ui.Content.setProperty("hover", False)
        self.updateStyle()
        super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent) -> None:
        self.ui.Content.setProperty("focused", False)
        self.updateStyle()
        super().focusOutEvent(event)
