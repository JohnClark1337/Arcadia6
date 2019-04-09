from PyQt5 import QtWidgets
import PyQt5
import xml.etree.ElementTree as ET
import sys
import Arcadia6

class ArcadiaPy(QtWidgets.QMainWindow, Arcadia6.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ArcadiaPy, self).__init__(parent)
        self.setupUi(self)
        self.btnExit.clicked.connect(QtWidgets.QApplication.instance().quit)
        self.tabOS.setCurrentIndex(0)
        self.lstWindows.addItems(antivirusNames)
        self.lstWindows.setCurrentRow(0)
        self.iconImage.setPixmap(PyQt5.QtGui.QPixmap("Icons/Arcadia.ico"))
        self.lstWindows.currentItemChanged.connect(self.popWinSoft)
        self.btnAntivirus.clicked.connect(lambda: self.softwareList(1))
        self.btnAntimalware.clicked.connect(lambda: self.softwareList(2))
        self.btnClean.clicked.connect(lambda: self.softwareList(3))
        self.btnSetup.clicked.connect(lambda: self.softwareList(4))
        self.btnTools.clicked.connect(lambda: self.softwareList(5))
    

    def clearLists(self):
        self.lstWindows.clear()
        self.lstLinux.clear()
        self.lstMac.clear()


    def softwareList(self, category):
        self.clearLists()
        if category == 1:
            self.lstWindows.addItems(antivirusNames)
        elif category == 2:
            self.lstWindows.addItems(antimalNames)
        elif category == 3:
            self.lstWindows.addItems(cleanNames)
        elif category == 4:
            self.lstWindows.addItems(setupNames)
        elif category == 5:
            self.lstWindows.addItems(toolNames)
        else:
            self.lstWindows.addItems(antivirusNames)
        self.lstWindows.setCurrentRow(0)


    def popWinSoft(self):
        try:
            itemName = self.lstWindows.currentItem().text()
            root = ET.parse('Programs.xml').getroot()
            #print(itemName)
            
            for item in root.findall('Item'):
                if item.get('name') ==  itemName:
                    pix = PyQt5.QtGui.QPixmap(item.find('Icon').text)
                    self.iconImage.setPixmap(pix)
                    self.txtDescription.setText(item.find('Description').text)
        except:
            pix = PyQt5.QtGui.QPixmap("Icons/Arcadia.ico")
            self.iconImage.setPixmap(pix)
            

antivirusNames = list()
antimalNames = list()
cleanNames = list()
setupNames = list()
toolNames = list()


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ArcadiaPy()
    form.show()
    app.exec_()

def readProgramList(fileLoc):
    root = ET.parse(fileLoc).getroot()
    for item in root.findall('Item'):
        if item.get('cat') == 'Antivirus':
            antivirusNames.append(item.get('name'))
        elif item.get('cat') == 'Antimalware':
            antimalNames.append(item.get('name'))
        elif item.get('cat') == 'Clean':
            cleanNames.append(item.get('name'))
        elif item.get('cat') == 'Setup':
            setupNames.append(item.get('name'))
        elif item.get('cat') == 'Tools':
            toolNames.append(item.get('name'))
        antivirusNames.sort()
        antimalNames.sort()
        cleanNames.sort()
        setupNames.sort()
        toolNames.sort()

if __name__ == '__main__':

    readProgramList('Programs.xml')
    main()
