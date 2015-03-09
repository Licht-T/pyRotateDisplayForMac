import objc
import sys
from Foundation import *
from AppKit import *
from PyObjCTools import NibClassBuilder, AppHelper

import pyRotateDisplayAPIMac as dispAPI
import pyRotateDisplaySettingsMac as settingsWindow
import pyRotateDisplayArduinoAPI as arduinoAPI
import pyRotateDisplayStatusBar as statusBar

if __name__ == '__main__':
    import itertools, glob
    

    disp = dispAPI.Display()
    arduino = arduinoAPI.Arduino(disp.arduinoCallback, None)
    settings = settingsWindow.DisplaySelectWindow(sys.argv, disp, arduino)

    app = NSApplication.sharedApplication()
    delegate = statusBar.StatusBar.alloc().init()
    app.setDelegate_(delegate)
    delegate.setCallBack(settings.show)
    delegate.setQuitCallBack(arduino.stopAndClose)

    AppHelper.runEventLoop()
