from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys

class Light_Agent(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('Light_Agent')
        print "Light Agent init success"
    def update(self,obj,pID,val):
        if pID >= 0 and pID <= 5:
            R_left = obj.getProperty(0)
            R_forward = obj.getProperty(1)
            R_right = obj.getProperty(2)
            I_left = obj.getProperty(3)
            I_forward = obj.getProperty(4)
            I_right = obj.getProperty(5)
            pattern = 0
            state = 4

            value = 0
            if R_left > 0:
                value = 1
                pattern |= (1 << 4)
            else:
                if I_left == 1 or I_left == 2:
                    value = I_left + 1
                    pattern |= (value << 4)
            if value != 0 and value < state:
                state = value

            value = 0
            if R_forward > 0:
                value = 1
                pattern |= (1 << 2)
            else:
                if I_forward == 1 or I_forward == 2:
                    value = I_forward + 1
                    pattern |= (value << 2)
            if value != 0 and value < state:
                state = value
     
            value = 0
            if R_right > 0:
                value = 1
                pattern |= 1
            else:
                if I_right == 1 or I_right == 2:
                    value = I_right + 1
                    pattern |= value
            if value != 0 and value < state:
                state = value
            if state == 4:
                state = 0

            print "pattern = ", pattern
            print "state = ", state
            obj.setProperty(6, pattern)
            obj.setProperty(7, state)
 
if __name__ == "__main__":
    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
            cls = Light_Agent()
            self.addClass(cls, self.FLAG_VIRTUAL)
            self.obj_light_agent = self.addObject(cls.ID)

    if len(sys.argv) <= 2:
        print 'python %s <gip> <dip>:<port>' % sys.argv[0]
        print '      <gip>: IP addrees of gateway'
        print '      <dip>: IP address of Python device'
        print '      <port>: An unique port number'
        print ' ex. python %s 192.168.4.7 127.0.0.1:3000' % sys.argv[0]
        sys.exit(-1)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()
