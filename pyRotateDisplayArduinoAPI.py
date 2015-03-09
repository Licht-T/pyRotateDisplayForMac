import sys
import glob
import serial
import time, threading

class SerialThread(threading.Thread):
    def __init__(self, s, t, cb, cb_fail):
        super(SerialThread, self).__init__()
        self.t = t
        self.callBack = cb
        self.callBackFail = cb_fail
        self.ser = s
        self.stop = False

    def run(self):
        # self.ser.flushInput()
        # self.ser.flushOutput()
        try:
            while not self.stop:
                print("theread run")
                s=""
                count=0
                while s=="":
                    s = readline(self.ser)
                    time.sleep(self.t)
                    count=count+1
                    if count>10:
                        self.ser.write(b"2")
                        self.stop = True
                        self.callBackFail()
                        return
                self.callBack(s)
        except (OSError, serial.SerialException):
            self.stop = True
            self.callBackFail()
            return

def readline(ser):
    return ser.readline().decode("ascii").replace("\n","").replace("\r","")

def serial_ports():
    ports = ['COM' + str(i + 1) for i in range(256)]
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class Arduino:
    def __init__(self, cb, cb_fail):
        self.callBack=cb
        self.callBackFail = cb_fail
        self.ser = None
        self.thread = None
        self.connected = False
        self.ports = self.getCOMPorts()
        self.selected = 0

    def __del__(self):
        print("del")
        if self.ser!=None:
            self.ser.write(b"2")
            time.sleep(1)
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.close()
        if self.thread!=None:
            self.stop()

    def getCOMPorts(self):
        if sys.platform.startswith('win'):
            ports = ['COM' + str(i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        # ports = ['COM' + str(i + 1) for i in range(256)]
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        self.ports = result
        return self.ports

    def initSerial(self):
        self.ser = serial.Serial(self.ports[self.selected], 9600, timeout=0)

    def handShake(self,s):
        zero = time.time()
        while True:
            try:
                self.ser.write(b"0")
                time.sleep(1)
                cb = readline(self.ser)
                print(cb)
                if s==cb:
                    self.ser.flushInput()
                    self.ser.flushOutput()
                    self.ser.write(b"1")
                    time.sleep(1)
                    if "ok"==readline(self.ser):
                        print("Handshaked")
                        self.connected = True
                        return True
            except serial.SerialTimeoutException:
                print('Data could not be read')
                self.close()
                return False
            if time.time()-zero>10:
                break
        self.close()
        return False

    def start(self):
        self.thread = SerialThread(self.ser, 1, self.callBack, self.callBackFail)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.thread.start()

    def stop(self):
        if self.thread!=None:
            if self.thread.stop!=True:
                self.thread.stop = True
                self.thread.join()
            self.thread=None

    def close(self):
        self.connected = False
        if self.ser!=None:
            self.ser.write(b"2")
            time.sleep(1)
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.flush()
            self.ser.close()
        self.ser=None

    def stopAndClose(self):
        self.stop()
        self.close()

if __name__ == '__main__':
    ports = serial_ports()
    def test(a): print(a)
    def fail(): print("fail")
    a = Arduino(test,fail)
    print(ports[-1])
    a.initSerial(ports[-1])
    print(a.handShake("foobar"))
    a.start()
    time.sleep(20)
    a.stop()
