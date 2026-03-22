import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
