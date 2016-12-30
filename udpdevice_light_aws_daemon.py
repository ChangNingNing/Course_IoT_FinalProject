from twisted.web.client import FileBodyProducer
from twisted.protocols import basic
from twisted.internet import reactor
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

from udpwkpf import WuClass, Device
import sys
import json

class light_AWS_Daemon(WuClass):
    def __init__(self):
        WuClass.__init__(self)
        self.loadClass('light_AWS_Daemon')
        self.id = 0
        self.myMQTTClient = AWSIoTMQTTClient("")
        self.myMQTTClient.configureEndpoint("a1trumz0n7avwt.iot.us-west-2.amazonaws.com", 8883)
        self.myMQTTClient.configureCredentials("AWS/root.crt", "AWS/private.key", "AWS/cert.crt")
        self.myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        self.myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
        self.myMQTTClient.connect()
        print "light_AWS init success"

    def Callback(self, client, userdata, message, pID):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")
        try:
            data = json.loads(message.payload)
            if 'ParkingSpot' in data:
                self.obj.setProperty(pID, data['ParkingSpot'])
        except ValueError, e:
            print 'not JSON'

    def r_left_Callback(self, client, userdata, message):
        self.Callback(client, userdata, message, 1)
    
    def r_forward_Callback(self, client, userdata, message):
        self.Callback(client, userdata, message, 2)

    def r_right_Callback(self, client, userdata, message):
        self.Callback(client, userdata, message, 3)

    def i_left_Callback(self, client, userdata, message):
        self.Callback(client, userdata, message, 4)

    def i_forward_Callback(self, client, userdata, message):
        self.Callback(client, userdata, message, 5)

    def i_right_Callback(self, client, userdata, message):
        self.Callback(client, userdata, message, 6)

    def update(self,obj,pID=None,val=None):
        if self.id != (int)(obj.getProperty(0)):
            self.id = (int)(obj.getProperty(0))
            self.obj = obj
            x = (self.id % 1000) / 100
            y = (self.id % 100) / 10
            direc = self.id % 10
            print "Device/1"+str(x)+str(y)+str(direc)
            if direc == 0:
                self.myMQTTClient.subscribe('Device/00'+str(x)+str(y+1), 1, self.r_left_Callback)
                self.myMQTTClient.subscribe('Device/01'+str(x)+str(y), 1, self.r_forward_Callback)
                self.myMQTTClient.subscribe('Device/00'+str(x)+str(y), 1, self.r_right_Callback)
                self.myMQTTClient.subscribe('Device/1'+str(x)+str(y+1)+'1', 1, self.i_left_Callback)
                self.myMQTTClient.subscribe('Device/1'+str(x-1)+str(y)+'0', 1, self.i_forward_Callback)
                self.myMQTTClient.subscribe('Device/1'+str(x)+str(y-1)+'3', 1, self.i_right_Callback)
            elif direc == 1:
                self.myMQTTClient.subscribe('Device/01'+str(x+1)+str(y), 1, self.r_left_Callback)
                self.myMQTTClient.subscribe('Device/00'+str(x)+str(y+1), 1, self.r_forward_Callback)
                self.myMQTTClient.subscribe('Device/01'+str(x)+str(y), 1, self.r_right_Callback)
                self.myMQTTClient.subscribe('Device/1'+str(x+1)+str(y)+'2', 1, self.i_left_Callback)
                self.myMQTTClient.subscribe('Device/1'+str(x)+str(y+1)+'1', 1, self.i_forward_Callback)
                self.myMQTTClient.subscribe('Device/1'+str(x-1)+str(y)+'0', 1, self.i_right_Callback)
            elif direc == 2:
                self.myMQTTClient.subscribe('Device/00'+str(x)+str(y), 1, self.r_left_Callback)
                self.myMQTTClient.subscribe('Device/01'+str(x+1)+str(y), 1, self.r_forward_Callback)
                self.myMQTTClient.subscribe('Device/00'+str(x)+str(y+1), 1, self.r_right_Callback)
                self.myMQTTClient.subscribe('Device/1'+str(x)+str(y-1)+'3', 1, self.i_left_Callback)
                self.myMQTTClient.subscribe('Device/1'+str(x+1)+str(y)+'2', 1, self.i_forward_Callback)
                self.myMQTTClient.subscribe('Device/1'+str(x)+str(y+1)+'1', 1, self.i_right_Callback)
            elif direc == 3:
                self.myMQTTClient.subscribe('Device/01'+str(x)+str(y), 1, self.r_left_Callback)
                self.myMQTTClient.subscribe('Device/00'+str(x)+str(y), 1, self.r_forward_Callback)
                self.myMQTTClient.subscribe('Device/01'+str(x+1)+str(y), 1, self.r_right_Callback)
                self.myMQTTClient.subscribe('Device/1'+str(x-1)+str(y)+'0', 1, self.i_left_Callback)
                self.myMQTTClient.subscribe('Device/1'+str(x)+str(y-1)+'3', 1, self.i_forward_Callback)
                self.myMQTTClient.subscribe('Device/1'+str(x+1)+str(y)+'2', 1, self.i_right_Callback)
        
        if pID == 7:
            x = (self.id % 1000) / 100
            y = (self.id % 100) / 10
            direc = self.id % 10
            state = obj.getProperty(7)
            print "Device/1"+str(x)+str(y)+str(direc)+"; state : "+str(state)
            mess = json.dumps({'ParkingSpot': state})
            self.myMQTTClient.publish('Device/1'+str(x)+str(y)+str(direc), mess, 0)

if __name__ == "__main__":
    class MyDevice(Device):
        def __init__(self,addr,localaddr):
            Device.__init__(self,addr,localaddr)

        def init(self):
            self.m = light_AWS_Daemon()
            self.addClass(self.m,0)
            self.obj_light_aws = self.addObject(self.m.ID)

    if len(sys.argv) <= 2:
        print 'python %s <gip> <dip>:<port>' % sys.argv[0]
        print '      <gip>: IP addrees of gateway'
        print '      <dip>: IP address of Python device'
        print '      <port>: An unique port number'
        print ' ex. python %s 192.168.4.7 127.0.0.1:3000' % sys.argv[0]
        sys.exit(-1)

    d = MyDevice(sys.argv[1],sys.argv[2])
    reactor.run()
