# Copyright (C) 2026 mogaitesheng
# SPDX-License-Identifier: LGPL-3.0-or-later

from .lib_replace import LibReplace
from .home import Home
from qfluentwidgets import FluentWindow, FluentIcon
from PySide6.QtWidgets import QWidget


class Gallery(FluentWindow):
    INSTANCE = None

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)
        self.setWindowTitle("ToolBox")
        self.resize(800, 600)

        self.installComponent()

    @staticmethod
    def get_instance() -> "Gallery":
        if Gallery.INSTANCE is None:
            Gallery.INSTANCE = Gallery()
        return Gallery.INSTANCE

    def installComponent(self) -> None:
        self.home = Home(self)
        self.addSubInterface(self.home, FluentIcon.HOME, "首页")
        self.libReplace = LibReplace(self)
        self.addSubInterface(self.libReplace, ":/images/binary.svg", "链接库替换")
