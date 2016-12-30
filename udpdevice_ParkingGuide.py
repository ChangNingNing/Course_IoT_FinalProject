from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys
from udpwkpf_io_interface import *

import pyupm_lpd8806
nLED = 4
class ParkingGuide(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('ParkingGuide')
        mystrip = pyupm_lpd8806.LPD8806(nLED, 7)
        print "ParkingGuide init success"

    def update(self,obj,pID=None,val=None):
        try:
            valid = obj.getProperty(0)
            pattern = obj.getProperty(1)

            mystrip = pyupm_lpd8806.LPD8806(nLED, 7)
            mystrip.show()

            if (valid & 1)==0: # right
                color = pattern & 3
                if color == 0:
                    mystrip.setPixelColor(0, 0, 0, 0)
                elif color == 1:
                    mystrip.setPixelColor(0, 0, 10, 0)
                elif color == 2:
                    mystrip.setPixelColor(0, 0, 0, 10)
                elif color == 3:
                    mystrip.setPixelColor(0, 10, 0, 0)
            else:
                mystrip.setPixelColor(0, 0, 0, 0)
            if ((valid>>1) & 1)==0: # forward
                color = (pattern >> 2) & 3
                if color == 0:
                    mystrip.setPixelColor(1, 0, 0, 0)
                elif color == 1:
                    mystrip.setPixelColor(1, 0, 10, 0)
                elif color == 2:
                    mystrip.setPixelColor(1, 0, 0, 10)
                elif color == 3:
                    mystrip.setPixelColor(1, 10, 0, 0)
            else:
                mystrip.setPixelColor(1, 0, 0, 0)
            if ((valid>>2) & 1)==0: # left
                color = (pattern >> 4) & 3
                if color == 0:
                    mystrip.setPixelColor(2, 0, 0, 0)
                elif color == 1:
                    mystrip.setPixelColor(2, 0, 10, 0)
                elif color == 2:
                    mystrip.setPixelColor(2, 0, 0, 10)
                elif color == 3:
                    mystrip.setPixelColor(2, 10, 0, 0)
            else:
                mystrip.setPixelColor(2, 0, 0, 0)
            mystrip.show()
        except IOError:
            print ("Error")

class MyDevice(Device):
    def __init__(self,addr,localaddr):
        Device.__init__(self,addr,localaddr)

    def init(self):
        m = ParkingGuide()
        self.addClass(m,0)
        self.obj_parking_guide = self.addObject(m.ID)

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print 'python %s <gip> <dip>:<port>' % sys.argv[0]
        print '      <gip>: IP addrees of gateway'
        print '      <dip>: IP address of Python device'
        print '      <port>: An unique port number'
        print ' ex. python %s 192.168.4.7 127.0.0.1:3000' % sys.argv[0]
        sys.exit(-1)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()
    device_cleanup()

