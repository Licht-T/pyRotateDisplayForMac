import objc
from Foundation import *
from AppKit import *
from PyObjCTools import NibClassBuilder, AppHelper

class StatusBar(NSObject):
    def setFront(self):
        NSRunningApplication.currentApplication_().activateWithOptions_(NSApplicationActivateIgnoringOtherApps)

    def applicationDidFinishLaunching_(self, notification):
        self.statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = self.statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        self.image = NSImage.alloc().initByReferencingFile_('Logo.png')
        self.statusitem.setImage_(self.image)
        self.statusitem.setHighlightMode_(1)
        self.statusitem.setToolTip_('pyRotateDisplay')
        self.menu = NSMenu.alloc().init()
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Settings', 'settings:', '')
        self.menu.addItem_(menuitem)
        menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
        self.menu.addItem_(menuitem)
        self.statusitem.setMenu_(self.menu)

    def applicationWillTerminate_(self, notification):
        self.quitCallBack()

    def setCallBack(self,cb):
        self.callback = cb

    def setQuitCallBack(self,cb):
        self.quitCallBack = cb

    def settings_(self, notification):
        self.callback()

if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = StatusBar.alloc().init()
    app.setDelegate_(delegate)
    AppHelper.runEventLoop()

