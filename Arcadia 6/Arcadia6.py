# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Arcadia6.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(818, 503)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icons/Arcadia.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frmCategory = QtWidgets.QFrame(self.centralwidget)
        self.frmCategory.setGeometry(QtCore.QRect(20, 30, 171, 311))
        self.frmCategory.setFrameShape(QtWidgets.QFrame.Panel)
        self.frmCategory.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frmCategory.setObjectName("frmCategory")
        self.btnAntivirus = QtWidgets.QPushButton(self.frmCategory)
        self.btnAntivirus.setGeometry(QtCore.QRect(10, 10, 151, 51))
        self.btnAntivirus.setObjectName("btnAntivirus")
        self.pushButton_2 = QtWidgets.QPushButton(self.frmCategory)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 70, 151, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.frmCategory)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 130, 151, 51))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.frmCategory)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 190, 151, 51))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.frmCategory)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 250, 151, 51))
        self.pushButton_5.setObjectName("pushButton_5")
        self.lblCategory = QtWidgets.QLabel(self.centralwidget)
        self.lblCategory.setGeometry(QtCore.QRect(20, 10, 47, 13))
        self.lblCategory.setObjectName("lblCategory")
        self.btnRun = QtWidgets.QPushButton(self.centralwidget)
        self.btnRun.setGeometry(QtCore.QRect(10, 350, 191, 61))
        self.btnRun.setObjectName("btnRun")
        self.btnAutoRun = QtWidgets.QPushButton(self.centralwidget)
        self.btnAutoRun.setGeometry(QtCore.QRect(30, 420, 151, 31))
        self.btnAutoRun.setObjectName("btnAutoRun")
        self.tabOS = QtWidgets.QTabWidget(self.centralwidget)
        self.tabOS.setGeometry(QtCore.QRect(230, 30, 411, 391))
        self.tabOS.setObjectName("tabOS")
        self.tabWindows = QtWidgets.QWidget()
        self.tabWindows.setObjectName("tabWindows")
        self.lstWindows = QtWidgets.QListWidget(self.tabWindows)
        self.lstWindows.setGeometry(QtCore.QRect(0, 0, 401, 361))
        self.lstWindows.setObjectName("lstWindows")
        self.tabOS.addTab(self.tabWindows, "")
        self.tabLinux = QtWidgets.QWidget()
        self.tabLinux.setObjectName("tabLinux")
        self.lstLinux = QtWidgets.QListWidget(self.tabLinux)
        self.lstLinux.setGeometry(QtCore.QRect(0, 0, 401, 361))
        self.lstLinux.setObjectName("lstLinux")
        self.tabOS.addTab(self.tabLinux, "")
        self.tabMac = QtWidgets.QWidget()
        self.tabMac.setObjectName("tabMac")
        self.lstMac = QtWidgets.QListWidget(self.tabMac)
        self.lstMac.setGeometry(QtCore.QRect(0, 0, 401, 361))
        self.lstMac.setObjectName("lstMac")
        self.tabOS.addTab(self.tabMac, "")
        self.iconView = QtWidgets.QGraphicsView(self.centralwidget)
        self.iconView.setGeometry(QtCore.QRect(660, 30, 141, 101))
        self.iconView.setAutoFillBackground(False)
        self.iconView.setObjectName("iconView")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(650, 140, 161, 101))
        self.listView.setObjectName("listView")
        self.btnExit = QtWidgets.QPushButton(self.centralwidget)
        self.btnExit.setGeometry(QtCore.QRect(680, 420, 101, 31))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(19)
        font.setBold(True)
        font.setWeight(75)
        self.btnExit.setFont(font)
        self.btnExit.setObjectName("btnExit")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 818, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabOS.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Arcadia 6"))
        self.btnAntivirus.setText(_translate("MainWindow", "Antivirus"))
        self.pushButton_2.setText(_translate("MainWindow", "Antimalware"))
        self.pushButton_3.setText(_translate("MainWindow", "Clean"))
        self.pushButton_4.setText(_translate("MainWindow", "Setup"))
        self.pushButton_5.setText(_translate("MainWindow", "Tools"))
        self.lblCategory.setText(_translate("MainWindow", "Category"))
        self.btnRun.setText(_translate("MainWindow", "Run"))
        self.btnAutoRun.setText(_translate("MainWindow", "Auto Run"))
        self.tabOS.setTabText(self.tabOS.indexOf(self.tabWindows), _translate("MainWindow", "Windows"))
        self.tabOS.setTabText(self.tabOS.indexOf(self.tabLinux), _translate("MainWindow", "Linux"))
        self.tabOS.setTabText(self.tabOS.indexOf(self.tabMac), _translate("MainWindow", "Mac OS X"))
        self.btnExit.setText(_translate("MainWindow", "Exit"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

