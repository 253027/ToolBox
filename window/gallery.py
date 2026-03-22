# Copyright (C) 2026 mogaitesheng
# SPDX-License-Identifier: LGPL-3.0-or-later

from qfluentwidgets import FluentWindow
from PySide6.QtWidgets import QWidget


class Gallery(FluentWindow):
    INSTANCE = None

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)
        self.setWindowTitle("Gallery")
        self.resize(800, 600)

    @staticmethod
    def get_instance() -> "Gallery":
        if Gallery.INSTANCE is None:
            Gallery.INSTANCE = Gallery()
        return Gallery.INSTANCE
