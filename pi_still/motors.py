# reference:
# video play problem: http://www.raspberrypi-spy.co.uk/2013/05/capturing-hd-video-with-the-pi-camera-module/

import time
import bluetooth

class Motors:
    def __init__(self, hlist = range(0,180,30), vlist = range(60,130,30)):
        # initial with addr file
        with open("addr",'r') as faddr:
            addr = faddr.readline().strip()
        port  = 1
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.sock.connect((addr,port))
        
        # generate arm scan path
        import arm_router
        nodes = arm_router.gen_nodes(hlist, vlist)
        self.arm_path = arm_router.greedy_path((90,90),nodes)
        self.arm_path.append((90,90))
        
        self.arm_iter = iter(self.arm_path)
        self.arm_status = (90,90)        
        
    def arm_scan(self):        
        while self.arm_scan_loop():
            pass
            
        return 0

    def arm_move(self,node):
        (h,v) = node
        self.arm_status = node
        self.sock.send("V"+chr(v)+'\n')
        self.sock.send('H'+chr(h)+'\n')
    
    def arm_scan_loop(self):
        node = next(self.arm_iter, None)
        if node==None:
            return False
        else:
            self.arm_move(node)
            return True
        
