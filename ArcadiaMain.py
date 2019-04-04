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
        self.lstWindows.setCurrentRow(3)
        self.lstWindows.itemClicked.connect(popIcon)
    

def popIcon(self):
    root = ET.parse('Programs.xml').getroot()
    print("Hello World")
    # for item in root.findall('Item'):
    #     if item.get('name') ==  name:
    #         pix = PyQt5.QtGui.QPixmap(item.find('Icon').text)
    #         self.iconImage.setPixmap(pix)
            


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
