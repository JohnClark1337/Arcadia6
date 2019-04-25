from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
from shutil import copyfile
import PyQt5
import xml.etree.ElementTree as ET
import sys
import os
import subprocess
import Arcadia6
import progEditor
import diaAddProg

class ArcadiaPy(QtWidgets.QMainWindow, Arcadia6.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ArcadiaPy, self).__init__(parent)
        self.setupUi(self)
        self.btnExit.clicked.connect(QtWidgets.QApplication.instance().quit)
        self.tabOS.setCurrentIndex(0)
        self.lstWindows.addItems(mainList[0])
        self.lstWindows.setCurrentRow(0)
        self.iconImage.setPixmap(PyQt5.QtGui.QPixmap("Icons/Arcadia.ico"))
        self.popWinSoft()
        self.lstWindows.currentItemChanged.connect(self.popWinSoft)
        self.btnAntivirus.clicked.connect(lambda: self.softwareList(1))
        self.btnAntimalware.clicked.connect(lambda: self.softwareList(2))
        self.btnClean.clicked.connect(lambda: self.softwareList(3))
        self.btnSetup.clicked.connect(lambda: self.softwareList(4))
        self.btnTools.clicked.connect(lambda: self.softwareList(5))
        self.btnRun.clicked.connect(runProgram)
        self.btnEditor.clicked.connect(self.openEditor)
    

    def openEditor(self):
        formEdit = EditorPy(self)
        formEdit.show()


    def clearLists(self):
        self.lstWindows.clear()
        self.lstLinux.clear()
        self.lstMac.clear()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            runProgram()

    def softwareList(self, category):
        self.clearLists()
        if category == 1:
            self.lstWindows.addItems(mainList[0])
        elif category == 2:
            self.lstWindows.addItems(mainList[1])
        elif category == 3:
            self.lstWindows.addItems(mainList[2])
        elif category == 4:
            self.lstWindows.addItems(mainList[3])
        elif category == 5:
            self.lstWindows.addItems(mainList[4])
        else:
            self.lstWindows.addItems(mainList[0])
        self.lstWindows.setCurrentRow(0)


    def popWinSoft(self):
        global selectedLocation
        try:
            itemName = self.lstWindows.currentItem().text()
            root = ET.parse('Programs.xml').getroot()

            for item in root.findall('Item'):
                if item.get('name') ==  itemName:
                    pix = PyQt5.QtGui.QPixmap(item.find('Icon').text)
                    self.iconImage.setPixmap(pix)
                    self.txtDescription.setText(item.find('Description').text)
                    selectedLocation = item.find('Location').text
        except:
            pix = PyQt5.QtGui.QPixmap("Icons/Arcadia.ico")
            self.iconImage.setPixmap(pix)


class EditorPy(QtWidgets.QMainWindow, progEditor.Ui_frmXMLEdit):
    def __init__(self, parent=None):
        super(EditorPy, self).__init__(parent)
        self.setupUi(self)
        self.lblCurrentDiff.hide()
        self.lblLeftArrow.hide()
        self.lblModDiff.hide()
        self.lblRightArrow.hide()
        self.btnRemove.clicked.connect(self.removeEntry)
        self.chkChanges.stateChanged.connect(self.showDiffs)
        self.populateList(self.lstCurrent, mainList)
        self.btnAdd.clicked.connect(self.addEntry)
        self.actionClose.triggered.connect(self.close)
        self.btnExit.clicked.connect(self.close)
        self.btnRefresh.clicked.connect(self.refreshList)
        copyfile('Programs.xml', 'temp.xml')
        readProgramList('temp.xml', tempList)
        self.populateList(self.lstMod, tempList)


    def addEntry(self):
        addDia = AddProg(self)
        addDia.show()
        self.refreshList()

    
    def removeEntry(self):
        name = self.lstMod.currentItem().text()
        root = ET.parse('temp.xml').getroot()

        
        
    
    def showDiffs(self, state):
        if state == QtCore.Qt.Checked:
            self.lblCurrentDiff.show()
            self.lblLeftArrow.show()
            self.lblModDiff.show()
            self.lblRightArrow.show()
            longmain = list()
            longtemp = list()
            for tItem in tempList:
                for stItem in tItem:
                    longtemp.append(stItem)
            for mItem in mainList:
                for smItem in mItem:
                    longmain.append(smItem)
            for lm in longmain:
                if lm not in longtemp:
                    print(lm + " will be removed.")
            for lt in longtemp:
                if lt not in longmain:
                    print(lt + " will be added.")
                    
                        
            
                    
                         
        else:
            self.lblCurrentDiff.hide()
            self.lblLeftArrow.hide()
            self.lblModDiff.hide()
            self.lblRightArrow.hide()


    def populateList(self, wid, biglist):
        wid.addItem("Antivirus:\n")
        wid.addItems(biglist[0])
        wid.addItem("\nAntimalware:\n")
        wid.addItems(biglist[1])
        wid.addItem("\nCleaning Tools:\n")
        wid.addItems(biglist[2])
        wid.addItem("\nSetup Tools:\n")
        wid.addItems(biglist[3])
        wid.addItem("\nRandom Tools:\n")
        wid.addItems(biglist[4])

    def refreshList(self):
        self.lstMod.clear()
        for item in tempList:
            item.clear()
        readProgramList('temp.xml', tempList)
        self.populateList(self.lstMod, tempList)
        

class AddProg(QtWidgets.QDialog, diaAddProg.Ui_diaAddProg):
    def __init__(self, parent=None):
        super(AddProg, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.buttonBox.accepted.connect(self.addProgramInfo)
        


    def addProgramInfo(self):
        name = self.tbxName.text()
        loc = self.tbxLocation.text()
        desc = self.tbxDescription.toPlainText()
        ico = self.tbxItemLocation.text()
        ty = ''
        oss = ''
        tboxes = {self.rbnAntimalware, self.rbnAntivirus, self.rbnClean, self.rbnSetup, self.rbnTools}
        for t in tboxes:
            if t.isChecked():
                ty = t.text()
        oboxes = {self.rbnLinux, self.rbnMac, self.rbnWindows}
        for o in oboxes:
            if o.isChecked():
                oss = o.text()
        writeTempList('temp.xml', ty, name, desc, loc, ' ', ico)
        #writeTempList('temp.xml', 'Tools', 'Tacocat', 'this is a test of the taco cat', 'wherever', 'here is the link', 'here is the icon')
        self.parent.refreshList()


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ArcadiaPy()
    form.show()
    app.exec_()

def readProgramList(fileLoc, biglist):
    root = ET.parse(fileLoc).getroot()
    for item in root.findall('Item'):
        if item.get('cat') == 'Antivirus':
            biglist[0].append(item.get('name'))
        elif item.get('cat') == 'Antimalware':
            biglist[1].append(item.get('name'))
        elif item.get('cat') == 'Clean':
            biglist[2].append(item.get('name'))
        elif item.get('cat') == 'Setup':
            biglist[3].append(item.get('name'))
        elif item.get('cat') == 'Tools':
            biglist[4].append(item.get('name'))

        for cat in biglist:
            cat.sort()
       
def writeTempList(fileLoc, cat, name, des, loc, link, icon):
    tree = ET.parse(fileLoc)
    root = tree.getroot()
    new_item = ET.SubElement(root, 'Item', attrib={"cat": cat, "name": name})
    new_item_des = ET.SubElement(new_item, 'Description')
    new_item_loc = ET.SubElement(new_item, 'Location')
    new_item_link = ET.SubElement(new_item, 'Link')
    new_item_icon = ET.SubElement(new_item, 'Icon')

    new_item_des.text = des
    new_item_loc.text = loc
    new_item_link.text = link
    new_item_icon.text = icon

    tree.write(fileLoc)


def dialog(text, title):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()



def runProgram():
    try:
        if selectedLocation is not '':
            subprocess.call([selectedLocation])
    except:
        dialog("Program Not Found at {}".format(selectedLocation), "Error") 


mainList = list((list(), list(), list(), list(), list()))
tempList = list((list(), list(), list(), list(), list()))

if __name__ == '__main__':

    readProgramList('Programs.xml', mainList)
    main()
