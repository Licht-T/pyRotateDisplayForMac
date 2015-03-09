import re
import collections

# import numpy as np

from Foundation import *
from AppKit import *
from Quartz import *
from CoreFoundation import *
import objc

with open("iokit.metadata","r",encoding="utf-8") as cont:
    IOKIT_XML = cont.read()
objc.parseBridgeSupport(IOKIT_XML, globals(), objc.pathForFramework("/System/Library/Frameworks/IOKit.framework"))

with open("iodisp.metadata","r",encoding="utf-8") as cont:
    IODISP_XML = cont.read()
objc.parseBridgeSupport(IODISP_XML, globals(), objc.pathForFramework("/System/Library/Frameworks/IOKit.framework"))


def inner(lhs,rhs):
    return lhs[0]*rhs[0]+lhs[1]*rhs[1]

def cross(lhs,rhs):
    return lhs[0]*rhs[1]-lhs[1]*rhs[0]

def NSRectToDict(rect):
    return {"origin":[rect.origin.x,rect.origin.y],\
            "size":[int(rect.size.width),int(rect.size.height)]}

class Display:
    def __init__(self):
        self.deviceList = self.getDeviceList()
        self.selected = 0
        self.currentVec=None
        self.oriList = [{"str":"0.0","val":kIOScaleRotate0},{"str":"90.0","val":kIOScaleRotate90},{"str":"180.0","val":kIOScaleRotate180},{"str":"270.0","val":kIOScaleRotate270}]
        self.orientation = collections.deque(self.oriList)

    def getDeviceList(self):
        self.deviceList = []
        screens = NSScreen.screens()
        dics=[]
        # sortl = []
        for screen in screens:
            rect = NSRectToDict(screen.frame())
            d = screen.deviceDescription()
            no = d.valueForKey_("NSScreenNumber")
            dics.append({"NO":no,"Rect":rect})
            # sortl.append((rect["origin"][0],rect["origin"][1]))

        # sortl = np.array(sortl)
        # ind = np.lexsort((sortl[:,0],sortl[:,1]))

        for d in dics:
            no = d["NO"]
            rect = d["Rect"]
            deviceDict = IODisplayCreateInfoDictionary(CGDisplayIOServicePort(no),0)
            dispName = deviceDict.objectForKey_("DisplayProductName").objectForKey_("id")
            dic = { "NO":no, \
                    "DevStr": dispName, \
                    "DevName":str(rect["size"][0])+"x"+str(rect["size"][1]) \
                    }
            self.deviceList.append(dic)
        return self.deviceList

    def getOrientation(self,i):
        oris = str(CGDisplayRotation(i))
        for ori in self.oriList:
            if ori["str"]==oris:
                return ori["val"]
        return str(CGDisplayRotation(i))

    def arduinoCallback(self,s):
        ori = self.getOrientation(self.selected)
        while ori!=self.orientation[0]["val"]:
            self.orientation.rotate(1)
        print("currnet:"+str(self.orientation[0]))
        match = re.compile(r'{.*?}').match(s)
        print(s)
        if match:
            s=s.replace("{","").replace("}","").split(",")
            v=[int(s[0])-340,int(s[1])-340]
            if self.currentVec==None:
                self.currentVec = v

            p=inner(v,self.currentVec)
            print(p)
            if abs(p)<500:
                print("rot!")
                cr=cross(v,self.currentVec)
                print(cr)
                if cr>0:
                    self.orientation.rotate(-1)
                    print("next:"+str(self.orientation[0]))
                    self.rotate(self.orientation[0]["val"])
                else:
                    self.orientation.rotate(1)
                    print("next:"+str(self.orientation[0]))
                    self.rotate(self.orientation[0]["val"])
                self.currentVec = v


    def rotate(self,ori):
        service = CGDisplayIOServicePort(self.selected)
        options = (0x00000400 | (ori)  << 16)
        IOServiceRequestProbe(service, options)
