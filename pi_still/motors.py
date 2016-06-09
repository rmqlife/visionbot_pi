# reference:
# video play problem: http://www.raspberrypi-spy.co.uk/2013/05/capturing-hd-video-with-the-pi-camera-module/

import time
import bluetooth

class Motors:
    def __init__(self):
        # initial with addr file
        with open("addr",'r') as faddr:
            addr = faddr.readline().strip()
        port  = 1
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((addr,port))        
        self.status = (90,90)
     
    def arm_scan_init(self, hlist = range(0,180,30), vlist = range(60,130,30)):            
        # generate arm scan path
        import arm_router
        nodes = arm_router.gen_nodes(hlist, vlist)
        self.arm_path = arm_router.greedy_path((90,90),nodes)
        # end with
        self.arm_path.append((90,90))
        self.arm_iter = iter(self.arm_path)
        # start with
        self.arm_status = (90,90)   
    
    def sendCmd(self, cmd):
        self.sock.send(chr(254)+cmd+chr(255)+'\n')
        return 
        
    def arm_move(self,node):
        (h,v) = node
        self.status = node
        self.sendCmd("A"+chr(h)+chr(v))
    
    def arm_move_delta(self, delta):
        (h,v) = delta
        self.status[0] = self.status[0] + h
        self.status[1] = self.status[1] + v
        sefl.arm_move(self, self.status)
    
    def arm_scan_loop(self):
        node = next(self.arm_iter, None)
        if node==None:# end of the loop
            return True 
        else:
            self.arm_move(node)
            return False
    
    def turn(self, direction = 'r'):
        self.sendCmd(direction)
        
