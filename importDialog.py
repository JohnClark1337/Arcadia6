# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmImport(object):
    def setupUi(self, frmImport):
        frmImport.setObjectName("frmImport")
        frmImport.resize(448, 299)
        frmImport.setMinimumSize(QtCore.QSize(448, 299))
        frmImport.setMaximumSize(QtCore.QSize(448, 299))
        self.txtInstructions = QtWidgets.QTextEdit(frmImport)
        self.txtInstructions.setEnabled(False)
        self.txtInstructions.setGeometry(QtCore.QRect(30, 20, 391, 181))
        self.txtInstructions.setObjectName("txtInstructions")
        self.tbxImFolder = QtWidgets.QLineEdit(frmImport)
        self.tbxImFolder.setGeometry(QtCore.QRect(50, 230, 261, 20))
        self.tbxImFolder.setObjectName("tbxImFolder")
        self.tbnImFolder = QtWidgets.QToolButton(frmImport)
        self.tbnImFolder.setGeometry(QtCore.QRect(320, 230, 25, 19))
        self.tbnImFolder.setObjectName("tbnImFolder")
        self.btnImport = QtWidgets.QPushButton(frmImport)
        self.btnImport.setGeometry(QtCore.QRect(140, 260, 75, 23))
        self.btnImport.setObjectName("btnImport")
        self.btnExit = QtWidgets.QPushButton(frmImport)
        self.btnExit.setGeometry(QtCore.QRect(330, 260, 75, 23))
        self.btnExit.setObjectName("btnExit")

        self.retranslateUi(frmImport)
        QtCore.QMetaObject.connectSlotsByName(frmImport)

    def retranslateUi(self, frmImport):
        _translate = QtCore.QCoreApplication.translate
        frmImport.setWindowTitle(_translate("frmImport", "Import"))
        self.tbnImFolder.setText(_translate("frmImport", "..."))
        self.btnImport.setText(_translate("frmImport", "Import"))
        self.btnExit.setText(_translate("frmImport", "Exit"))

