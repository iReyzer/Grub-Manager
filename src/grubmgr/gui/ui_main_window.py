from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QSize,
    Qt,
)
from PySide6.QtGui import (
    QCursor,
)
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QTabWidget,
    QWidget,
)


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 900)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.logText = QPlainTextEdit(self.centralwidget)
        self.logText.setObjectName("logText")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logText.sizePolicy().hasHeightForWidth())
        self.logText.setSizePolicy(sizePolicy)
        self.logText.setReadOnly(True)

        self.gridLayout_2.addWidget(self.logText, 4, 0, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.themesTab = QWidget()
        self.themesTab.setObjectName("themesTab")
        self.gridLayout = QGridLayout(self.themesTab)
        self.gridLayout.setObjectName("gridLayout")
        self.labelPreview = QLabel(self.themesTab)
        self.labelPreview.setObjectName("labelPreview")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelPreview.sizePolicy().hasHeightForWidth())
        self.labelPreview.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.labelPreview, 0, 2, 1, 1)

        self.listWidget = QListWidget(self.themesTab)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.listWidget, 0, 0, 5, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 1, 1, 2)

        self.btnApply = QPushButton(self.themesTab)
        self.btnApply.setObjectName("btnApply")

        self.gridLayout.addWidget(self.btnApply, 2, 1, 1, 2)

        self.btnRemove = QPushButton(self.themesTab)
        self.btnRemove.setObjectName("btnRemove")

        self.gridLayout.addWidget(self.btnRemove, 3, 1, 1, 2)

        self.tabWidget.addTab(self.themesTab, "")
        self.installTab = QWidget()
        self.installTab.setObjectName("installTab")
        self.gridLayout_3 = QGridLayout(self.installTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_3, 3, 0, 1, 1)

        self.btnSearch = QPushButton(self.installTab)
        self.btnSearch.setObjectName("btnSearch")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btnSearch.sizePolicy().hasHeightForWidth())
        self.btnSearch.setSizePolicy(sizePolicy2)
        self.btnSearch.setMaximumSize(QSize(120, 16777215))

        self.gridLayout_3.addWidget(self.btnSearch, 1, 1, 1, 1)

        self.btnInstall = QPushButton(self.installTab)
        self.btnInstall.setObjectName("btnInstall")

        self.gridLayout_3.addWidget(self.btnInstall, 2, 0, 1, 1)

        self.sourceLavel = QLabel(self.installTab)
        self.sourceLavel.setObjectName("sourceLavel")
        self.sourceLavel.setMaximumSize(QSize(16777215, 40))
        self.sourceLavel.setTextFormat(Qt.TextFormat.RichText)
        self.sourceLavel.setMargin(5)

        self.gridLayout_3.addWidget(self.sourceLavel, 0, 0, 1, 1)

        self.editSource = QLineEdit(self.installTab)
        self.editSource.setObjectName("editSource")

        self.gridLayout_3.addWidget(self.editSource, 1, 0, 1, 1)

        self.tabWidget.addTab(self.installTab, "")
        self.configTab = QWidget()
        self.configTab.setObjectName("configTab")
        self.configTab.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.gridLayout_8 = QGridLayout(self.configTab)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.screenGBox = QGroupBox(self.configTab)
        self.screenGBox.setObjectName("screenGBox")
        self.gridLayout_5 = QGridLayout(self.screenGBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gfxModeLabel = QLabel(self.screenGBox)
        self.gfxModeLabel.setObjectName("gfxModeLabel")

        self.gridLayout_5.addWidget(self.gfxModeLabel, 0, 0, 1, 1)

        self.comboGfxMode = QComboBox(self.screenGBox)
        self.comboGfxMode.addItem("")
        self.comboGfxMode.addItem("")
        self.comboGfxMode.addItem("")
        self.comboGfxMode.setObjectName("comboGfxMode")
        self.comboGfxMode.setEditable(True)

        self.gridLayout_5.addWidget(self.comboGfxMode, 0, 1, 1, 1)

        self.gfxPayloadLabel = QLabel(self.screenGBox)
        self.gfxPayloadLabel.setObjectName("gfxPayloadLabel")

        self.gridLayout_5.addWidget(self.gfxPayloadLabel, 1, 0, 1, 1)

        self.gfxPayloadCheckBox = QCheckBox(self.screenGBox)
        self.gfxPayloadCheckBox.setObjectName("gfxPayloadCheckBox")

        self.gridLayout_5.addWidget(self.gfxPayloadCheckBox, 1, 1, 1, 1)


        self.gridLayout_8.addWidget(self.screenGBox, 1, 0, 1, 1)

        self.advancedGBox = QGroupBox(self.configTab)
        self.advancedGBox.setObjectName("advancedGBox")
        self.gridLayout_7 = QGridLayout(self.advancedGBox)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.recoveryLabel = QLabel(self.advancedGBox)
        self.recoveryLabel.setObjectName("recoveryLabel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.recoveryLabel.sizePolicy().hasHeightForWidth())
        self.recoveryLabel.setSizePolicy(sizePolicy3)

        self.gridLayout_7.addWidget(self.recoveryLabel, 1, 0, 1, 1)

        self.osProberLabel = QLabel(self.advancedGBox)
        self.osProberLabel.setObjectName("osProberLabel")
        sizePolicy3.setHeightForWidth(self.osProberLabel.sizePolicy().hasHeightForWidth())
        self.osProberLabel.setSizePolicy(sizePolicy3)

        self.gridLayout_7.addWidget(self.osProberLabel, 0, 0, 1, 1)

        self.osProberCheckBox = QCheckBox(self.advancedGBox)
        self.osProberCheckBox.setObjectName("osProberCheckBox")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(1)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.osProberCheckBox.sizePolicy().hasHeightForWidth())
        self.osProberCheckBox.setSizePolicy(sizePolicy4)

        self.gridLayout_7.addWidget(self.osProberCheckBox, 0, 1, 1, 1)

        self.submenuLabel = QLabel(self.advancedGBox)
        self.submenuLabel.setObjectName("submenuLabel")
        sizePolicy3.setHeightForWidth(self.submenuLabel.sizePolicy().hasHeightForWidth())
        self.submenuLabel.setSizePolicy(sizePolicy3)

        self.gridLayout_7.addWidget(self.submenuLabel, 2, 0, 1, 1)

        self.recoveryCheckBox = QCheckBox(self.advancedGBox)
        self.recoveryCheckBox.setObjectName("recoveryCheckBox")
        sizePolicy4.setHeightForWidth(self.recoveryCheckBox.sizePolicy().hasHeightForWidth())
        self.recoveryCheckBox.setSizePolicy(sizePolicy4)

        self.gridLayout_7.addWidget(self.recoveryCheckBox, 1, 1, 1, 1)

        self.submenuCheckBox = QCheckBox(self.advancedGBox)
        self.submenuCheckBox.setObjectName("submenuCheckBox")
        sizePolicy4.setHeightForWidth(self.submenuCheckBox.sizePolicy().hasHeightForWidth())
        self.submenuCheckBox.setSizePolicy(sizePolicy4)

        self.gridLayout_7.addWidget(self.submenuCheckBox, 2, 1, 1, 1)


        self.gridLayout_8.addWidget(self.advancedGBox, 3, 0, 1, 1)

        self.kernelGBox = QGroupBox(self.configTab)
        self.kernelGBox.setObjectName("kernelGBox")
        self.gridLayout_6 = QGridLayout(self.kernelGBox)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.kernelParametersLineEdit = QLineEdit(self.kernelGBox)
        self.kernelParametersLineEdit.setObjectName("kernelParametersLineEdit")
        sizePolicy2.setHeightForWidth(self.kernelParametersLineEdit.sizePolicy().hasHeightForWidth())
        self.kernelParametersLineEdit.setSizePolicy(sizePolicy2)

        self.gridLayout_6.addWidget(self.kernelParametersLineEdit, 0, 1, 1, 1)

        self.kernelParametersLabel = QLabel(self.kernelGBox)
        self.kernelParametersLabel.setObjectName("kernelParametersLabel")
        sizePolicy3.setHeightForWidth(self.kernelParametersLabel.sizePolicy().hasHeightForWidth())
        self.kernelParametersLabel.setSizePolicy(sizePolicy3)

        self.gridLayout_6.addWidget(self.kernelParametersLabel, 0, 0, 1, 1)

        self.quietLabel = QLabel(self.kernelGBox)
        self.quietLabel.setObjectName("quietLabel")
        sizePolicy3.setHeightForWidth(self.quietLabel.sizePolicy().hasHeightForWidth())
        self.quietLabel.setSizePolicy(sizePolicy3)

        self.gridLayout_6.addWidget(self.quietLabel, 1, 0, 1, 1)

        self.quietCheckBox = QCheckBox(self.kernelGBox)
        self.quietCheckBox.setObjectName("quietCheckBox")
        sizePolicy4.setHeightForWidth(self.quietCheckBox.sizePolicy().hasHeightForWidth())
        self.quietCheckBox.setSizePolicy(sizePolicy4)

        self.gridLayout_6.addWidget(self.quietCheckBox, 1, 1, 1, 1)


        self.gridLayout_8.addWidget(self.kernelGBox, 2, 0, 1, 1)

        self.startUpGBox = QGroupBox(self.configTab)
        self.startUpGBox.setObjectName("startUpGBox")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(1)
        sizePolicy5.setVerticalStretch(1)
        sizePolicy5.setHeightForWidth(self.startUpGBox.sizePolicy().hasHeightForWidth())
        self.startUpGBox.setSizePolicy(sizePolicy5)
        self.gridLayout_4 = QGridLayout(self.startUpGBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_3 = QLabel(self.startUpGBox)
        self.label_3.setObjectName("label_3")

        self.gridLayout_4.addWidget(self.label_3, 2, 0, 1, 1)

        self.spinTimeout = QSpinBox(self.startUpGBox)
        self.spinTimeout.setObjectName("spinTimeout")
        sizePolicy2.setHeightForWidth(self.spinTimeout.sizePolicy().hasHeightForWidth())
        self.spinTimeout.setSizePolicy(sizePolicy2)
        self.spinTimeout.setMaximum(60)

        self.gridLayout_4.addWidget(self.spinTimeout, 0, 1, 1, 1)

        self.timeoutStyleLabel = QLabel(self.startUpGBox)
        self.timeoutStyleLabel.setObjectName("timeoutStyleLabel")

        self.gridLayout_4.addWidget(self.timeoutStyleLabel, 1, 0, 1, 1)

        self.comboDefault = QComboBox(self.startUpGBox)
        self.comboDefault.addItem("")
        self.comboDefault.addItem("")
        self.comboDefault.setObjectName("comboDefault")
        self.comboDefault.setEditable(True)

        self.gridLayout_4.addWidget(self.comboDefault, 2, 1, 1, 1)

        self.timeoutLabel = QLabel(self.startUpGBox)
        self.timeoutLabel.setObjectName("timeoutLabel")
        sizePolicy3.setHeightForWidth(self.timeoutLabel.sizePolicy().hasHeightForWidth())
        self.timeoutLabel.setSizePolicy(sizePolicy3)

        self.gridLayout_4.addWidget(self.timeoutLabel, 0, 0, 1, 1)

        self.comboTimeoutStyle = QComboBox(self.startUpGBox)
        self.comboTimeoutStyle.addItem("")
        self.comboTimeoutStyle.addItem("")
        self.comboTimeoutStyle.addItem("")
        self.comboTimeoutStyle.setObjectName("comboTimeoutStyle")
        sizePolicy2.setHeightForWidth(self.comboTimeoutStyle.sizePolicy().hasHeightForWidth())
        self.comboTimeoutStyle.setSizePolicy(sizePolicy2)

        self.gridLayout_4.addWidget(self.comboTimeoutStyle, 1, 1, 1, 1)


        self.gridLayout_8.addWidget(self.startUpGBox, 0, 0, 1, 1)

        self.groupBox = QGroupBox(self.configTab)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnApplyCfg = QPushButton(self.groupBox)
        self.btnApplyCfg.setObjectName("btnApplyCfg")
        sizePolicy4.setHeightForWidth(self.btnApplyCfg.sizePolicy().hasHeightForWidth())
        self.btnApplyCfg.setSizePolicy(sizePolicy4)

        self.horizontalLayout.addWidget(self.btnApplyCfg)

        self.btnReloadCfg = QPushButton(self.groupBox)
        self.btnReloadCfg.setObjectName("btnReloadCfg")
        sizePolicy4.setHeightForWidth(self.btnReloadCfg.sizePolicy().hasHeightForWidth())
        self.btnReloadCfg.setSizePolicy(sizePolicy4)

        self.horizontalLayout.addWidget(self.btnReloadCfg)


        self.gridLayout_8.addWidget(self.groupBox, 4, 0, 1, 1)

        self.tabWidget.addTab(self.configTab, "")

        self.gridLayout_2.addWidget(self.tabWidget, 1, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 2, 0, 2, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
        self.labelPreview.setText("")
        self.btnApply.setText(QCoreApplication.translate("MainWindow", "Apply", None))
        self.btnRemove.setText(QCoreApplication.translate("MainWindow", "Remove", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.themesTab), QCoreApplication.translate("MainWindow", "Themes", None))
        self.btnSearch.setText(QCoreApplication.translate("MainWindow", "Browse...", None))
        self.btnInstall.setText(QCoreApplication.translate("MainWindow", "Install", None))
        self.sourceLavel.setText(QCoreApplication.translate("MainWindow", "Source (URL git or folder):", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.installTab), QCoreApplication.translate("MainWindow", "Install Theme", None))
#if QT_CONFIG(accessibility)
        self.configTab.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.screenGBox.setTitle(QCoreApplication.translate("MainWindow", "Screen", None))
        self.gfxModeLabel.setText(QCoreApplication.translate("MainWindow", "Resolution:", None))
        self.comboGfxMode.setItemText(0, QCoreApplication.translate("MainWindow", "auto", None))
        self.comboGfxMode.setItemText(1, QCoreApplication.translate("MainWindow", "1920x1080", None))
        self.comboGfxMode.setItemText(2, QCoreApplication.translate("MainWindow", "2560x1440", None))

        self.gfxPayloadLabel.setText(QCoreApplication.translate("MainWindow", "Keep resolution on Linux:", None))
        self.gfxPayloadCheckBox.setText(QCoreApplication.translate("MainWindow", "Keep", None))
        self.advancedGBox.setTitle(QCoreApplication.translate("MainWindow", "Advanced", None))
        self.recoveryLabel.setText(QCoreApplication.translate("MainWindow", "Hide recovery entries:", None))
        self.osProberLabel.setText(QCoreApplication.translate("MainWindow", "Detect other OS:", None))
#if QT_CONFIG(tooltip)
        self.osProberCheckBox.setToolTip(QCoreApplication.translate("MainWindow", "GRUB_DISABLE_OS_PROBER", None))
#endif // QT_CONFIG(tooltip)
        self.osProberCheckBox.setText(QCoreApplication.translate("MainWindow", "Enabled", None))
        self.submenuLabel.setText(QCoreApplication.translate("MainWindow", "Join kernels in sub-menu:", None))
#if QT_CONFIG(tooltip)
        self.recoveryCheckBox.setToolTip(QCoreApplication.translate("MainWindow", "GRUB_DISABLE_RECOVERY", None))
#endif // QT_CONFIG(tooltip)
        self.recoveryCheckBox.setText(QCoreApplication.translate("MainWindow", "Enabled", None))
#if QT_CONFIG(tooltip)
        self.submenuCheckBox.setToolTip(QCoreApplication.translate("MainWindow", "GRUB_DISABLE_SUBMEN", None))
#endif // QT_CONFIG(tooltip)
        self.submenuCheckBox.setText(QCoreApplication.translate("MainWindow", "Enabled", None))
        self.kernelGBox.setTitle(QCoreApplication.translate("MainWindow", "Kernel", None))
        self.kernelParametersLabel.setText(QCoreApplication.translate("MainWindow", "Kernel parameters:", None))
        self.quietLabel.setText(QCoreApplication.translate("MainWindow", "Hide startup messages:", None))
        self.quietCheckBox.setText(QCoreApplication.translate("MainWindow", "Quiet", None))
        self.startUpGBox.setTitle(QCoreApplication.translate("MainWindow", "Startup", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", "Default entry:", None))
        self.spinTimeout.setSuffix(QCoreApplication.translate("MainWindow", " s", None))
        self.timeoutStyleLabel.setText(QCoreApplication.translate("MainWindow", "Show menu:", None))
        self.comboDefault.setItemText(0, QCoreApplication.translate("MainWindow", "0", None))
        self.comboDefault.setItemText(1, QCoreApplication.translate("MainWindow", "saved", None))

        self.timeoutLabel.setText(QCoreApplication.translate("MainWindow", "Timeout:", None))
        self.comboTimeoutStyle.setItemText(0, QCoreApplication.translate("MainWindow", "men", None))
        self.comboTimeoutStyle.setItemText(1, QCoreApplication.translate("MainWindow", "countdown", None))
        self.comboTimeoutStyle.setItemText(2, QCoreApplication.translate("MainWindow", "hidden", None))

        self.groupBox.setTitle("")
        self.btnApplyCfg.setText(QCoreApplication.translate("MainWindow", "Apply", None))
        self.btnReloadCfg.setText(QCoreApplication.translate("MainWindow", "Reload", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.configTab), QCoreApplication.translate("MainWindow", "Grub Config", None))
    # retranslateUi

