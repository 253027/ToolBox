# Copyright (C) 2026 mogaitesheng
# SPDX-License-Identifier: LGPL-3.0-or-later

from PySide6.QtGui import QMouseEvent, QPainter, QColor
from PySide6.QtWidgets import QHeaderView, QWidget, QStyleOptionButton, QStyle
from PySide6.QtCore import QObject, QPoint, QRect, QRectF, Qt, Signal
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
    toggle = Signal(bool)

    class ResizeSide(Enum):
        LEFT = "left"
        RIGHT = "right"

    def __init__(self, parent: QWidget | None = None):
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.sectionResized.connect(self.onSectionResized)
        self.ignoreSignal = False
        self.headerChecked = False
        self.styleSource = None

    def setStyleSource(self, widget: QWidget | None) -> None:
        """Set an external widget as style source for the header checkbox.

        When set, the header will use `widget.style()` / `opt.initFrom(widget)`
        to render the checkbox so it visually matches that widget.
        """
        self.styleSource = widget

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

    def _paintFirstColumn(self, painter: QPainter, rect: QRect) -> None:
        """
        paint first column for checkbox
        """
        size = 16  # checkbox square size in pixels
        x = rect.x() + (rect.width() - size) // 2  # center horizontally
        y = rect.y() + (rect.height() - size) // 2  # center vertically
        try:
            opt = QStyleOptionButton()
            styleSrc = self.styleSource if self.styleSource is not None else self
            try:
                opt.initFrom(styleSrc)
            except Exception:
                pass
            opt.rect = QRect(x, y, size, size)
            if hasattr(QStyle, "CE_CheckBox") and hasattr(QStyle, "State_On"):
                state = getattr(QStyle, "State_On")
                if self.headerChecked:
                    opt.state = opt.state | state
                else:
                    opt.state = opt.state & ~state

                sytle = styleSrc.style() if hasattr(styleSrc, "style") else self.style()
                checkbox = getattr(QStyle, "CE_CheckBox")
                sytle.drawControl(checkbox, opt, painter, styleSrc)
                return
            raise RuntimeError("QStyle checkbox constants unavailable; fallback")
        except Exception:
            painter.save()  # save painter state
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            pen = painter.pen()
            pen.setColor(QColor("black"))
            painter.setPen(pen)
            painter.setBrush(QColor("white"))
            cb_rect = QRect(x, y, size, size)
            # painter.drawRect(cb_rect)
            painter.drawRoundedRect(cb_rect, 4.5, 4.5)
            if self.headerChecked:
                inner = QRect(x + 3, y + 3, size - 6, size - 6)
                painter.fillRect(inner, QColor("black"))
            painter.restore()

    def paintSection(self, painter: QPainter, rect: QRect, logicalIndex: int) -> None:
        super().paintSection(painter, rect, logicalIndex)
        if logicalIndex == 0:
            self._paintFirstColumn(painter, rect)

    def _onFirstColumnClicked(self, pos: QPoint) -> None:
        size = 16
        start = self.sectionViewportPosition(0)
        x = start + (self.sectionSize(0) - size) // 2
        y = (self.height() - size) // 2
        rect = QRect(x, y, size, size)
        if rect.contains(pos):
            self.headerChecked = not self.headerChecked
            try:
                self.updateSection(0)
            except Exception:
                self.update()
            try:
                self.toggle.emit(self.headerChecked)
            except Exception:
                pass
            return

    def _handleColumnPressEvent(self, event: QMouseEvent) -> None:
        """Handle mouse press to toggle header checkbox when clicked."""
        pos = event.pos()
        index = -1
        for i in range(self.count()):
            start = self.sectionViewportPosition(i)
            size = self.sectionSize(i)
            if start <= pos.x() < start + size:
                index = i
                break
        if index == 0:
            self._onFirstColumnClicked(pos)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._handleColumnPressEvent(event)
        super().mousePressEvent(event)
