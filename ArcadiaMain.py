from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.uic import loadUi
from shutil import copyfile
import PyQt5
import xml.etree.ElementTree as ET
import sys
import shlex
import time
import os, ctypes
import subprocess
import threading
import Arcadia6
import progEditor
import diaAddProg
import utilDialog
import importDialog


"""
ArcadiaPy()
Arguments:
    Form Initialization Arguments
Description:
Graphical interface for Arcadia 6. This application is a toolbox that enables users to store
and run various computer repair applications and utilities. The user has control over which
applications are available to them, can add and remove applications as they please. Also contains
some utilities built in that may be useful to the user.

Previous versions of this application were written in C# and designed to run only on Windows platforms,
but this version has been rewritten in python with Qt for the purpose of cross-compatibility with other
operating systems. The goal is also to make an application that is easy to run on any machine.
"""

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
    

    """
    ArcadiaPy::openEditor()
    Arguments:
        self: referring to parent class
    Description:
    Opens up the Program Editor so that the user can modify the applications present in the
    Arcadia 6 toolbox. Usually attached to btnEditor.
    """


    def openEditor(self):
        formEdit = EditorPy(self)
        formEdit.show()


    """
    ArcadiaPy::openUtil()
    Arguments:
        self: referring to parent class
    Description:
    Opens up the Utility Dialog box (UtilDialog) which allows the user to run certain utilities
    such as file and driver backup. Usually attached to btnUtilities.
    """


    def openUtil(self):
        util = UtilDialog(self)
        util.show()


    """
    ArcadiaPy::clearLists()
    Arguments:
        self: referring to parent class
    Description:
    Clears all the items from the list widgets.
    """

    def clearLists(self):
        self.lstWindows.clear()
        self.lstLinux.clear()
        self.lstMac.clear()

    """
    ArcadiaPy::keyPressEvent()
    Arguments:
        self: referring to parent class
        event: event that has taken place (in this case a keypress)
    Description:
    If enter key is pressed at any time while Arcadia6 main form is in focus, attempt to run
    whatever application is currently selected in the main list.
    """


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            runProgram()

    """
    ArcadiaPy::softwareList()
    Arguments:  
        self: referring to parent class
        category: Group that application belongs to (Antivirus, Antimalware, etc.)
    Description:
    Determines which applications appear on the list depending on the category button
    that is pressed.
    """


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

    """
    ArcadiaPy::popWinSoft()
    Arguments:
        self: referring to parent class
    Description:
    Populates the listbox for Windows software present in Arcadia 6. Uses "Programs.xml" to populate.
    Also shows the application's icon, displays a brief summary, shows the website for the application,
    and tells the user if the application is available to run or not.
    """


    def popWinSoft(self):
        global selectedLocation
        try:
            itemName = self.lstWindows.currentItem().text()
            root = ET.parse('Programs.xml').getroot()

            for item in root.findall('ns1:Item', namespace):
                if item.get('name') ==  itemName:
                    pix = PyQt5.QtGui.QPixmap(item.find('ns1:Icon', namespace).text)
                    self.iconImage.setPixmap(pix)
                    self.txtDescription.setText(item.find('ns1:Description', namespace).text)
                    selectedLocation = item.find('ns1:Location', namespace).text
                    if os.path.exists(selectedLocation) == False:
                        self.lblAvailable.setText("Unavailable")
                        self.lblAvailable.setStyleSheet("QLabel {background-color: red; color: white} QToolTip {background-color: white; color: black}")
                        self.lblAvailable.setToolTip("Program not available.")
                    else:
                        self.lblAvailable.setText("Available")
                        self.lblAvailable.setStyleSheet("QLabel {background-color: green; color: white} QToolTip{background-color: white; color: black}")
                        self.lblAvailable.setToolTip("Program Available")
                    if sys.platform == 'win32':
                        self.lblWebsite.setText('<a href="{}">Website</a>'.format(item.find('ns1:Link', namespace).text))
                    else:
                        self.lblWebsite.setDisabled
        except:
            pix = PyQt5.QtGui.QPixmap("Icons/Arcadia.ico")
            self.iconImage.setPixmap(pix)


"""
EditorPy()
Arguments:
    Dialog Definition
Description:
An Editor that allows the user to modify the list of applications present within the Arcadia toolbox.
"""

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
        self.resetList()
        self.btnChange.clicked.connect(self.changeEntry)
        self.btnImport.clicked.connect(self.impApps)
        self.btnBackup.clicked.connect(self.mainBackup)
        self.btnLoad.clicked.connect(self.loadList)
        self.btnReset.clicked.connect(self.resetList)


    """
    EditorPy::resetList()
    Arguments:
        self: referring to parent class
    Description:
    Completely resets the temp.xml, tempList, and lstMod, and resets the colors in lstMod and lstCurrent to white.
    """

    
    def resetList(self):
        clearTempList()
        copyfile('Programs.xml', 'temp.xml')
        readProgramList('temp.xml', tempList)
        self.refreshList()
        self.resetColors(self.lstCurrent)
        self.resetColors(self.lstMod)
        

    """
    EditorPy::resetColors
    Arguments:
        self: referring to parent class
        lname: list name
    Description: Goes through ever item in the list (lname) and sets the background color to white.
    """


    def resetColors(self, lname):
        for i in range(lname.count()):
            item = lname.item(i)
            item.setBackground(QtGui.QBrush(QtCore.Qt.white, QtCore.Qt.SolidPattern))

    
    """
    EditorPy::addEntry()
    Arguments:
        self: referring to parent class
    Description:
    Opens up the add program dialog (AddProg) so that the user can import information for an
    application to add to the main list.
    """


    def addEntry(self):
        changeList.clear()
        addDia = AddProg(self)
        addDia.show()
        self.refreshList()

    """
    EditorPy::impApps()
    Arguments:
        self: referring to parent class
    Description:
    Opens up the import dialog (ImpDialog) used to import a large group of applications automatically.
    Function is usually connected to btnImport.
    """


    def impApps(self):
        btnQuestion = QtWidgets.QMessageBox.question(self, "Proceed to Import", "This will remove unsaved changes. Continue?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if btnQuestion == QtWidgets.QMessageBox.Yes:
            iDia = ImpDialog(self)
            iDia.show()
    
    """
    EditorPy::loadList()
    Arguments:
        self: referring to parent class
    Description:
    Enables user to load an existing xml list of programs. Useful for reloading a backup list.
    """


    def loadList(self):
        btnQuestion = QtWidgets.QMessageBox.question(self, "Proceed to Load", "This will remove unsaved changes. Continue?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if btnQuestion == QtWidgets.QMessageBox.Yes:
            bac = QtWidgets.QFileDialog.getOpenFileName(self, "Load Existing List", "", "XML File (*.xml)")
            if bac[0] != "":
                try:
                    copyfile(bac[0], "temp.xml")
                except:
                    dialog("Unable to import file. Closing Editor.", "Unable to Import")
                    self.close()
                clearTempList()
                readProgramList('temp.xml', tempList)

    """
    EditorPy::changeEntry()
    Arguments:
        self: referring to parent class
    Description:
    Allows user to edit an entry selected in lstMod. Takes the name from lstMod, gets the
    information from temp.xml for that entry, and uses it to populate an AddProg dialog box.
    """


    def changeEntry(self):
        changeList.clear()
        cname = self.lstMod.selectedItems()
        if len(cname) > 0:
            cname = cname[0].text()
            readProgramList('temp.xml',None,cname)
            addDia = AddProg(self)
            addDia.show()
        else:
            dialog("No Entry Selected", "Nothing Selected")
        self.refreshList()


    """
    EditorPy::removeEntry()
    Arguments:
        self: referring to parent class
        n='': if name is specified, use that, otherwise keep blank
    Description:
    Can be used either with specific program name, or by taking the name of the selected
    lstMod item. It removes whatever program is specified from the temp.xml file and then
    refreshes the tempList and GUI (lstMod) to show the changes.
    """


    def removeEntry(self, n=''):
        if n == '' or n == False:
            name = self.lstMod.selectedItems()
            name = name[0].text()
        else: 
            name = n
        tree = ET.parse('temp.xml')
        root = tree.getroot()

        for item in root:
            if item.attrib["name"] == name:
                btnQuestion = QtWidgets.QMessageBox.question(self, "Removing Program", "This will remove the program. Continue?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if btnQuestion == QtWidgets.QMessageBox.Yes:
                    root.remove(item)

        tree.write("temp.xml")  
        self.refreshList()

    """
    EditorPy::mainBackup()
    Arguments:
        self: referring to parent
    Description:
    Creates backup of current application list in location designated by user. Uses copyfile to copy
    Programs.xml to another location.
    """

    
    def mainBackup(self):
        bac = QtWidgets.QFileDialog.getSaveFileName(self, "Backup Program List", "", "XML File (*.xml)")
        if bac[0] != '':
            copyfile('Programs.xml', bac[0])

    """
    EditorPy::showDiffs()
    Arguments:
        self: referring to parent class
        state: state of chkChanges (True or False)
    Description:
    Displays arrows and labels to show number of apps that are being removed and added. Also changes colors
    of added/removed entries in lstCurrent and lstMod so that the changed applications can
    be me easily identified.
    """


    def showDiffs(self, state):
        if state == QtCore.Qt.Checked:
            self.lblCurrentDiff.show()
            self.lblLeftArrow.show()
            self.lblModDiff.show()
            self.lblRightArrow.show()
            self.lblCurrentDiff.setText('0')
            self.lblModDiff.setText('0')
            longmain = list()
            longtemp = list()
            mint = 0
            tint = 0
            for tItem in tempList:
                for stItem in tItem:
                    
                    longtemp.append(stItem)
            for mItem in mainList:
                for smItem in mItem:
                    
                    longmain.append(smItem)
            for lm in longmain:
                if lm not in longtemp:
                    mint += 1
                    self.lblCurrentDiff.setText("-" + str(mint))
            for lt in longtemp:
                if lt not in longmain:
                    tint += 1
                    self.lblModDiff.setText("+" + str(tint))
                  

            self.colorChange(mainList, self.lstMod, self.lstCurrent, QtCore.Qt.red)
            self.colorChange(tempList, self.lstCurrent, self.lstMod, QtCore.Qt.green)
            
                         
        else:
            self.lblCurrentDiff.hide()
            self.lblLeftArrow.hide()
            self.lblModDiff.hide()
            self.lblRightArrow.hide()
            self.resetColors(self.lstCurrent)
            self.resetColors(self.lstMod)


    """
    EditorPy::colorChange()
    Arguments:
        self: referring to parent class
        l: takes in mainList or tempList
        w1: Widget 1, takes in qlistwidget
        w2: Widget 2, takes in qlistwidget
        c: Color that you want list item background color to be
    Description:
    Take each item from each category from each list item and uses it for comparison. Tests if
    the item matches an item in qlistwidget 1. If it does not match any entry, find the same
    entry in qlistwidget 2 and change the background color of that qlist item to 'c'. 
    """


    def colorChange(self, l, w1, w2, c):
        for zitem in l:
            for prog in zitem:
                it = w1.findItems(prog, QtCore.Qt.MatchExactly)
                if len(it) == 0:
                    w2.findItems(prog, QtCore.Qt.MatchExactly)[0].setBackground(QtGui.QBrush(c, QtCore.Qt.SolidPattern))
                

    """
    EditorPy::populateList()
    Arguments:
        self: referring to parent class
        wid: for passing the list widget that will be populated
        biglist: for passing the list that will be used to populate the widgets
    Description:
    Used for populating list widgets using mainList or tempList
    """


    def populateList(self, wid, biglist):
        wid.addItem("Antivirus:\n")
        wid.addItems(biglist[0])
        wid.addItem("\n\nAntimalware:\n")
        wid.addItems(biglist[1])
        wid.addItem("\n\nCleaning Tools:\n")
        wid.addItems(biglist[2])
        wid.addItem("\n\nSetup Tools:\n")
        wid.addItems(biglist[3])
        wid.addItem("\n\nRandom Tools:\n")
        wid.addItems(biglist[4])

    """
    EditorPy::refreshList()
    Arguments:
        self: referring to parent class
    Description:
    Clears the modified list box, clears the templist list, and repopulates both using temp.xml.
    It also refreshes showDiffs if chkChanges is checked. 
    """


    def refreshList(self):
        self.lstMod.clear()
        for item in tempList:
            item.clear()
        readProgramList('temp.xml', tempList)
        self.populateList(self.lstMod, tempList)
        if self.chkChanges.isChecked() == True:
            self.showDiffs(QtCore.Qt.Checked)

"""
AddProg()
Arguments:
    Dialog Definition
Description:
Dialog for entering information for adding and/or editing programs in the temporary list
"""
        

class AddProg(QtWidgets.QDialog, diaAddProg.Ui_diaAddProg):
    def __init__(self, parent=None):
        super(AddProg, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.buttonBox.accepted.connect(self.addProgramInfo)
        self.tbtnLocation.clicked.connect(lambda: self.openFileDialog(0))
        self.tbtnItemLocation.clicked.connect(lambda: self.openFileDialog(1))
        if len(changeList) > 0:
            self.tbxName.setText(changeList[0])
            self.tbxDescription.appendPlainText(changeList[2])
            self.tbxLocation.setText(changeList[3])
            self.tbxURL.setText(changeList[4])
            self.tbxItemLocation.setText(changeList[5])
            btnList1 = {self.rbnAntivirus, self.rbnAntimalware, self.rbnClean, self.rbnSetup, self.rbnTools}
            for btn in btnList1:
                if btn.text() == changeList[1]:
                    btn.setChecked(True)
        

    """
    AddProg::addProgramInfo()
    Arguments:
        self: referring back to parent class
    Description:
    Gets information from the AddProg form and uses it to create a new entry in the temporary
    xml file. It also checks to make sure the program does not already exist on the list.
    """


    def addProgramInfo(self):
        name = self.tbxName.text()
        loc = self.tbxLocation.text()
        desc = self.tbxDescription.toPlainText()
        ico = self.tbxItemLocation.text()
        web = self.tbxURL.text()
        rname =''
        ty = ''
        oss = ''
        #Message for checking if item already exists
        message = 'Name Exists Already'
        tboxes = {self.rbnAntimalware, self.rbnAntivirus, self.rbnClean, self.rbnSetup, self.rbnTools}
        for t in tboxes:
            if t.isChecked():
                ty = t.text()
        oboxes = {self.rbnLinux, self.rbnMac, self.rbnWindows}
        for o in oboxes:
            if o.isChecked():
                oss = o.text()
        changeList.clear()
        readProgramList('temp.xml', None, loc)
        #if location exists already set it for possible deletion
        if len(changeList) > 0:
            rname = changeList[0]
            message = "Location Exists Already"
            #if name exists also then same entry
            if rname == name:
                message = "Entry Exists Already"
        else:
            rname = name
        readProgramList('temp.xml', None, name)
        if len(changeList) > 0:
            btnQuestion = QtWidgets.QMessageBox.question(self, "Overwrite Entry", "{}, would you like to overwrite?".format(message), QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if btnQuestion == QtWidgets.QMessageBox.Yes:
                self.parent.removeEntry(rname)
                dialog("Adding updated item", "Updating")
                writeTempList('temp.xml', ty, name, desc, loc, web, ico)

        else:
            writeTempList('temp.xml', ty, name, desc, loc, web, ico)
        self.parent.refreshList()


    """
    AddProg::openFileDialog()
    Arguments:
        self: referring back to parent class
        ftype: determining which dialog to show
    Description:
    Opens dialog for finding a file depending on which button is clicked (tbnLocation or 
    tbnItemLocation) and determines where to put the resulting url (tbxlocation or 
    tbxItemLocation).
    """


    def openFileDialog(self, ftype):
        if ftype == 0:
            d = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select File", '',
            filter=('Windows Executable (*.exe);;Microsoft Installer (*.msi)'))[0]
            if d != '':
                self.tbxLocation.setText(d)
        else:
            d = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select File", '',
            filter=('PNG File (*.png);;JPEG/JPG (*.jpeg *.jpg)'))[0]
            if d != '':
                self.tbxItemLocation.setText(d)

"""
ImpDialog()
Arguments:
    Dialog Definitions
Description:
Enables user to easily import folder filled with executables to populate the tools list
in Arcadia 6. Files need to be organzied by type (Antivirus, Antimalware, Clean, Setup, Tools)
in subfolders of those names within the primary folder. User will have the option to append
the existing application list, or overwrite the existing list. 
"""


class ImpDialog(QtWidgets.QMainWindow, importDialog.Ui_frmImport):
    def __init__(self, parent=None):
        super(ImpDialog, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        clearTempList()
        copyfile('Programs.xml', 'temp.xml')
        readProgramList('temp.xml', tempList)
        self.txtInstructions.setText(self.instuctions)
        self.btnExit.clicked.connect(self.close)
        self.tbnImFolder.clicked.connect(self.openDirDialog)
        self.btnImport.clicked.connect(self.importEverything)

    #instructions for how to import. Stored here and presented in txtInstructions box
    instuctions = ("This is for importing many applications at once. Make sure that the "
                   "file structure is as follows:\n-Parent\n---Type(Antivirus, Antimalware, Clean, Setup, Tools)\n-----Files\n\nImport the parent directory. Not all "
                   "subdirectories are necessary, but the structure is.")
    

    """
    ImpDialog:openDirDialog()
    Arguments:
        self: referring back to parent class
    Description:
    Opens dialog for finding folder to import from.
    """


    def openDirDialog(self):
        d = QtWidgets.QFileDialog.getExistingDirectory(self, "Select a Directory", '')
        self.tbxImFolder.setText(d)
    

    """
    ImpDialog:importEverything()
    Arguments:
        self: referring back to parent class
    Description:
    Code for importing folders full of application executables. Creating an xml file
    with the information about the applications, allowing the applications to be organized
    and run from Arcadia 6.
    """

    def importEverything(self):
        importFolder = self.tbxImFolder.text()
        av = importFolder + "/Antivirus"
        am = importFolder + "/Antimalware"
        cl = importFolder + "/Clean"
        st = importFolder + "/Setup"
        tl = importFolder + "/Tools"
        checkList = {av: "Antivirus", am: "Antimalware", cl: "Clean", st: "Setup", tl: "Tools"}
        filelist = list()
        if os.path.isdir(importFolder):
            for ci in checkList:
                if os.path.isdir(ci):
                    filelist = os.listdir(ci)
                    for item in filelist:
                        fname, fext = os.path.splitext(item)
                        readProgramList('temp.xml',None, fname)
                        if fext == '.exe' or fext == '.msi':
                            if len(changeList) > 0:
                                writeTempList('temp.xml', checkList[ci], fname, " ", ci + "/" + item, "www.google.com", "")
                            else:
                                dialog("Name already exists", "Name Already Exists")
                else:
                    dialog("Directory " + ci + " does not exist", "No Directory")
        else:
            dialog("Directory does not exist", "No Directory")
                


"""
UtilDialog()
Arguments:
    Dialog Defintions
Description:
Utilities that users may find useful. So far contains file backup (using robocopy, xcopy
or rsync depending on OS) and driver backup(for Windows operating systems XP+)
"""



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
        self.tbnDriver.clicked.connect(lambda: self.openDirDialog(2))
        self.btnTest.clicked.connect(self.testCounter)


    """
    UtilDialog:aCheck()
    Arguments:
        self: referring back to parent class
    Description:
    Checks if the user has administrative privilages.
    """


    def aCheck(self):
        if checkIfAdmin() == False:
            dialog("Best used if Arcadia is run as Administrator", "User Not Administrator")


    """
    UtilDialog:WinBackup()
    Arguments:
        self: referring back to parent class
        ffold: From Folder, folder where the files to be moved are located
        tfold: To folder, folder where you want the files moved
    Description:
    Determines which version of Windows is being used and runs copy commands based on the OS.
    Windows XP uses XCopy, as robocopy is not installed by default. Newer versions of Windows
    use Robocopy. Windows operating systems older than XP are not supported.
    """


    def winBackup(self, ffold, tfold):
        winstate = int(checkWindows())
        if winstate == 1:
            try:
                subprocess.Popen('xcopy "{0}" "{1}" /MEGHY'.format(ffold, tfold))
                self.lblStatus.setText("Status: Backup Complete")
            except subprocess.CalledProcessError as e:
                self.xcopyWeird(e.returncode)
        elif winstate > 1 and winstate <= 6:
            try:
                subprocess.Popen('robocopy "{0}" "{1}" /e /z /R:1 /W:1 /xj /xf desktop.ini /MT:8'.format(ffold, tfold))
                self.lblStatus.setText("Status: Backup Complete")
            except subprocess.CalledProcessError as e:
                self.roboWeird(e.returncode)
        else:
            self.lblStatus.setText("Status: Unsupported Windows Version")
        self.tbxFrom.setText("")
        self.tbxTo.setText("")


    """
    UtilDialog::fileCounter()
    Arguments:
        self: referring back to parent class
        folder1: location of files that will be counted

    Description:
    Goes through a folder and creates a list of the filenames present within. Ignores 'desktop.ini' as that will not be
    copied over in the file backup process.
    """

    def fileCounter(self, folder1):
        global filelist
        for root, dirs, files in os.walk(folder1):
            for name in files:
                if name != 'desktop.ini':
                    filelist.append(name)
            for name in dirs:
                self.fileCounter(name)
        


    #def folderCompare(self, folder1, folder2):
    def testCounter(self):
        self.fileCounter(self.tbxFrom.text())
        dialog("There are {} files total.".format(len(filelist)), "Total Files")
        print(filelist)

    """
    UtilDialog::xcopyWeird()
    Arguments:
        self: referring back to parent class
        ec: The thrown return code from xcopy
    Description:
    Xcopy throws return codes (picked up as error codes by exception handling) in order to show what happened
    during file transfer. Once the exceptions are thrown, this list parses it to determine what really happened.
    """

    def xcopyWeird(self, ec):
        if ec == 1:
            self.dialog("No files were found to copy.", "Backup Successful")
        elif ec == 2:
            self.dialog("Xcopy process terminated.", "Backup Terminated")
        elif ec == 4:
            self.dialog("Not enough memory or disk space.", "Backup Failed")
        elif ec == 5:
            self.dialog("Disk Write Error Occurred.", "Backup Failed")


    """
    UtilDialog::monitorFileMove()
    Arguments:
        self: referring back to parent class
        loc1: initial 'from' folder location
        loc2: 'to' folderlocation that will be monitored
        total: total number of files that should be present in the 'to' folder once completed

    Description:
    Continuously monitors 'to' folder to see when file transfer has been completed. Takes number of 
    files in folder and divides by total to find percentage of completion. Uses percentage to
    update the progress bar (pbrfiles). Function is designed to run in its own thread.
    """

    def monitorFileMove(self, loc1, loc2, total):
        x = True
        while x == True:
            filelist.clear()
            self.fileCounter(loc2)
            now = len(filelist)
            try:
                percent = (total / now) * 100
            except ZeroDivisionError:
                percent = 0
            self.lblStatus.setText("Status: {}%".format(percent))
            self.pbrFiles.setValue(percent)
            if percent == 100:
                x = False
            #time.sleep(.05)



    """
    UtilDialog::roboWeird()
    Arguments:
        self: referring back to parent class
        ec: The thrown return code from robocopy
    Description:
    Robocopy throws return codes (picked up as error codes by exception handling) in order to show what happened
    during file transfer. Once the exceptions are thrown, this list parses it to determine what really happened.
    """

    def roboWeird(self, ec):
        if ec == 1:
            self.lblStatus.setText("Status: Backup Completed Successfully")
        elif ec == 2:
            self.lblStatus.setText("Status: Some files were skipped")
        elif ec == 4:
            self.lblStatus.setText("Status: Mismatched files or directories detected. Check manually")
        elif ec == 8:
            self.lblStatus.setText("Status: Copy Errors Occurred and retry limit was exceeded")
        elif ec == 16:
            self.lblStatus.setText("Status: Serious Error. No files copied.")
        else:
            self.lblStatus.setText("Status: Unknown Error")


    """
    UtilDialog::winDriverBackup()
    Arguments:
        self: referring back to parent class
        tfold: "To Folder", or where the drivers will end up
        winver: Version of Windows that the process will be running on
    Description:
    Determines version of Windows. If Windows version is XP then skips to using xcopy to transfer the files from default
    locations listed in driverLocations list. If newer than XP (Vista or later) attempts to run powershell commands first
    for easier backup. If that fails it proceeds to use robocopy on the driverLocations.
    """


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

    """
    UtilDialog::openDirDialog()
    Arguments:
        self: referring back to parent class
        ftype: Determining which button was pressed (tbnFrom or tbnTo)
    Description:
    Opens a QFileDialog so that the user can select directories for the "From" and "To" locations for the
    file backup. tbxFrom or tbxTo are then populated based on the result.
    """


    def openDirDialog(self, ftype):
        d = QtWidgets.QFileDialog.getExistingDirectory(self, "Select a Directory", os.path.expanduser('~'))
        if ftype == 0:
            if d != '':
                self.tbxFrom.setText(d)
        elif ftype == 1:
            if d != '':
                self.tbxTo.setText(d)
        elif ftype == 2:
            if d != '':
                self.tbxDriver.setText(d)
        else:
            print("Hello World")



    """
    UtilDialog::runBackup()
    Arguments:
        self: referring back to parent class
    Description:
    Makes sure that tbxFrom and tbxTo listboxes in UtilDialog are populated.
    Determines which operating system is being run.
    Runs backup function based upon current operating system.
    """


    def runBackup(self):
        ff = self.tbxFrom.text()
        tf = self.tbxTo.text()
        if ff != "" and ff != None and tf != '' and tf != None:
            if sys.platform == 'win32':
                filelist.clear()
                self.fileCounter(ff)
                inisize = len(filelist)
                filelist.clear()
                self.fileCounter(tf)
                fromsize = len(filelist)
                newtotal = inisize + fromsize
                t = threading.Thread(target=lambda: self.winBackup(ff, tf))
                t2 = threading.Thread(target=lambda: self.monitorFileMove(ff, tf, newtotal))
                t.daemon = True
                t2.daemon = True
                t.start()
                t2.start()
                t.join()
                t2.join()
            else:
                print("Not currently supported")

    """
    UtilDialog::runDriverBackup()
    Arguments:
        self: referring back to parent class
    
    Description:
    Determines which version of Windows is being run.
    Makes sure that the tbxDriver listbox in the Utiliy dialog is populated.
    Runs function to back up drivers from Windows system files.

    """

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


def readProgramList(fileLoc, biglist=None, search=""):
    changeList.clear()
    root = ET.parse(fileLoc).getroot()
    for item in root.findall('ns1:Item', namespace):
        if search == "" and biglist != None:
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
        else:
            if item.get('name') == search or item.find('ns1:Location', namespace).text == search:
                changeList.append(item.get('name'))
                changeList.append(item.get('cat'))
                changeList.append(item.find('ns1:Description', namespace).text)
                changeList.append(item.find('ns1:Location', namespace).text)
                changeList.append(item.find('ns1:Link', namespace).text)
                changeList.append(item.find('ns1:Icon', namespace).text)
            #changelist[0] = name, [1] = category, [2] = Description, [3] = Location
            #[4] = Link, [5] = Icon
                

    
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
    new_item = ET.SubElement(root, 'ns0:Item', attrib={"cat": cat, "name": name})
    new_item_des = ET.SubElement(new_item, 'ns0:Description')
    new_item_loc = ET.SubElement(new_item, 'ns0:Location')
    new_item_link = ET.SubElement(new_item, 'ns0:Link')
    new_item_icon = ET.SubElement(new_item, 'ns0:Icon')

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
Runs program determined by 'selectedLocation' global variable. Currently using subprocess.call([sys.path[0] + / + selectedlocation])


"""


def runProgram():
    try:
        if selectedLocation is not '':
    
            subprocess.call([sys.path[0] + "/" + selectedLocation])
    
    except:
        dialog("Program Not Found at {}".format(selectedLocation), "Error") 

#Primary programs list
mainList = list((list(), list(), list(), list(), list()))
#Temporary programs list for user manipulation
tempList = list((list(), list(), list(), list(), list()))

filelist = list()

namespace = {"ns1": "http://harlocktech.com/Arcadia6"}
#hold program information for the Program Editor change function
changeList = list()

if __name__ == '__main__':

    readProgramList('Programs.xml', mainList)
    main()
