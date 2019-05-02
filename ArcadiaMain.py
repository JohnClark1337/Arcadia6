from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
from shutil import copyfile
import PyQt5
import xml.etree.ElementTree as ET
import sys
import shlex
import os, ctypes
import subprocess
import Arcadia6
import progEditor
import diaAddProg
import utilDialog

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
        self.btnUtilites.clicked.connect(self.openUtil)
    

    def openEditor(self):
        formEdit = EditorPy(self)
        formEdit.show()

    def openUtil(self):
        util = UtilDialog(self)
        util.show()

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
                    if os.path.exists(selectedLocation) == False:
                        self.lblAvailable.setText("Unavailable")
                        self.lblAvailable.setStyleSheet("QLabel {background-color: red; color: white} QToolTip {background-color: white; color: black}")
                        self.lblAvailable.setToolTip("Program not available.")
                    else:
                        self.lblAvailable.setText("Available")
                        self.lblAvailable.setStyleSheet("QLabel {background-color: green; color: white} QToolTip{background-color: white; color: black}")
                        self.lblAvailable.setToolTip("Program Available")
                    if sys.platform == 'win32':
                        self.lblWebsite.setText('<a href="{}">Website</a>'.format(item.find('Link').text))
                    else:
                        self.lblWebsite.setDisabled
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
        clearTempList()
        copyfile('Programs.xml', 'temp.xml')
        readProgramList('temp.xml', tempList)
        self.populateList(self.lstMod, tempList)


    def addEntry(self):
        addDia = AddProg(self)
        addDia.show()
        self.refreshList()

    
    def removeEntry(self):
        name = self.lstMod.selectedItems()
        name = name[0].text()
        tree = ET.parse('temp.xml')
        root = tree.getroot()

        for item in root:
            if item.attrib["name"] == name:
                dialog("Removing {}".format(item.attrib['name']), "Removing Item")
                root.remove(item)

        tree.write("temp.xml")  
        self.refreshList()

    
    def showDiffs(self, state):
        if state == QtCore.Qt.Checked:
            self.lblCurrentDiff.show()
            self.lblLeftArrow.show()
            self.lblModDiff.show()
            self.lblRightArrow.show()
            longmain = list()
            longtemp = list()
            mint = 0
            tint = 0
            for tItem in tempList:
                for stItem in tItem:
                    tint += 1
                    longtemp.append(stItem)
            for mItem in mainList:
                for smItem in mItem:
                    mint += 1
                    longmain.append(smItem)
            for lm in longmain:
                if lm not in longtemp:
                    mdif = 0
                    if mint > tint:
                        mdif = mint - tint
                    self.lblCurrentDiff.setText(str(mdif))
                    print(lm + " will be removed.")
            for lt in longtemp:
                if lt not in longmain:
                    tdif = 0
                    if tint > mint:
                        tdif = tint - mint
                    self.lblModDiff.setText(str(tdif))
                    #print(lt + " will be added.")             
                         
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
        self.tbtnLocation.clicked.connect(lambda: self.openFileDialog(0))
        self.tbtnItemLocation.clicked.connect(lambda: self.openFileDialog(1))
        


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
        self.parent.refreshList()


    def openFileDialog(self, ftype):
        if ftype == 0:
            d = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select File", os.path.expanduser('~'),
            filter=('Windows Executable (*.exe);;Microsoft Installer (*.msi)'))[0]
            if d != '':
                self.tbxLocation.setText(d)
        else:
            d = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select File", os.path.expanduser('~'),
            filter=('PNG File (*.png);;JPEG/JPG (*.jpeg *.jpg)'))[0]
            if d != '':
                self.tbxItemLocation.setText(d)

class UtilDialog(QtWidgets.QDialog, utilDialog.Ui_frmUtilities):
    def __init__(self, parent=None):
        super(UtilDialog, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.aCheck()
        self.btnBackup.clicked.connect(self.runBackup)
        self.btnDriver.clicked.connect(self.runDriverBackup)
        self.btnExit.clicked.connect(self.close)
        self.tbnFrom.clicked.connect(lambda: self.openDirDialog(0))
        self.tbnTo.clicked.connect(lambda: self.openDirDialog(1))
        #self.btnTest.clicked.connect(self.testCounter)

    def aCheck(self):
        if checkIfAdmin() == False:
            dialog("Best used if Arcadia is run as Administrator", "User Not Administrator")

    def winBackup(self, ffold, tfold):
        #print("Running Backup")
        winstate = int(checkWindows())
        if winstate == 1:
            try:
                subprocess.Popen(shlex.split('xcopy "{0}" "{1}" /MEGHY'.format(ffold, tfold)))
                #self.monitorFileMove(process)
                dialog("Backup Complete.", "Backup Successful")
            except subprocess.CalledProcessError as e:
                self.xcopyWeird(e.returncode)
        elif winstate > 1 and winstate <= 6:
            try:
                subprocess.Popen('robocopy "{0}" "{1}" /e /z /R:1 /W:1 /xj /xf desktop.ini /MT:8'.format(ffold, tfold))
                #self.monitorFileMove(process)
                
                dialog("Backup Complete.", "Backup Successful")
            except subprocess.CalledProcessError as e:
                self.roboWeird(e.returncode)
        else:
            dialog("Unsupported Windows Version", "Unable to Copy")
        self.tbxFrom.setText("")
        self.tbxTo.setText("")


    def fileCounter(self, folder1):
        global filelist
        for root, dirs, files in os.walk(folder1):
            for name in files:
                if name != 'desktop.ini':
                    filelist.append(name)
            for name in dirs:
                self.fileCounter(name)
        


    #def folderCompare(self, folder1, folder2):
    # def testCounter(self):
    #     self.fileCounter(self.tbxFrom.text())
    #     dialog("There are {} files total.".format(len(filelist)), "Total Files")
    #     print(filelist)


    def xcopyWeird(self, ec):
        if ec == 1:
            dialog("No files were found to copy.", "Backup Successful")
        elif ec == 2:
            dialog("Xcopy process terminated.", "Backup Terminated")
        elif ec == 4:
            dialog("Not enough memory or disk space.", "Backup Failed")
        elif ec == 5:
            dialog("Disk Write Error Occurred.", "Backup Failed")


    def monitorFileMove(self, proc):
        #stdout = proc.communicate()[0]
        while True:
            output = proc.stdout.readline()
            if output == '' and proc.poll() is not None:
                break
            if output:    
                self.txtInfo.append(output.strip())
        #print('STDOUT:{}'.format(stdout))

    def roboWeird(self, ec):
        if ec == 1:
            dialog("Backup Completed Successfully", "Backup Successfull")
        elif ec == 2:
            dialog("Some files were skipped", "Backup Successfull")
        elif ec == 4:
            dialog("Mismatched files or directories detected. Check manually", "Backup Completed")
        elif ec == 8:
            dialog("Copy Errors Occurred and retry limit was exceeded. Some files/directories may have not been moved", "Backup May Have Failed")
        elif ec == 16:
            dialog("Serious Error. No files copied.", "Backup Failed")
        else:
            dialog("Unknown Error.", "Backup Probably Failed")

    def winDriverBackup(self, tfold, winver):
        driverLocations = ["%SystemRoot%\\Driver Cache\\i386\\drivers.cab", "%SystemRoot%\\Driver Cache\\i386\\service_pack.cab", "%windir%\\inf", "%SystemRoot%\\System32\\Drivers", "%SystemRoot%\\System32"]
        if winver != 1:
            try:
                subprocess.Popen("Export-WindowsDriver -Online -Destination {}".format(tfold))
            except:
                dialog("Unable to copy drivers. Attempting Robocopy Backup", "Switching to Robocopy")
                try:
                    for item in driverLocations:
                        subprocess.check_output('robocopy "{0}" "{1}" /MIR /xj /MT:8'.format(item, tfold))
                    dialog("Backup Finished", "Backup Completed")
                except subprocess.CalledProcessError as e:
                    self.roboWeird(e.returncode)
        else:
            for item in driverLocations:
                try:
                    subprocess.check_output('xcopy "{0}" "{1}" /MEGHY'.format(item, tfold))
                except subprocess.CalledProcessError as e:
                    self.xcopyWeird(e.returncode)
            
    def openDirDialog(self, ftype):
        d = QtWidgets.QFileDialog.getExistingDirectory(self, "Select a Directory", os.path.expanduser('~'))
        if ftype == 0:
            if d != '':
                self.tbxFrom.setText(d)
        elif ftype == 1:
            if d != '':
                self.tbxTo.setText(d)
        else:
            print("Hello World")

    def runBackup(self):
        ff = self.tbxFrom.text()
        tf = self.tbxTo.text()
        if ff != "" and ff != None and tf != '' and tf != None:
            if sys.platform == 'win32':
                self.winBackup(ff, tf)
            else:
                print("Not currently supported")

    def runDriverBackup(self):
        tf = self.tbxDriver.text()
        if sys.platform == 'win32':
            versions = {2: "Vista", 3: "7", 4: "8", 5: "8.1", 6: "10"}
            if tf != "" and tf != None:
                winstate = int(checkWindows())
                if winstate == 1:
                    dialog("Detected Windows XP. Using Xcopy", "XP Detected")
                elif winstate > 1 and winstate <= 6:
                    dialog("Detected Windows {}. Attempting to use Powershell Driver Backup", "Win {} Detected".format(versions[winstate]))
                else:
                    dialog("Unknown version of Windows", "Unable to Backup Drivers")
                self.winDriverBackup(tf, winstate)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ArcadiaPy()
    form.show()
    app.exec_()


"""
readProgramList()
Arguments:
    fileLoc: Location of XML file with stored application information
    biglist: QListbox that will be populated with the information from the XML file

Description:
Takes an XML file with the list of programs (either main or temporary), and a qlistbox widget
and populates the qlistbox widget with the names taken from xml file based on application category.

"""


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

    
"""
checkWindows()
Arguments: None

Description:
Determines what version of Windows is being run. Necessary for determining whether to run
robocopy (which is included with versions of Windows beyond XP) or xcopy. Also Could be
useful for other situations.

"""


def checkWindows():
    if sys.platform == "win32":
        ver = subprocess.getoutput('systeminfo | findstr /B /C:"OS Version"')
        ver = str(ver)
        #Check if Win XP
        if "5.1" in ver:
            return 1
        #Check if Win Vista
        elif "6.0" in ver:
            return 2
        #Check if Win 7
        elif "6.1" in ver:
            return 3
        #Check if Win 8
        elif "6.2" in ver:
            return 4
        #Check if Win 8.1
        elif "6.3" in ver:
            return 5
        #Check if Win 10
        elif "10.0" in ver:
            return 6
        else:
            return 0

"""
checkIfAdmin()
Arguments: None

Description:
Checks if the user has administrator access and returns true or false.

"""



def checkIfAdmin():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    return is_admin


"""
writeTempList()
Arguments:
    fileLoc: Location of XML file to parse
    cat: Category of application (Antivirus, Antimalware, Clean, Setup, Tool)
    name: Name of application
    des: Description of application
    loc: Application location on the disk (try to use generic location)
    link: Link to website of application developer or download location
    icon: Icon for application

Description:
Adds a new entry to the temporary XML file (temp.xml). Entry will not change the primary
program.xml file.


"""


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


"""
clearTempList()
Arguments: None
Description:
Clears out the temporary list so that it can be repopulated with
default values when the program editor widget opens.

"""


def clearTempList():
    for items in tempList:
        items.clear()


"""
dialog()
Arguments:
    text: Message that you want delivered with the dialog box
    title: Title of the dialog box
Description:
Easy implementation of a basic dialog box that simply delivers a message
and allows the user to click 'ok'

"""


def dialog(text, title):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()


"""
runProgram()
Arguments: None
Description:
Runs program determined by 'selectedLocation' global variable. Currently using subprocess.call([selectedLocation])
to run the program, but having trouble when running through visual studio code with anaconda as the subprocess
opens in a separate directory from the program file location. Using a specific location may be necessary, but would
require users to place all programs in a specific location. Working on a solution.

"""


def runProgram():
    try:
        if selectedLocation is not '':
            #os.system(selectedLocation)
            #subprocess is opening in appdata directory. May need to fix.
            #home = os.path.expanduser('~')
            #subprocess.Popen(["{0}\\Documents\\Arcadia 6\\{1}".format(home, selectedLocation)])
            subprocess.call([selectedLocation])
    except:
        dialog("Program Not Found at {}".format(selectedLocation), "Error") 

#Primary programs list
mainList = list((list(), list(), list(), list(), list()))
#Temporary programs list for user manipulation
tempList = list((list(), list(), list(), list(), list()))

filelist = list()

if __name__ == '__main__':

    readProgramList('Programs.xml', mainList)
    main()
