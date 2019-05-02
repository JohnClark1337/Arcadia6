# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'utilDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmUtilities(object):
    def setupUi(self, frmUtilities):
        frmUtilities.setObjectName("frmUtilities")
        frmUtilities.resize(593, 309)
        self.tbxFrom = QtWidgets.QLineEdit(frmUtilities)
        self.tbxFrom.setGeometry(QtCore.QRect(20, 30, 281, 20))
        self.tbxFrom.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.tbxFrom.setObjectName("tbxFrom")
        self.tbxTo = QtWidgets.QLineEdit(frmUtilities)
        self.tbxTo.setGeometry(QtCore.QRect(20, 60, 281, 20))
        self.tbxTo.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.tbxTo.setObjectName("tbxTo")
        self.tbnFrom = QtWidgets.QToolButton(frmUtilities)
        self.tbnFrom.setGeometry(QtCore.QRect(320, 30, 25, 19))
        self.tbnFrom.setObjectName("tbnFrom")
        self.tbnTo = QtWidgets.QToolButton(frmUtilities)
        self.tbnTo.setGeometry(QtCore.QRect(320, 60, 25, 19))
        self.tbnTo.setObjectName("tbnTo")
        self.btnBackup = QtWidgets.QPushButton(frmUtilities)
        self.btnBackup.setGeometry(QtCore.QRect(420, 40, 121, 23))
        self.btnBackup.setObjectName("btnBackup")
        self.btnExit = QtWidgets.QPushButton(frmUtilities)
        self.btnExit.setGeometry(QtCore.QRect(490, 270, 75, 23))
        self.btnExit.setObjectName("btnExit")
        self.tbxDriver = QtWidgets.QLineEdit(frmUtilities)
        self.tbxDriver.setGeometry(QtCore.QRect(20, 120, 281, 20))
        self.tbxDriver.setObjectName("tbxDriver")
        self.tbnDriver = QtWidgets.QToolButton(frmUtilities)
        self.tbnDriver.setGeometry(QtCore.QRect(320, 120, 25, 19))
        self.tbnDriver.setObjectName("tbnDriver")
        self.btnDriver = QtWidgets.QPushButton(frmUtilities)
        self.btnDriver.setGeometry(QtCore.QRect(420, 120, 121, 23))
        self.btnDriver.setObjectName("btnDriver")
        self.btnTest = QtWidgets.QPushButton(frmUtilities)
        self.btnTest.setGeometry(QtCore.QRect(490, 180, 75, 23))
        self.btnTest.setObjectName("btnTest")
        self.pbrFiles = QtWidgets.QProgressBar(frmUtilities)
        self.pbrFiles.setGeometry(QtCore.QRect(40, 270, 411, 23))
        self.pbrFiles.setProperty("value", 0)
        self.pbrFiles.setObjectName("pbrFiles")

        self.retranslateUi(frmUtilities)
        QtCore.QMetaObject.connectSlotsByName(frmUtilities)

    def retranslateUi(self, frmUtilities):
        _translate = QtCore.QCoreApplication.translate
        frmUtilities.setWindowTitle(_translate("frmUtilities", "Utilities"))
        self.tbxFrom.setPlaceholderText(_translate("frmUtilities", "Original Folder Location"))
        self.tbxTo.setPlaceholderText(_translate("frmUtilities", "Backup Folder Location"))
        self.tbnFrom.setText(_translate("frmUtilities", "..."))
        self.tbnTo.setText(_translate("frmUtilities", "..."))
        self.btnBackup.setText(_translate("frmUtilities", "File Backup"))
        self.btnExit.setText(_translate("frmUtilities", "Exit"))
        self.tbxDriver.setPlaceholderText(_translate("frmUtilities", "Driver Backup Location"))
        self.tbnDriver.setText(_translate("frmUtilities", "..."))
        self.btnDriver.setText(_translate("frmUtilities", "Driver Backup"))
        self.btnTest.setText(_translate("frmUtilities", "test"))

