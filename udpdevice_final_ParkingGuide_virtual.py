import time,sys
from udpwkpf import WuClass, Device
from udpwkpf_io_interface import *
from twisted.internet import reactor
import random
from math import log
import time

import udpdevice_light_agent
import udpdevice_light_aws_daemon

class MyDevice(Device):
    def __init__(self,addr,localaddr):
        Device.__init__(self,addr,localaddr)

    def init(self):
        m2 = udpdevice_light_agent.Light_Agent()
        self.addClass(m2,self.FLAG_VIRTUAL)
        self.obj_light_agent = self.addObject(m2.ID)

        m3 = udpdevice_light_aws_daemon.light_AWS_Daemon()
        self.addClass(m3, 0)
        self.obj_light_aws = self.addObject(m3.ID)

if len(sys.argv) <= 2:
        print 'python udpwkpf.py <ip> <ip:port>'
        print '      <ip>: IP of the interface'
        print '      <port>: The unique port number in the interface'
        print ' ex. python udpwkpf.py 127.0.0.1 3000'
        sys.exit(-1)

d = MyDevice(sys.argv[1],sys.argv[2])

reactor.run()
