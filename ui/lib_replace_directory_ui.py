# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lib_replace_directory.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

from qfluentwidgets import IconWidget

class Ui_LibReplaceDirectory(object):
    def setupUi(self, LibReplaceDirectory):
        if not LibReplaceDirectory.objectName():
            LibReplaceDirectory.setObjectName(u"LibReplaceDirectory")
        LibReplaceDirectory.resize(228, 70)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LibReplaceDirectory.sizePolicy().hasHeightForWidth())
        LibReplaceDirectory.setSizePolicy(sizePolicy)
        LibReplaceDirectory.setMinimumSize(QSize(0, 70))
        LibReplaceDirectory.setMaximumSize(QSize(16777215, 70))
        LibReplaceDirectory.setAutoFillBackground(False)
        self.LibReplaceDirectoryLayout = QGridLayout(LibReplaceDirectory)
        self.LibReplaceDirectoryLayout.setSpacing(0)
        self.LibReplaceDirectoryLayout.setObjectName(u"LibReplaceDirectoryLayout")
        self.LibReplaceDirectoryLayout.setContentsMargins(0, 0, 0, 0)
        self.Content = QWidget(LibReplaceDirectory)
        self.Content.setObjectName(u"Content")
        self.ContentLayout = QHBoxLayout(self.Content)
        self.ContentLayout.setSpacing(0)
        self.ContentLayout.setObjectName(u"ContentLayout")
        self.ContentLayout.setContentsMargins(0, 0, 0, 0)
        self.IconFrame = QFrame(self.Content)
        self.IconFrame.setObjectName(u"IconFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.IconFrame.sizePolicy().hasHeightForWidth())
        self.IconFrame.setSizePolicy(sizePolicy1)
        self.IconFrame.setMinimumSize(QSize(40, 0))
        self.IconFrame.setMaximumSize(QSize(40, 16777215))
        self.IconFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.IconFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.IconFrameLayout = QGridLayout(self.IconFrame)
        self.IconFrameLayout.setSpacing(0)
        self.IconFrameLayout.setObjectName(u"IconFrameLayout")
        self.IconFrameLayout.setContentsMargins(11, 24, 5, 24)
        self.IconWidget = IconWidget(self.IconFrame)
        self.IconWidget.setObjectName(u"IconWidget")

        self.IconFrameLayout.addWidget(self.IconWidget, 0, 0, 1, 1)


        self.ContentLayout.addWidget(self.IconFrame)

        self.DirectoryComponentFrame = QFrame(self.Content)
        self.DirectoryComponentFrame.setObjectName(u"DirectoryComponentFrame")
        self.DirectoryComponentFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.DirectoryComponentFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.DirectoryComponentLayout = QVBoxLayout(self.DirectoryComponentFrame)
        self.DirectoryComponentLayout.setSpacing(0)
        self.DirectoryComponentLayout.setObjectName(u"DirectoryComponentLayout")
        self.DirectoryComponentLayout.setContentsMargins(0, 14, -1, 14)
        self.Directory = QLabel(self.DirectoryComponentFrame)
        self.Directory.setObjectName(u"Directory")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        self.Directory.setFont(font)
        self.Directory.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.DirectoryComponentLayout.addWidget(self.Directory)

        self.Date = QLabel(self.DirectoryComponentFrame)
        self.Date.setObjectName(u"Date")
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(8)
        self.Date.setFont(font1)
        self.Date.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.DirectoryComponentLayout.addWidget(self.Date)


        self.ContentLayout.addWidget(self.DirectoryComponentFrame)


        self.LibReplaceDirectoryLayout.addWidget(self.Content, 0, 0, 1, 1)


        self.retranslateUi(LibReplaceDirectory)

        QMetaObject.connectSlotsByName(LibReplaceDirectory)
    # setupUi

    def retranslateUi(self, LibReplaceDirectory):
        LibReplaceDirectory.setWindowTitle(QCoreApplication.translate("LibReplaceDirectory", u"LibReplacer", None))
        self.Directory.setText("")
        self.Date.setText("")
    # retranslateUi

