from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys
from udpwkpf_io_interface import *

ParkingSpot_Pin = 2
class ParkingSpot(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('ParkingSpot')
        self.button_gpio = pin_mode(ParkingSpot_Pin, PIN_TYPE_DIGITAL, PIN_MODE_INPUT)
        print "ParkingSpot init success"

    def update(self,obj,pID=None,val=None):
        try:
            isPress = obj.getProperty(0)
            if isPress==0 and digital_read(self.button_gpio):
                obj.setProperty(0, isPress+1)
                print "ParkingSpot pin: ", ParkingSpot_Pin, ", value: ", isPress
            elif isPress and digital_read(self.button_gpio)==0:
                obj.setProperty(0, 0)
                print "ParkingSpot pin: ", ParkingSpot_Pin, ", value: ", isPress
        except IOError:
            print "Error"

class MyDevice(Device):
    def __init__(self,addr,localaddr):
        Device.__init__(self,addr,localaddr)

    def init(self):
        m = ParkingSpot()
        self.addClass(m,0)
        self.obj_parking_spot = self.addObject(m.ID)

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

