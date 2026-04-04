# Copyright (C) 2026 mogaitesheng
# SPDX-License-Identifier: LGPL-3.0-or-later

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject, QRectF, Qt
from qfluentwidgets import FluentIconBase, MessageBox
from qfluentwidgets.components.widgets.button import (
    TransparentDropDownToolButton,
    ToolButton,
)
from qfluentwidgets.components.widgets import RoundMenu


class DropDownIconButton(TransparentDropDownToolButton):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)
        self.setMenu(RoundMenu(parent=self))

    def _drawIcon(self, icon, painter, rect: QRectF) -> None:
        rect.moveLeft((self.width() - rect.width()) // 2)
        return ToolButton._drawIcon(self, icon, painter, rect)

    def paintEvent(self, e) -> None:
        ToolButton.paintEvent(self, e)


def noticeBox(title: str, content: str, parent: QObject) -> None:
    messageBox = MessageBox(title=title, content=content, parent=parent)
    messageBox.contentLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    messageBox.yesButton.setText("确定")
    messageBox.cancelButton.hide()
    messageBox.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
    messageBox.show()
