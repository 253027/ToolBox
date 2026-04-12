# Copyright (C) 2026 mogaitesheng
# SPDX-License-Identifier: LGPL-3.0-or-later

from PySide6.QtWidgets import QHeaderView, QWidget
from PySide6.QtCore import QObject, QRectF, Qt
from enum import Enum
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


class HorizontalHeaderView(QHeaderView):

    class ResizeSide(Enum):
        LEFT = "left"
        RIGHT = "right"

    def __init__(self, parent: QWidget | None = None):
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.sectionResized.connect(self.onSectionResized)
        self.ignoreSignal = False

    def setBlockSignals(self, state: bool) -> None:
        self.ignoreSignal = state

    def isFirstColumn(self, index: int) -> bool:
        """
        Check if the index is the first visible column
        """
        for i in range(index):
            if not self.isSectionHidden(i):
                return False
        return True

    def isLastColumn(self, index: int) -> bool:
        """
        Check if the index is the last visible column
        """
        if index + 1 > self.count():
            raise ValueError("index out of range")
        for i in range(index + 1, self.count()):
            if not self.isSectionHidden(i):
                return False
        return True

    def getColumnSide(self, index: int) -> ResizeSide:
        """
        Get the resize side of the column
        """
        offset = self.cursor().pos().x() - self.mapToGlobal(self.pos()).x()
        start = self.sectionViewportPosition(index)
        end = start + self.sectionSize(index)
        if abs(offset - start) < abs(offset - end):
            return HorizontalHeaderView.ResizeSide.LEFT
        return HorizontalHeaderView.ResizeSide.RIGHT

    def onSectionResized(self, logicalIndex: int, oldSize: int, newSize: int) -> None:
        if logicalIndex < 0 or logicalIndex >= self.count():
            raise ValueError("index out of range")

        if self.ignoreSignal:
            return

        try:
            self.blockSignals(True)
            self.setBlockSignals(True)
            side = self.getColumnSide(logicalIndex)

            if (
                self.isFirstColumn(logicalIndex)
                and side == HorizontalHeaderView.ResizeSide.LEFT
            ) or (
                self.isLastColumn(logicalIndex)
                and side == HorizontalHeaderView.ResizeSide.RIGHT
            ):
                self.resizeSection(logicalIndex, oldSize)
                return

            def getVacantSectionInfo(start: int, end: int) -> dict[int, int]:
                records: dict[int, int] = {}
                next = 1 if end > start else -1
                for i in range(start, end, next):
                    if self.isSectionHidden(i):
                        continue
                    records[i] = self.sectionSize(i)
                return records

            if side == HorizontalHeaderView.ResizeSide.LEFT:
                memo = getVacantSectionInfo(0, logicalIndex)
            else:
                memo = getVacantSectionInfo(logicalIndex + 1, self.count())
            vacant = sum(memo.values())

            if newSize > oldSize:  # expand
                need = newSize - oldSize
                limit = self.minimumSectionSize()
                vacant -= limit * len(memo)
                if need > vacant:  # too large reject to expand
                    self.resizeSection(logicalIndex, oldSize)
                    return

                for i in sorted(memo.keys(), reverse=(side == self.ResizeSide.LEFT)):
                    catSub = min(need, memo[i] - limit)
                    memo[i] -= catSub
                    need -= catSub
                    self.resizeSection(i, memo[i])
                    if need == 0:
                        break
            else:  # shrink
                need = oldSize - newSize
                limit = self.maximumSectionSize()
                vacant = limit * len(memo) - vacant
                if need > vacant:  # too large reject to shrink
                    self.resizeSection(logicalIndex, oldSize)
                    return

                for i in sorted(memo.keys(), reverse=side == self.ResizeSide.LEFT):
                    catAdd = min(need, limit - memo[i])
                    memo[i] += catAdd
                    need -= catAdd
                    self.resizeSection(i, memo[i])
                    if need == 0:
                        break

        finally:
            self.setBlockSignals(False)
            self.blockSignals(False)
