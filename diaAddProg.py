# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'diaAddProg.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_diaAddProg(object):
    def setupUi(self, diaAddProg):
        diaAddProg.setObjectName("diaAddProg")
        diaAddProg.resize(400, 278)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Icons/Arcadia.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        diaAddProg.setWindowIcon(icon)
        self.buttonBox = QtWidgets.QDialogButtonBox(diaAddProg)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.frmOS = QtWidgets.QFrame(diaAddProg)
        self.frmOS.setGeometry(QtCore.QRect(40, 30, 301, 31))
        self.frmOS.setFrameShape(QtWidgets.QFrame.Box)
        self.frmOS.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frmOS.setObjectName("frmOS")
        self.rbnWindows = QtWidgets.QRadioButton(self.frmOS)
        self.rbnWindows.setGeometry(QtCore.QRect(20, 10, 71, 17))
        self.rbnWindows.setChecked(True)
        self.rbnWindows.setObjectName("rbnWindows")
        self.rbnMac = QtWidgets.QRadioButton(self.frmOS)
        self.rbnMac.setGeometry(QtCore.QRect(130, 10, 61, 17))
        self.rbnMac.setObjectName("rbnMac")
        self.rbnLinux = QtWidgets.QRadioButton(self.frmOS)
        self.rbnLinux.setGeometry(QtCore.QRect(230, 10, 51, 17))
        self.rbnLinux.setObjectName("rbnLinux")
        self.lblOS = QtWidgets.QLabel(diaAddProg)
        self.lblOS.setGeometry(QtCore.QRect(50, 10, 101, 16))
        self.lblOS.setObjectName("lblOS")
        self.tbxName = QtWidgets.QLineEdit(diaAddProg)
        self.tbxName.setGeometry(QtCore.QRect(50, 80, 113, 20))
        self.tbxName.setObjectName("tbxName")
        self.tbxLocation = QtWidgets.QLineEdit(diaAddProg)
        self.tbxLocation.setGeometry(QtCore.QRect(200, 80, 141, 20))
        self.tbxLocation.setClearButtonEnabled(False)
        self.tbxLocation.setObjectName("tbxLocation")
        self.tbtnLocation = QtWidgets.QToolButton(diaAddProg)
        self.tbtnLocation.setGeometry(QtCore.QRect(340, 80, 25, 19))
        self.tbtnLocation.setObjectName("tbtnLocation")
        self.tbxDescription = QtWidgets.QPlainTextEdit(diaAddProg)
        self.tbxDescription.setGeometry(QtCore.QRect(50, 120, 311, 81))
        self.tbxDescription.setObjectName("tbxDescription")
        self.tbtnItemLocation = QtWidgets.QToolButton(diaAddProg)
        self.tbtnItemLocation.setGeometry(QtCore.QRect(340, 210, 25, 19))
        self.tbtnItemLocation.setObjectName("tbtnItemLocation")
        self.tbxItemLocation = QtWidgets.QLineEdit(diaAddProg)
        self.tbxItemLocation.setGeometry(QtCore.QRect(200, 210, 141, 20))
        self.tbxItemLocation.setClearButtonEnabled(False)
        self.tbxItemLocation.setObjectName("tbxItemLocation")
        self.iconView = QtWidgets.QLabel(diaAddProg)
        self.iconView.setGeometry(QtCore.QRect(140, 210, 41, 41))
        self.iconView.setObjectName("iconView")

        self.retranslateUi(diaAddProg)
        self.buttonBox.accepted.connect(diaAddProg.accept)
        self.buttonBox.rejected.connect(diaAddProg.reject)
        QtCore.QMetaObject.connectSlotsByName(diaAddProg)

    def retranslateUi(self, diaAddProg):
        _translate = QtCore.QCoreApplication.translate
        diaAddProg.setWindowTitle(_translate("diaAddProg", "Add Program"))
        self.rbnWindows.setText(_translate("diaAddProg", "Windows"))
        self.rbnMac.setText(_translate("diaAddProg", "Mac OS"))
        self.rbnLinux.setText(_translate("diaAddProg", "Linux"))
        self.lblOS.setText(_translate("diaAddProg", "Operating System"))
        self.tbxName.setPlaceholderText(_translate("diaAddProg", "Name"))
        self.tbxLocation.setPlaceholderText(_translate("diaAddProg", "Location"))
        self.tbtnLocation.setText(_translate("diaAddProg", "..."))
        self.tbxDescription.setPlaceholderText(_translate("diaAddProg", "Description"))
        self.tbtnItemLocation.setText(_translate("diaAddProg", "..."))
        self.tbxItemLocation.setPlaceholderText(_translate("diaAddProg", "Icon Location"))
        self.iconView.setText(_translate("diaAddProg", "Default"))

