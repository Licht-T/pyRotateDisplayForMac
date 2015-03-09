# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyRotateDisplay.ui'
#
# Created: Wed Nov 26 17:10:48 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets

import syslog
import threading

syslog.openlog("pyRotateDisplay")

_translate = QtCore.QCoreApplication.translate

kIOScaleRotate0=0
kIOScaleRotate180=96
kIOScaleRotate270=80
kIOScaleRotate90=48

class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self._want_to_close = False

    def closeEvent(self, evnt):
        if self._want_to_close:
            super(MyDialog, self).closeEvent(evnt)
        else:
            evnt.ignore()

class Ui_Dialog(QtCore.QThread):
    failedConnectSignal = QtCore.pyqtSignal()
    failedReconnectSignal = QtCore.pyqtSignal()
    def __init__(self, disp, ard,th):
        syslog.syslog(syslog.LOG_ALERT, "UI init")
        super(Ui_Dialog, self).__init__(None)
        self.moveToThread(th)
        self.hide = True
        self.displayMode = "test"
        self.Dialog = None
        self.display = disp
        self.arduino = ard
        self.arduino.callBackFail = self.reconnect

        self.failedConnectSignal.connect(self.failed_connect)
        self.failedReconnectSignal.connect(self.failed_reconnect)
        syslog.syslog(syslog.LOG_ALERT, "UI end")


    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(402, 163)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(50, 130, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 114))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.displayLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.displayLabel.setObjectName("displayLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.displayLabel)
        self.displayComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.displayComboBox.setObjectName("displayComboBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.displayComboBox)
        self.currentModeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.currentModeLabel.setObjectName("currentModeLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.currentModeLabel)
        self.currentModeLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.currentModeLineEdit.setEnabled(False)
        self.currentModeLineEdit.setText("")
        self.currentModeLineEdit.setReadOnly(False)
        self.currentModeLineEdit.setObjectName("currentModeLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.currentModeLineEdit)
        self.comPortLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.comPortLabel.setObjectName("comPortLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.comPortLabel)
        self.handShakeLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.handShakeLabel.setObjectName("handShakeLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.handShakeLabel)
        self.handShakeLineEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.handShakeLineEdit.setObjectName("handShakeLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.handShakeLineEdit)
        self.comPortComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.comPortComboBox.setObjectName("comPortComboBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.comPortComboBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.displayComboBox.activated['int'].connect(self.displayComboChanged)
        self.comPortComboBox.activated['int'].connect(self.comComboChanged)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.Dialog = Dialog
        self.refreshDisplayCombo()
        self.refreshCOMCombo()

    def retranslateUi(self, Dialog):
        # _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "pyRotateDisplay Settings"))
        self.displayLabel.setText(_translate("Dialog", "Display:"))
        self.currentModeLabel.setText(_translate("Dialog", "CurrentMode:"))
        self.comPortLabel.setText(_translate("Dialog", "COM Port:"))
        self.handShakeLabel.setText(_translate("Dialog", "HandShake:"))

    def refreshDisplayCombo(self):
        selected = self.display.selected

        self.displayComboBox.clear()
        devList = self.display.getDeviceList()
        devList = list(map(lambda dic : \
                        "[{NO}] {DevStr} ({DevName})".format(**dic),
                        devList))
        self.displayComboBox.addItems(devList)

        i=0
        for i in range(len(self.display.deviceList)):
            if selected==self.display.deviceList[i]["NO"]:
                break
        if i in range(len(self.display.deviceList)):
            self.displayComboBox.setCurrentIndex(i)
            self.displayComboChanged(i)
            self.display.selected = i
            print("non zero")
        else:
            print("zero")
            self.displayComboChanged(0)
            self.display.selected = 0

    def refreshCOMCombo(self):
        selected = self.arduino.ports[self.arduino.selected]

        self.comPortComboBox.clear()
        ports = self.arduino.getCOMPorts()
        self.comPortComboBox.addItems(ports)
        if selected in ports:
            self.comPortComboBox.setCurrentIndex(ports.index(selected))
            self.comComboChanged(ports.index(selected))
            self.arduino.selected = ports.index(selected)
        else:
            self.comComboChanged(0)
            self.arduino.selected = 0

    def displayComboChanged(self, i):
        print("changed to {index}!".format(index=i))
        ori = self.display.getOrientation(self.display.deviceList[i]["NO"])
        self.changeOrientationText(ori)

    def comComboChanged(self, i):
        print("changed to {index}!".format(index=i))
        print(str(self.comPortComboBox.currentText()))

    def setButtonsEnabled(self,flag):
        for button in self.buttonBox.buttons():
            button.setEnabled(flag)

    def setInputsEnabled(self,flag):
        self.displayComboBox.setEnabled(flag)
        self.comPortComboBox.setEnabled(flag)
        self.handShakeLineEdit.setEnabled(flag)

    def failed_connect(self):
        self.hide = False
        self.Dialog.setWindowTitle(_translate("Dialog", "pyRotateDisplay Settings", None))
        QtWidgets.QMessageBox.warning(
                self.Dialog,
                "Failed to connect Arduino.",
                "Invalid COM Port or Handshake message."
            )
        self.refreshDisplayCombo()
        self.refreshCOMCombo()
        for button in self.buttonBox.buttons():
            if "Disconnect"==str(button.text()):
                button.setText("OK")
        self.Dialog.show()

    def failed_reconnect(self):
        self.handshake()

    def handshake(self):
        self.setInputsEnabled(False)
        self.setButtonsEnabled(False)
        self.arduino.stopAndClose()
        self.arduino.initSerial()
        self.display.currentVec = None
        if self.arduino.handShake(str(self.handShakeLineEdit.text())):
            self.Dialog.setWindowTitle(_translate("Dialog", "pyRotateDisplay Settings (Connected!)", None))
            self.ide = True
            self.Dialog.hide()
            self.arduino.start()
            for button in self.buttonBox.buttons():
                if "OK"==str(button.text()):
                    button.setText("Disconnect")
        else:
            self.failedConnectSignal.emit()
            self.setInputsEnabled(True)
        self.setButtonsEnabled(True)

    def reconnect(self):
        self.failedReconnectSignal.emit()

    def accept(self):
        print("accepted!")
        if str(self.handShakeLineEdit.text())=="":
            QtWidgets.QMessageBox.warning(
                self.Dialog,
                "HandShake string empty.",
                "Put HandShake string."
            )
        elif not self.arduino.connected:
            self.display.selected = \
                    self.display.deviceList[self.displayComboBox.currentIndex()]["NO"]
            self.arduino.selected = self.comPortComboBox.currentIndex()
            self.Dialog.setWindowTitle(_translate("Dialog", "pyRotateDisplay Settings (Connecting...)", None))
            # self.arduino.stop()
            # self.arduino.close()
            t = threading.Thread(target=self.handshake)
            t.start()
        else:
            self.setButtonsEnabled(False)
            self.arduino.stopAndClose()
            self.refreshDisplayCombo()
            self.refreshCOMCombo()
            self.Dialog.setWindowTitle(_translate("Dialog", "pyRotateDisplay Settings", None))
            for button in self.buttonBox.buttons():
                if "Disconnect"==str(button.text()):
                    button.setText("OK")
            self.setInputsEnabled(True)
            self.setButtonsEnabled(True)

    def reject(self):
        print("rejected!")
        self.hide = True
        self.Dialog.hide()

    def changeOrientationText(self, ori):
        if ori==kIOScaleRotate0:
            print("Default orientation.")
            self.currentModeLineEdit.setText("Horizontal Orientatin(0 deg)")
        elif ori==kIOScaleRotate90:
            print("90 orientation")
            self.currentModeLineEdit.setText("Vertical Orientatin(90 deg)")
        elif ori==kIOScaleRotate180:
            print("180 orientation")
            self.currentModeLineEdit.setText("Horizontal Orientatin(180 deg)")
        elif ori==kIOScaleRotate270:
            print("270 orientation")
            self.currentModeLineEdit.setText("Vertical Orientatin(270 deg)")


class DisplaySelectWindow:
    mainThread = QtCore.QThread.currentThread()
    def __init__(self, args, disp, ard):
        syslog.syslog(syslog.LOG_ALERT, "Window init")

        syslog.syslog(syslog.LOG_ALERT, str(args))
        self.app = QtWidgets.QApplication(args)
        syslog.syslog(syslog.LOG_ALERT, "Qapp init")
        QtWidgets.QApplication.addLibraryPath(QtWidgets.QApplication.applicationDirPath()+"/../Frameworks")
        Dialog = MyDialog()
        Dialog.setWindowFlags(Dialog.windowFlags() & QtCore.Qt.WindowCloseButtonHint)
        self.ui = Ui_Dialog(disp,ard,self.mainThread)
        self.ui.setupUi(Dialog)
        syslog.syslog(syslog.LOG_ALERT, "Window end")

    def show(self):
        # if self.ui.hide:
        #     if not self.ui.arduino.connected:
        #         self.ui.refreshDisplayCombo()
        #         self.ui.refreshCOMCombo()
        #     self.ui.Dialog.show()
        #     self.ui.hide = False
        if not self.ui.arduino.connected:
            self.ui.refreshDisplayCombo()
            self.ui.refreshCOMCombo()
        self.ui.Dialog.show()
        self.ui.hide = False

    def hide(self):
        # if not self.ui.hide:
        #     self.ui.Dialog.hide()
        #     self.ui.hide = True
        self.ui.Dialog.hide()
        self.ui.hide = True



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

