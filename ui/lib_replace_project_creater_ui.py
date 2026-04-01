# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lib_replace_project_creater.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QRadioButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (LineEdit, PrimaryPushButton, PrimaryPushButton , PushButton)
import resource_rc

class Ui_ProjectCreater(object):
    def setupUi(self, ProjectCreater):
        if not ProjectCreater.objectName():
            ProjectCreater.setObjectName(u"ProjectCreater")
        ProjectCreater.resize(403, 385)
        self.ProjectCreaterLayout = QVBoxLayout(ProjectCreater)
        self.ProjectCreaterLayout.setSpacing(0)
        self.ProjectCreaterLayout.setObjectName(u"ProjectCreaterLayout")
        self.ProjectCreaterLayout.setContentsMargins(0, 38, 0, 0)
        self.ContentArea = QFrame(ProjectCreater)
        self.ContentArea.setObjectName(u"ContentArea")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ContentArea.sizePolicy().hasHeightForWidth())
        self.ContentArea.setSizePolicy(sizePolicy)
        self.ContentArea.setMinimumSize(QSize(0, 152))
        self.ContentArea.setMaximumSize(QSize(16777215, 152))
        self.ContentArea.setFrameShape(QFrame.Shape.NoFrame)
        self.ContentArea.setFrameShadow(QFrame.Shadow.Raised)
        self.ContentAreaLayout = QVBoxLayout(self.ContentArea)
        self.ContentAreaLayout.setSpacing(0)
        self.ContentAreaLayout.setObjectName(u"ContentAreaLayout")
        self.ContentAreaLayout.setContentsMargins(15, 6, 15, 0)
        self.RootDirectoryFrame = QFrame(self.ContentArea)
        self.RootDirectoryFrame.setObjectName(u"RootDirectoryFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.RootDirectoryFrame.sizePolicy().hasHeightForWidth())
        self.RootDirectoryFrame.setSizePolicy(sizePolicy1)
        self.RootDirectoryFrame.setMinimumSize(QSize(0, 40))
        self.RootDirectoryFrame.setMaximumSize(QSize(16777215, 40))
        self.RootDirectoryFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.RootDirectoryFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.RootDirectoryLayout = QHBoxLayout(self.RootDirectoryFrame)
        self.RootDirectoryLayout.setSpacing(10)
        self.RootDirectoryLayout.setObjectName(u"RootDirectoryLayout")
        self.RootDirectoryLayout.setContentsMargins(-1, 0, -1, 0)
        self.RootTitle = QLabel(self.RootDirectoryFrame)
        self.RootTitle.setObjectName(u"RootTitle")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(True)
        self.RootTitle.setFont(font)

        self.RootDirectoryLayout.addWidget(self.RootTitle)

        self.RootPath = LineEdit(self.RootDirectoryFrame)
        self.RootPath.setObjectName(u"RootPath")
        self.RootPath.setMinimumSize(QSize(0, 28))
        self.RootPath.setMaximumSize(QSize(16777215, 28))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(10)
        self.RootPath.setFont(font1)

        self.RootDirectoryLayout.addWidget(self.RootPath)

        self.DirectoryButton = PrimaryPushButton (self.RootDirectoryFrame)
        self.DirectoryButton.setObjectName(u"DirectoryButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.DirectoryButton.sizePolicy().hasHeightForWidth())
        self.DirectoryButton.setSizePolicy(sizePolicy2)
        self.DirectoryButton.setMinimumSize(QSize(50, 28))
        self.DirectoryButton.setMaximumSize(QSize(50, 28))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        self.DirectoryButton.setFont(font2)

        self.RootDirectoryLayout.addWidget(self.DirectoryButton)


        self.ContentAreaLayout.addWidget(self.RootDirectoryFrame)

        self.RootProjectNameLine = QFrame(self.ContentArea)
        self.RootProjectNameLine.setObjectName(u"RootProjectNameLine")
        self.RootProjectNameLine.setMinimumSize(QSize(0, 3))
        self.RootProjectNameLine.setMaximumSize(QSize(16777215, 3))
        self.RootProjectNameLine.setFrameShadow(QFrame.Shadow.Raised)
        self.RootProjectNameLine.setLineWidth(1)
        self.RootProjectNameLine.setMidLineWidth(0)
        self.RootProjectNameLine.setFrameShape(QFrame.Shape.HLine)

        self.ContentAreaLayout.addWidget(self.RootProjectNameLine)

        self.ProjectNameFrame = QFrame(self.ContentArea)
        self.ProjectNameFrame.setObjectName(u"ProjectNameFrame")
        sizePolicy1.setHeightForWidth(self.ProjectNameFrame.sizePolicy().hasHeightForWidth())
        self.ProjectNameFrame.setSizePolicy(sizePolicy1)
        self.ProjectNameFrame.setMinimumSize(QSize(0, 40))
        self.ProjectNameFrame.setMaximumSize(QSize(16777215, 40))
        self.ProjectNameFrame.setFont(font2)
        self.ProjectNameFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.ProjectNameFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.ProjectNameLayout = QHBoxLayout(self.ProjectNameFrame)
        self.ProjectNameLayout.setSpacing(37)
        self.ProjectNameLayout.setObjectName(u"ProjectNameLayout")
        self.ProjectNameLayout.setContentsMargins(9, 0, 70, 0)
        self.ProjectName = QLabel(self.ProjectNameFrame)
        self.ProjectName.setObjectName(u"ProjectName")
        self.ProjectName.setFont(font)

        self.ProjectNameLayout.addWidget(self.ProjectName)

        self.ProjectNameInput = LineEdit(self.ProjectNameFrame)
        self.ProjectNameInput.setObjectName(u"ProjectNameInput")
        self.ProjectNameInput.setMinimumSize(QSize(0, 28))
        self.ProjectNameInput.setMaximumSize(QSize(16777215, 28))
        self.ProjectNameInput.setFont(font1)

        self.ProjectNameLayout.addWidget(self.ProjectNameInput)


        self.ContentAreaLayout.addWidget(self.ProjectNameFrame)

        self.ProjectRemoteLine = QFrame(self.ContentArea)
        self.ProjectRemoteLine.setObjectName(u"ProjectRemoteLine")
        self.ProjectRemoteLine.setMinimumSize(QSize(0, 3))
        self.ProjectRemoteLine.setMaximumSize(QSize(16777215, 3))
        self.ProjectRemoteLine.setFrameShadow(QFrame.Shadow.Raised)
        self.ProjectRemoteLine.setFrameShape(QFrame.Shape.HLine)

        self.ContentAreaLayout.addWidget(self.ProjectRemoteLine)

        self.RemoteDirectoryArea = QFrame(self.ContentArea)
        self.RemoteDirectoryArea.setObjectName(u"RemoteDirectoryArea")
        sizePolicy1.setHeightForWidth(self.RemoteDirectoryArea.sizePolicy().hasHeightForWidth())
        self.RemoteDirectoryArea.setSizePolicy(sizePolicy1)
        self.RemoteDirectoryArea.setMinimumSize(QSize(0, 60))
        self.RemoteDirectoryArea.setMaximumSize(QSize(16777215, 60))
        self.RemoteDirectoryArea.setFrameShape(QFrame.Shape.NoFrame)
        self.RemoteDirectoryArea.setFrameShadow(QFrame.Shadow.Raised)
        self.RemoteDirectoryAreaLayout = QVBoxLayout(self.RemoteDirectoryArea)
        self.RemoteDirectoryAreaLayout.setSpacing(4)
        self.RemoteDirectoryAreaLayout.setObjectName(u"RemoteDirectoryAreaLayout")
        self.RemoteDirectoryAreaLayout.setContentsMargins(0, 4, 0, 0)
        self.RemoteDirectory = QWidget(self.RemoteDirectoryArea)
        self.RemoteDirectory.setObjectName(u"RemoteDirectory")
        self.RemoteDirectoryLayout = QHBoxLayout(self.RemoteDirectory)
        self.RemoteDirectoryLayout.setSpacing(23)
        self.RemoteDirectoryLayout.setObjectName(u"RemoteDirectoryLayout")
        self.RemoteDirectoryLayout.setContentsMargins(9, 0, 70, 0)
        self.RemoteName = QLabel(self.RemoteDirectory)
        self.RemoteName.setObjectName(u"RemoteName")
        self.RemoteName.setFont(font)

        self.RemoteDirectoryLayout.addWidget(self.RemoteName)

        self.RemoteInput = LineEdit(self.RemoteDirectory)
        self.RemoteInput.setObjectName(u"RemoteInput")
        self.RemoteInput.setMinimumSize(QSize(0, 28))
        self.RemoteInput.setMaximumSize(QSize(16777215, 28))
        self.RemoteInput.setFont(font1)

        self.RemoteDirectoryLayout.addWidget(self.RemoteInput)


        self.RemoteDirectoryAreaLayout.addWidget(self.RemoteDirectory)

        self.RemoteChoice = QWidget(self.RemoteDirectoryArea)
        self.RemoteChoice.setObjectName(u"RemoteChoice")
        self.horizontalLayout_2 = QHBoxLayout(self.RemoteChoice)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.RemoteLeftSpacer = QSpacerItem(94, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.RemoteLeftSpacer)

        self.LocalButton = QRadioButton(self.RemoteChoice)
        self.LocalButton.setObjectName(u"LocalButton")
        self.LocalButton.setFont(font2)
        self.LocalButton.setIconSize(QSize(0, 0))

        self.horizontalLayout_2.addWidget(self.LocalButton)

        self.SshButton = QRadioButton(self.RemoteChoice)
        self.SshButton.setObjectName(u"SshButton")
        self.SshButton.setFont(font2)
        self.SshButton.setIconSize(QSize(0, 0))

        self.horizontalLayout_2.addWidget(self.SshButton)

        self.RemoteRightSpacer = QSpacerItem(94, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.RemoteRightSpacer)


        self.RemoteDirectoryAreaLayout.addWidget(self.RemoteChoice)


        self.ContentAreaLayout.addWidget(self.RemoteDirectoryArea)


        self.ProjectCreaterLayout.addWidget(self.ContentArea)

        self.SshArea = QFrame(ProjectCreater)
        self.SshArea.setObjectName(u"SshArea")
        self.SshArea.setMinimumSize(QSize(0, 135))
        self.SshArea.setMaximumSize(QSize(16777215, 135))
        self.SshArea.setFrameShape(QFrame.Shape.NoFrame)
        self.SshArea.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.SshArea)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(20, 2, 20, 0)
        self.SshContent = QFrame(self.SshArea)
        self.SshContent.setObjectName(u"SshContent")
        self.SshContent.setMinimumSize(QSize(0, 100))
        self.SshContent.setMaximumSize(QSize(16777215, 100))
        self.SshContent.setFrameShape(QFrame.Shape.NoFrame)
        self.SshContent.setFrameShadow(QFrame.Shadow.Raised)
        self.SshContentLayout = QGridLayout(self.SshContent)
        self.SshContentLayout.setSpacing(0)
        self.SshContentLayout.setObjectName(u"SshContentLayout")
        self.SshContentLayout.setContentsMargins(8, 6, 8, 6)
        self.HostFrame = QFrame(self.SshContent)
        self.HostFrame.setObjectName(u"HostFrame")
        self.HostFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.HostFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.HostLayout = QHBoxLayout(self.HostFrame)
        self.HostLayout.setSpacing(15)
        self.HostLayout.setObjectName(u"HostLayout")
        self.HostLayout.setContentsMargins(0, 0, 4, 4)
        self.HostLabel = QLabel(self.HostFrame)
        self.HostLabel.setObjectName(u"HostLabel")
        self.HostLabel.setFont(font2)

        self.HostLayout.addWidget(self.HostLabel)

        self.HostInput = LineEdit(self.HostFrame)
        self.HostInput.setObjectName(u"HostInput")
        self.HostInput.setMinimumSize(QSize(0, 28))
        self.HostInput.setMaximumSize(QSize(16777215, 28))
        self.HostInput.setFont(font2)

        self.HostLayout.addWidget(self.HostInput)


        self.SshContentLayout.addWidget(self.HostFrame, 0, 0, 1, 1)

        self.PortFrame = QFrame(self.SshContent)
        self.PortFrame.setObjectName(u"PortFrame")
        self.PortFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.PortFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.PortLayout = QHBoxLayout(self.PortFrame)
        self.PortLayout.setSpacing(4)
        self.PortLayout.setObjectName(u"PortLayout")
        self.PortLayout.setContentsMargins(4, 0, 0, 4)
        self.PortLabel = QLabel(self.PortFrame)
        self.PortLabel.setObjectName(u"PortLabel")
        self.PortLabel.setFont(font2)

        self.PortLayout.addWidget(self.PortLabel)

        self.PortInput = LineEdit(self.PortFrame)
        self.PortInput.setObjectName(u"PortInput")
        self.PortInput.setMinimumSize(QSize(0, 28))
        self.PortInput.setMaximumSize(QSize(16777215, 28))
        self.PortInput.setFont(font2)

        self.PortLayout.addWidget(self.PortInput)


        self.SshContentLayout.addWidget(self.PortFrame, 0, 1, 1, 1)

        self.UserNameFrame = QFrame(self.SshContent)
        self.UserNameFrame.setObjectName(u"UserNameFrame")
        self.UserNameFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.UserNameFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.UserNameFrame)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.UserNameLabel = QLabel(self.UserNameFrame)
        self.UserNameLabel.setObjectName(u"UserNameLabel")
        self.UserNameLabel.setFont(font2)

        self.horizontalLayout_3.addWidget(self.UserNameLabel)

        self.UserNameInput = LineEdit(self.UserNameFrame)
        self.UserNameInput.setObjectName(u"UserNameInput")
        self.UserNameInput.setMinimumSize(QSize(0, 28))
        self.UserNameInput.setMaximumSize(QSize(16777215, 28))
        self.UserNameInput.setFont(font2)

        self.horizontalLayout_3.addWidget(self.UserNameInput)


        self.SshContentLayout.addWidget(self.UserNameFrame, 1, 0, 1, 2)

        self.PasswordFrame = QFrame(self.SshContent)
        self.PasswordFrame.setObjectName(u"PasswordFrame")
        self.PasswordFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.PasswordFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.PasswordFrame)
        self.horizontalLayout_4.setSpacing(15)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.PasswordLabel = QLabel(self.PasswordFrame)
        self.PasswordLabel.setObjectName(u"PasswordLabel")
        self.PasswordLabel.setFont(font2)

        self.horizontalLayout_4.addWidget(self.PasswordLabel)

        self.PasswordInput = LineEdit(self.PasswordFrame)
        self.PasswordInput.setObjectName(u"PasswordInput")
        self.PasswordInput.setMinimumSize(QSize(0, 28))
        self.PasswordInput.setMaximumSize(QSize(16777215, 28))
        self.PasswordInput.setFont(font2)
        self.PasswordInput.setEchoMode(QLineEdit.EchoMode.Password)

        self.horizontalLayout_4.addWidget(self.PasswordInput)


        self.SshContentLayout.addWidget(self.PasswordFrame, 2, 0, 1, 2)

        self.SshContentLayout.setColumnStretch(0, 3)

        self.gridLayout.addWidget(self.SshContent, 0, 0, 1, 1)

        self.SshVerify = QFrame(self.SshArea)
        self.SshVerify.setObjectName(u"SshVerify")
        self.SshVerify.setMinimumSize(QSize(0, 35))
        self.SshVerify.setMaximumSize(QSize(16777215, 35))
        self.SshVerify.setFrameShape(QFrame.Shape.NoFrame)
        self.SshVerify.setFrameShadow(QFrame.Shadow.Raised)
        self.SshVerifyLayout = QHBoxLayout(self.SshVerify)
        self.SshVerifyLayout.setSpacing(0)
        self.SshVerifyLayout.setObjectName(u"SshVerifyLayout")
        self.SshVerifyLayout.setContentsMargins(0, 6, 0, 0)
        self.VerifyButton = PrimaryPushButton(self.SshVerify)
        self.VerifyButton.setObjectName(u"VerifyButton")
        self.VerifyButton.setFont(font2)

        self.SshVerifyLayout.addWidget(self.VerifyButton)


        self.gridLayout.addWidget(self.SshVerify, 1, 0, 1, 1)


        self.ProjectCreaterLayout.addWidget(self.SshArea)

        self.ButtonArea = QFrame(ProjectCreater)
        self.ButtonArea.setObjectName(u"ButtonArea")
        sizePolicy1.setHeightForWidth(self.ButtonArea.sizePolicy().hasHeightForWidth())
        self.ButtonArea.setSizePolicy(sizePolicy1)
        self.ButtonArea.setMinimumSize(QSize(0, 60))
        self.ButtonArea.setMaximumSize(QSize(16777215, 60))
        self.ButtonArea.setFrameShape(QFrame.Shape.NoFrame)
        self.ButtonArea.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.ButtonArea)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, 0, 20, 0)
        self.AcceptButton = PushButton(self.ButtonArea)
        self.AcceptButton.setObjectName(u"AcceptButton")
        self.AcceptButton.setMinimumSize(QSize(0, 35))
        self.AcceptButton.setMaximumSize(QSize(16777215, 35))
        self.AcceptButton.setFont(font2)

        self.horizontalLayout.addWidget(self.AcceptButton)

        self.CloseButton = PushButton(self.ButtonArea)
        self.CloseButton.setObjectName(u"CloseButton")
        self.CloseButton.setMinimumSize(QSize(0, 35))
        self.CloseButton.setMaximumSize(QSize(16777215, 35))
        self.CloseButton.setFont(font2)

        self.horizontalLayout.addWidget(self.CloseButton)


        self.ProjectCreaterLayout.addWidget(self.ButtonArea)


        self.retranslateUi(ProjectCreater)

        QMetaObject.connectSlotsByName(ProjectCreater)
    # setupUi

    def retranslateUi(self, ProjectCreater):
        ProjectCreater.setWindowTitle(QCoreApplication.translate("ProjectCreater", u"Dialog", None))
        self.RootTitle.setText(QCoreApplication.translate("ProjectCreater", u"\u6839\u76ee\u5f55\u8def\u5f84", None))
        self.DirectoryButton.setText(QCoreApplication.translate("ProjectCreater", u"\u6d4f\u89c8", None))
        self.ProjectName.setText(QCoreApplication.translate("ProjectCreater", u"\u5de5\u7a0b\u540d", None))
        self.RemoteName.setText(QCoreApplication.translate("ProjectCreater", u"\u7f16\u8bd1\u76ee\u5f55", None))
        self.LocalButton.setText(QCoreApplication.translate("ProjectCreater", u"\u672c\u5730\u76ee\u5f55", None))
        self.SshButton.setText(QCoreApplication.translate("ProjectCreater", u"SSH\u76ee\u5f55", None))
        self.HostLabel.setText(QCoreApplication.translate("ProjectCreater", u"\u4e3b\u673a", None))
        self.PortLabel.setText(QCoreApplication.translate("ProjectCreater", u"\u7aef\u53e3", None))
        self.UserNameLabel.setText(QCoreApplication.translate("ProjectCreater", u"\u7528\u6237\u540d", None))
        self.PasswordLabel.setText(QCoreApplication.translate("ProjectCreater", u"\u5bc6\u7801", None))
        self.VerifyButton.setText(QCoreApplication.translate("ProjectCreater", u"\u9a8c\u8bc1", None))
        self.AcceptButton.setText(QCoreApplication.translate("ProjectCreater", u"\u786e\u8ba4", None))
        self.CloseButton.setText(QCoreApplication.translate("ProjectCreater", u"\u53d6\u6d88", None))
    # retranslateUi

