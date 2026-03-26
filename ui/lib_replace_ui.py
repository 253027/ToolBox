# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lib_replace.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

from qfluentwidgets import (ScrollArea, SearchLineEdit)
from ui import DropDownIconButton

class Ui_LibReplace(object):
    def setupUi(self, LibReplace):
        if not LibReplace.objectName():
            LibReplace.setObjectName(u"LibReplace")
        LibReplace.resize(614, 463)
        LibReplace.setAutoFillBackground(False)
        self.LibPeplaceLayout = QHBoxLayout(LibReplace)
        self.LibPeplaceLayout.setSpacing(0)
        self.LibPeplaceLayout.setObjectName(u"LibPeplaceLayout")
        self.LibPeplaceLayout.setContentsMargins(0, 0, 0, 0)
        self.LeftSideBarWidget = QWidget(LibReplace)
        self.LeftSideBarWidget.setObjectName(u"LeftSideBarWidget")
        self.LeftSideBarWidget.setStyleSheet(u"")
        self.LeftSideBarLayout = QVBoxLayout(self.LeftSideBarWidget)
        self.LeftSideBarLayout.setSpacing(0)
        self.LeftSideBarLayout.setObjectName(u"LeftSideBarLayout")
        self.LeftSideBarLayout.setContentsMargins(0, 0, 0, 0)
        self.SearchFrame = QFrame(self.LeftSideBarWidget)
        self.SearchFrame.setObjectName(u"SearchFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearchFrame.sizePolicy().hasHeightForWidth())
        self.SearchFrame.setSizePolicy(sizePolicy)
        self.SearchFrame.setMinimumSize(QSize(0, 40))
        self.SearchFrame.setMaximumSize(QSize(16777215, 40))
        self.SearchFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.SearchFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.SearchLayout = QGridLayout(self.SearchFrame)
        self.SearchLayout.setSpacing(0)
        self.SearchLayout.setObjectName(u"SearchLayout")
        self.SearchLayout.setContentsMargins(10, 7, 10, 0)
        self.SearchEdit = SearchLineEdit(self.SearchFrame)
        self.SearchEdit.setObjectName(u"SearchEdit")
        self.SearchEdit.setMinimumSize(QSize(0, 33))
        self.SearchEdit.setMaximumSize(QSize(16777215, 33))

        self.SearchLayout.addWidget(self.SearchEdit, 0, 0, 1, 1)


        self.LeftSideBarLayout.addWidget(self.SearchFrame)

        self.ProjectsHeaderFrame = QFrame(self.LeftSideBarWidget)
        self.ProjectsHeaderFrame.setObjectName(u"ProjectsHeaderFrame")
        sizePolicy.setHeightForWidth(self.ProjectsHeaderFrame.sizePolicy().hasHeightForWidth())
        self.ProjectsHeaderFrame.setSizePolicy(sizePolicy)
        self.ProjectsHeaderFrame.setMinimumSize(QSize(0, 35))
        self.ProjectsHeaderFrame.setMaximumSize(QSize(16777215, 35))
        self.ProjectsHeaderFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.ProjectsHeaderFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.ProjectsHeaderFrame.setLineWidth(0)
        self.ProjectsHeaderLayout = QHBoxLayout(self.ProjectsHeaderFrame)
        self.ProjectsHeaderLayout.setObjectName(u"ProjectsHeaderLayout")
        self.ProjectsHeaderLayout.setContentsMargins(22, 0, 20, 0)
        self.ProjectsTitle = QLabel(self.ProjectsHeaderFrame)
        self.ProjectsTitle.setObjectName(u"ProjectsTitle")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(11)
        self.ProjectsTitle.setFont(font)

        self.ProjectsHeaderLayout.addWidget(self.ProjectsTitle)

        self.ProjectsHeaderButton = DropDownIconButton(self.ProjectsHeaderFrame)
        self.ProjectsHeaderButton.setObjectName(u"ProjectsHeaderButton")
        self.ProjectsHeaderButton.setMinimumSize(QSize(18, 18))
        self.ProjectsHeaderButton.setMaximumSize(QSize(18, 18))

        self.ProjectsHeaderLayout.addWidget(self.ProjectsHeaderButton)


        self.LeftSideBarLayout.addWidget(self.ProjectsHeaderFrame)

        self.ScrollAreaFrame = QFrame(self.LeftSideBarWidget)
        self.ScrollAreaFrame.setObjectName(u"ScrollAreaFrame")
        self.ScrollAreaFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.ScrollAreaFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.ScrollAreaFrame.setLineWidth(0)
        self.ScrollAreaLayout = QVBoxLayout(self.ScrollAreaFrame)
        self.ScrollAreaLayout.setSpacing(0)
        self.ScrollAreaLayout.setObjectName(u"ScrollAreaLayout")
        self.ScrollAreaLayout.setContentsMargins(0, 0, 0, 0)
        self.ScrollArea = ScrollArea(self.ScrollAreaFrame)
        self.ScrollArea.setObjectName(u"ScrollArea")
        self.ScrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.ScrollArea.setLineWidth(0)
        self.ScrollArea.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.ScrollArea.setWidgetResizable(False)
        self.ScrollArea.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ScrollAreaWidgetContents = QWidget()
        self.ScrollAreaWidgetContents.setObjectName(u"ScrollAreaWidgetContents")
        self.ScrollAreaWidgetContents.setGeometry(QRect(0, 0, 170, 388))
        self.ScrollAreaWidgetContentsLayout = QVBoxLayout(self.ScrollAreaWidgetContents)
        self.ScrollAreaWidgetContentsLayout.setSpacing(10)
        self.ScrollAreaWidgetContentsLayout.setObjectName(u"ScrollAreaWidgetContentsLayout")
        self.ScrollAreaWidgetContentsLayout.setContentsMargins(0, 0, 0, 0)
        self.ScrollArea.setWidget(self.ScrollAreaWidgetContents)

        self.ScrollAreaLayout.addWidget(self.ScrollArea)


        self.LeftSideBarLayout.addWidget(self.ScrollAreaFrame)


        self.LibPeplaceLayout.addWidget(self.LeftSideBarWidget)

        self.MainContentWidget = QWidget(LibReplace)
        self.MainContentWidget.setObjectName(u"MainContentWidget")

        self.LibPeplaceLayout.addWidget(self.MainContentWidget)

        self.LibPeplaceLayout.setStretch(0, 75)
        self.LibPeplaceLayout.setStretch(1, 196)

        self.retranslateUi(LibReplace)

        QMetaObject.connectSlotsByName(LibReplace)
    # setupUi

    def retranslateUi(self, LibReplace):
        LibReplace.setWindowTitle(QCoreApplication.translate("LibReplace", u"LibReplacer", None))
        self.ProjectsTitle.setText(QCoreApplication.translate("LibReplace", u"\u5de5\u7a0b\u5217\u8868", None))
        self.ProjectsHeaderButton.setText("")
    # retranslateUi

