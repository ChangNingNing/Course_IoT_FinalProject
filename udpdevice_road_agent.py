from twisted.internet import reactor
from udpwkpf import WuClass, Device
import sys

class Road_Agent(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('Road_Agent')
        print "Road Agent init success"
    def update(self,obj,pID,val):
        if pID == 0:
            trigger = obj.getProperty(0)
            nValid = obj.getProperty(1)
            if trigger == True:
                nValid += 1
            else:
                nValid -= 1
            print "Road Agent nValid :", nValid
            obj.setProperty(1, nValid)
 
if __name__ == "__main__":
    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
            cls = Road_Agent()
            self.addClass(cls, self.FLAG_VIRTUAL)
            self.obj_road_agent = self.addObject(cls.ID)

    if len(sys.argv) <= 2:
        print 'python %s <gip> <dip>:<port>' % sys.argv[0]
        print '      <gip>: IP addrees of gateway'
        print '      <dip>: IP address of Python device'
        print '      <port>: An unique port number'
        print ' ex. python %s 192.168.4.7 127.0.0.1:3000' % sys.argv[0]
        sys.exit(-1)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()
