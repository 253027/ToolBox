# Copyright (C) 2026 mogaitesheng
# SPDX-License-Identifier: LGPL-3.0-or-later
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QFrame,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import (
    BreadcrumbBar,
    CaptionLabel,
    CheckBox,
    FluentIcon,
    LineEdit,
    PrimaryPushButton,
    ProgressBar,
    TableWidget,
    TransparentPushButton,
    TransparentToolButton,
)


class Ui_LibReplaceContent(object):
    def setupUi(self, LibReplaceContent):
        if not LibReplaceContent.objectName():
            LibReplaceContent.setObjectName("LibReplaceContent")

        # the layout of LibReplaceContent
        self.LibReplaceContentLayout = QVBoxLayout(LibReplaceContent)
        self.LibReplaceContentLayout.setContentsMargins(0, 0, 0, 0)
        self.LibReplaceContentLayout.setSpacing(0)

        self._buildHeaerFrame(LibReplaceContent)
        self._buildSeparator_1(LibReplaceContent)
        self._buildAddFileFrame(LibReplaceContent)
        self._buildFileTable(LibReplaceContent)
        self._buildSeparator_2(LibReplaceContent)
        self._buildBottomBar(LibReplaceContent)

    def _buildHeaerFrame(self, parent: QWidget | None) -> None:
        self.headerFrame = QFrame(parent)
        self.headerFrame.setFixedHeight(60)
        headerFrameSizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        headerFrameSizePolicy.setHorizontalStretch(0)
        headerFrameSizePolicy.setVerticalStretch(0)
        headerFrameSizePolicy.setHeightForWidth(
            self.headerFrame.sizePolicy().hasHeightForWidth()
        )
        self.headerFrame.setSizePolicy(headerFrameSizePolicy)
        self.headerFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.headerFrame.setLineWidth(0)
        self.headLayout = QHBoxLayout(self.headerFrame)
        self.headLayout.setContentsMargins(10, 0, 15, 0)

        self.breadcrumbBar = BreadcrumbBar(parent)

        self.exportButton = TransparentPushButton(FluentIcon.SHARE, "导出清单", parent)
        self.exportButton.setEnabled(False)
        self.exportButton.setFixedSize(106, 60)

        self.headLayout.addWidget(self.breadcrumbBar, Qt.AlignmentFlag.AlignLeft)
        self.headLayout.addWidget(self.exportButton, Qt.AlignmentFlag.AlignRight)
        self.LibReplaceContentLayout.addWidget(self.headerFrame)

    def _buildSeparator_1(self, parent: QWidget | None) -> None:
        self.headFileLine = QFrame(parent)
        self.headFileLine.setObjectName("headFileLine")
        self.headFileLine.setFixedHeight(1)
        self.LibReplaceContentLayout.addWidget(self.headFileLine)

    def _buildAddFileFrame(self, parent: QWidget | None) -> None:
        self.addFileFrame = QFrame(parent)
        self.addFileFrame.setFixedHeight(60)
        self.addFileFrame.setObjectName("AddFileFrame")
        self.addFileLayout = QHBoxLayout(self.addFileFrame)
        self.addFileLayout.setContentsMargins(10, 10, 15, 10)
        self.addFileLayout.setSpacing(8)

        self.fileInput = LineEdit(parent)
        self.fileInput.setPlaceholderText("输入新的文件名（例如：core_module_v1.js）")
        self.fileInput.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        self.browseButton = TransparentToolButton(FluentIcon.FOLDER, parent)
        self.browseButton.setFixedSize(34, 34)
        self.browseButton.setToolTip("选择本地文件")

        self.addButton = PrimaryPushButton("+ 添加文件", parent)
        self.addButton.setFixedWidth(110)

        self.addFileLayout.addWidget(self.fileInput)
        self.addFileLayout.addWidget(self.browseButton)
        self.addFileLayout.addWidget(self.addButton)
        self.LibReplaceContentLayout.addWidget(self.addFileFrame)

    def _buildFileTable(self, parent: QWidget | None) -> None:
        self.fileTableFrame = QFrame(parent)
        self.fileTableFrame.setObjectName("FileTableFrame")
        self.fileTableFrameLayout = QVBoxLayout(self.fileTableFrame)
        self.fileTableFrameLayout.setContentsMargins(10, 0, 10, 0)
        self.fileTableFrameLayout.setSpacing(0)

        self.fileTable = TableWidget(self.fileTableFrame)
        self.fileTable.setObjectName("FileTable")
        self.fileTable.setColumnCount(5)
        self.fileTable.setHorizontalHeaderLabels(["", "文件名", "状态", "模块", ""])
        self.fileTable.verticalHeader().setVisible(False)
        self.fileTable.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.fileTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.fileTable.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.fileTable.setShowGrid(False)
        self.fileTable.setAlternatingRowColors(False)
        self.fileTable.setFrameShape(QFrame.Shape.NoFrame)
        self.fileTable.setColumnWidth(0, 36)
        self.fileTable.setColumnWidth(2, 80)
        self.fileTable.setColumnWidth(3, 150)
        self.fileTable.setColumnWidth(4, 36)

        header = self.fileTable.horizontalHeader()
        header.setFixedHeight(30)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setDefaultAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter
        )

        self._headerWidgets: dict[int, QWidget] = {}
        header.sectionResized.connect(self._repositionAllHeaderWidgets)
        header.geometriesChanged.connect(self._repositionAllHeaderWidgets)

        # Default: place a CheckBox in column 0
        self.selectAllBox = QCheckBox(parent)
        self.selectAllBox.setFixedSize(16, 16)
        self.setHeaderWidget(0, self.selectAllBox)

        self.fileTableFrameLayout.addWidget(self.fileTable)
        self.LibReplaceContentLayout.addWidget(self.fileTableFrame, stretch=1)

    # ------------------------------------------------------------------ #
    #  Public header-widget API                                            #
    # ------------------------------------------------------------------ #

    def setHeaderWidget(self, col: int, widget: QWidget) -> None:
        """Place any widget centered inside the header of the given column."""
        header = self.fileTable.horizontalHeader()
        old = self._headerWidgets.get(col)
        if old is not None and old is not widget:
            old.deleteLater()
        widget.setParent(header)
        self._headerWidgets[col] = widget
        self._repositionHeaderWidget(col)
        widget.show()

    # ------------------------------------------------------------------ #
    #  Internal repositioning                                              #
    # ------------------------------------------------------------------ #

    def _repositionHeaderWidget(self, col: int) -> None:
        widget = self._headerWidgets.get(col)
        if widget is None:
            return
        header = self.fileTable.horizontalHeader()
        x_offset = sum(header.sectionSize(i) for i in range(col))
        col_w = header.sectionSize(col)
        h = header.height()
        size = widget.size()
        x = x_offset + (col_w - size.width()) // 2
        y = (h - size.height()) // 2
        widget.move(x, y)

    def _repositionAllHeaderWidgets(self) -> None:
        for col in self._headerWidgets:
            self._repositionHeaderWidget(col)

    def _buildSeparator_2(self, parent: QWidget | None) -> None:
        self.fileBottomLine = QFrame(parent)
        self.fileBottomLine.setObjectName("fileBottomLine")
        self.fileBottomLine.setFixedHeight(1)
        self.LibReplaceContentLayout.addWidget(self.fileBottomLine)

    def _buildBottomBar(self, parent: QWidget | None) -> None:
        self.bottomBar = QFrame(parent)
        self.bottomBar.setFixedHeight(54)
        self.bottomBar.setObjectName("BottomBar")
        self.bottomBarLayout = QHBoxLayout(self.bottomBar)
        self.bottomBarLayout.setContentsMargins(16, 0, 16, 0)
        self.bottomBarLayout.setSpacing(12)

        self.progressBar = ProgressBar(parent)
        self.progressBar.setFixedWidth(160)
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)

        self.progressLabel = CaptionLabel("", parent)
        self.progressLabel.setVisible(False)

        self.selectionLabel = CaptionLabel("", parent)

        self.executeButton = PrimaryPushButton("▶  立刻执行编译", parent)
        self.executeButton.setEnabled(False)

        self.envDot = QLabel("●", parent)
        self.envDot.setObjectName("envDot")
        self.envDot.setProperty("envState", "idle")
        self.envLabel = CaptionLabel("未选择工程", parent)

        self.bottomBarLayout.addWidget(self.progressBar)
        self.bottomBarLayout.addWidget(self.progressLabel)
        self.bottomBarLayout.addStretch()
        self.bottomBarLayout.addWidget(self.selectionLabel)
        self.bottomBarLayout.addWidget(self.executeButton)
        self.bottomBarLayout.addStretch()
        self.bottomBarLayout.addWidget(self.envDot)
        self.bottomBarLayout.addWidget(self.envLabel)
        self.LibReplaceContentLayout.addWidget(self.bottomBar)
