import time,sys
from udpwkpf import WuClass, Device
from udpwkpf_io_interface import *
from twisted.internet import reactor
import random
from math import log
import time

import udpdevice_ParkingSpot2
import udpdevice_spot_aws_daemon

class MyDevice(Device):
    def __init__(self,addr,localaddr):
        Device.__init__(self,addr,localaddr)

    def init(self):
        m1 = udpdevice_ParkingSpot2.ParkingSpot()
        self.addClass(m1,0)
        self.obj_parking_spot = self.addObject(m1.ID)
        
        m2 = udpdevice_spot_aws_daemon.spot_AWS_Daemon()
        self.addClass(m2, 0)
        self.obj_spot_aws = self.addObject(m2.ID)

if len(sys.argv) <= 2:
        print 'python udpwkpf.py <ip> <ip:port>'
        print '      <ip>: IP of the interface'
        print '      <port>: The unique port number in the interface'
        print ' ex. python udpwkpf.py 127.0.0.1 3000'
        sys.exit(-1)

d = MyDevice(sys.argv[1],sys.argv[2])

reactor.run()
