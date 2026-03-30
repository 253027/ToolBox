from PySide6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QFileDialog,
    QLabel,
    QLineEdit,
    QWidget,
)
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QFont, QShowEvent, QRegularExpressionValidator
from ui.lib_replace_project_creater_ui import Ui_ProjectCreater
from qframelesswindow import FramelessDialog, TitleBar
from qfluentwidgets.common.style_sheet import setStyleSheet


class ProjectTitleBar(TitleBar):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        label = QLabel("新建工程")
        font = label.font()
        font.setFamilies(["Segoe UI"])
        font.setPointSize(11)
        font.setBold(True)
        label.setFont(font)
        self.hBoxLayout.insertWidget(0, label, 0, Qt.AlignmentFlag.AlignLeft)
        self.setContentsMargins(10, 0, 0, 0)
        self.minBtn.hide()
        self.maxBtn.hide()
        self.setDoubleClickEnabled(False)
        self.setObjectName("ProjectTitleBar")


class ProjectCreater(FramelessDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._setupUi()
        self.setFixedSize(400, 350)
        self._installStyleSheet()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setResizeEnabled(False)
        self._installRequireSettings()

    def __del__(self) -> None:
        print("ProjectCreater deleted")

    def _setupUi(self):
        self.setTitleBar(ProjectTitleBar(self))
        self.ui = Ui_ProjectCreater()
        self.ui.setupUi(self)

        # set group
        self.buttonGroup = QButtonGroup(self)
        self.buttonGroup.addButton(self.ui.LocalButton)
        self.buttonGroup.addButton(self.ui.SshButton)

    def _installRequireSettings(self) -> None:
        self.ui.DirectoryButton.clicked.connect(self.onDirectoryButtonClicked)
        self.ui.LocalButton.clicked.connect(self.onLocalButtonClicked)
        self.ui.SshButton.clicked.connect(self.onSshButtonClicked)
        self.ui.CloseButton.clicked.connect(lambda: self.close())
        self.ui.AcceptButton.clicked.connect(self.onAcceptButtonClicked)
        self._setupInputValidators()

    def _installStyleSheet(
        self, path: str = ":/style/lib_replace_project_creater.qss"
    ) -> None:
        """style sheet installer"""
        setStyleSheet(self.ui.ContentArea, path)
        setStyleSheet(self.ui.SshArea, path)

    def _setupInputValidators(self) -> None:
        """Set up validators for input fields"""
        # IPv4 address validator (dotted decimal format, each octet 0-255)
        ipPattern = QRegularExpression(
            r"^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}"
            r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$"
        )
        self.ui.HostInput.setValidator(QRegularExpressionValidator(ipPattern, self))

        # Port number validator (range 1-65535)
        portPattern = QRegularExpression(
            r"^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$"
        )
        self.ui.PortInput.setValidator(QRegularExpressionValidator(portPattern, self))

    def onLocalButtonClicked(self) -> None:
        if not self.ui.SshArea.isVisible():
            return
        self.ui.SshArea.hide()
        self.setFixedSize(self.width(), self.height() - self.ui.SshArea.height())

    def onSshButtonClicked(self) -> None:
        if self.ui.SshArea.isVisible():
            return
        self.setFixedSize(self.width(), self.height() + self.ui.SshArea.height())
        self.ui.SshArea.show()

    def onDirectoryButtonClicked(self) -> None:
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择目录",
            "",
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks,
        )
        if not directory:
            return
        self.ui.RootPath.setText(directory)

    def onAcceptButtonClicked(self) -> None:
        self.close()

    def showEvent(self, event: QShowEvent) -> None:
        if not self.buttonGroup.checkedButton():
            self.ui.LocalButton.click()
        return super().showEvent(event)
