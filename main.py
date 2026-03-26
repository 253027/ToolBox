# Copyright (C) 2026 mogaitesheng
# SPDX-License-Identifier: LGPL-3.0-or-later

import sys
import resource_rc
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from window.gallery import Gallery


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    Gallery.getInstance().show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
