import weakref
from typing import ClassVar

from PySide6.QtWidgets import QVBoxLayout, QWidget
from ui.lib_replace_directory_ui import Ui_LibReplaceDirectory
from qfluentwidgets.common.style_sheet import setStyleSheet
from qfluentwidgets import Action, FluentIcon, FluentIconBase
from PySide6.QtCore import QDate, Qt, QDateTime, QEvent
from PySide6.QtGui import QFocusEvent, QFont, QIcon, QEnterEvent, QMouseEvent


class LibReplaceDirectory(QWidget):

    record: ClassVar[set[weakref.ref["LibReplaceDirectory"]]] = set()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)
        self._setupUi()
        self.setWindowFlag(Qt.WindowType.Window)
        self._installRequireSettings()
        self._installStyleSheet()
        self.focus = False
        self.name = ""
        LibReplaceDirectory.record.add(weakref.ref(self))

    def __del__(self) -> None:
        LibReplaceDirectory.record.discard(weakref.ref(self))

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

    def getTitle(self) -> str:
        return self.ui.Directory.text()

    def setName(self, name: str) -> None:
        self.name = name

    def getName(self) -> str:
        return self.name

    def setDate(self, date: QDateTime) -> None:
        """
            set date and show relative time

        Args:
            date: the date to beshow
        """
        diff = date.secsTo(QDateTime.currentDateTime())

        if diff < 60:  # not over a minute
            text = "刚刚更新"
        elif diff < 3600:  # not over an hour
            minutes = diff // 60
            text = f"更新于 {minutes}分钟前"
        elif diff < 86400:  # not over a day
            hours = diff // 3600
            text = f"更新于 {hours}小时前"
        elif diff < 172800:  # not over 2 days
            text = "更新于 昨天"
        elif diff < 604800:  # not over a week
            days = diff // 86400
            text = f"更新于 {days}天前"
        elif diff < 2592000:  # not over a month
            weeks = diff // 604800
            text = f"更新于 {weeks}周前"
        else:
            text = f"更新于 {date.toString('yyyy-MM-dd')}"

        self.date = date
        self.ui.Date.setText(text)
        self.ui.Date.setToolTip(date.toString("yyyy-MM-dd hh:mm:ss"))

    def updateStyle(self) -> None:
        self.ui.Content.style().polish(self.ui.Content)

    def enterEvent(self, event: QEnterEvent) -> None:
        if self.focus:
            return
        self.ui.Content.setProperty("hover", True)
        self.updateStyle()
        super().enterEvent(event)

    def leaveEvent(self, event: QEvent) -> None:
        self.ui.Content.setProperty("hover", False)
        self.updateStyle()
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.installStyle()

    def clearStyle(self) -> None:
        self.focus = False
        self.ui.Content.setProperty("focused", False)
        self.ui.Content.setProperty("hover", False)
        self.updateStyle()

    def installStyle(self) -> None:
        self.focus = True
        self.ui.Content.setProperty("focused", True)
        self.ui.Content.setProperty("hover", False)
        for widgetRef in LibReplaceDirectory.record:
            widget = widgetRef()
            if widget and widget != self:
                widget.clearStyle()
        self.updateStyle()

    def setConfig(self, config: dict) -> None:
        self.config = config

    def getConfig(self) -> dict:
        return self.config
