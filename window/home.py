from PySide6.QtWidgets import QWidget
from ui.home_ui import Ui_Home


class Home(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)
        self.ui = Ui_Home()
        self.ui.setupUi(self)
