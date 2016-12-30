from twisted.web.client import FileBodyProducer
from twisted.protocols import basic
from twisted.internet import reactor
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

from udpwkpf import WuClass, Device
import sys
import json

class spot_AWS_Daemon(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('spot_AWS_Daemon')
        self.id = 0
        self.myMQTTClient = AWSIoTMQTTClient("")
        self.myMQTTClient.configureEndpoint("a1trumz0n7avwt.iot.us-west-2.amazonaws.com", 8883)
        self.myMQTTClient.configureCredentials("AWS/root.crt", "AWS/private.key", "AWS/cert.crt")
        self.myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        self.myMQTTClient.connect()
        print "spot_AWS init success"

    def update(self,obj,pID=None,val=None):
        if self.id != (int)(obj.getProperty(0)):
            self.id = (int)(obj.getProperty(0))
            self.obj = obj
            print self.id
            
        if pID == 1:
            trigger = obj.getProperty(1)
            nValid = obj.getProperty(2)
            if trigger == 1:
                nValid += 1
            else:
                nValid -= 1
            obj.setProperty(2, nValid)
            mess = json.dumps({'ParkingSpot': nValid})
            y = self.id % 10
            x = (self.id % 100) / 10
            direc = (self.id % 1000) / 100
            print "Device/0"+str(direc)+str(x)+str(y),"; ParkingSpot:",nValid
            self.myMQTTClient.publish('Device/0'+str(direc)+str(x)+str(y), mess, 0)

if __name__ == "__main__":
    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
            self.m = spot_AWS_Daemon()
            self.addClass(self.m,0)
            self.obj_spot_aws = self.addObject(self.m.ID)

    if len(sys.argv) <= 2:
        print 'python %s <gip> <dip>:<port>' % sys.argv[0]
        print '      <gip>: IP addrees of gateway'
        print '      <dip>: IP address of Python device'
        print '      <port>: An unique port number'
        print ' ex. python %s 192.168.4.7 127.0.0.1:3000' % sys.argv[0]
        sys.exit(-1)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()
