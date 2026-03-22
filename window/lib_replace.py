from PySide6.QtWidgets import QWidget

from ui.lib_replace_ui import Ui_Form


class LibReplace(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
