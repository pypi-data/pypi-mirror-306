import os
import socket
from threading import *

from npdep_receiver.receiver.base.Receiver import Receiver

class IcmpEchoReceiver(Receiver):
    def __init__(self, options, logger):
        super().__init__("IcmpEchoReceiver", options, logger)
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_RAW, socket.IPPROTO_ICMP)
        self.thread = Thread(target=self.handle)
        
    def start(self):
        self.socket.bind((self.options["ip"], self.options["port"]))
        self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        self.thread.start()
                
    def handle(self):  
        self.logger.log(self.id + " started listening") 
        file_counter = 0
        while self.isRunning:
            data, addr = self.socket.recvfrom(self.options["pkgSize"])
            # Get the data
            icmp_data = data[28:]
            # Check if file end indicator was send
            # If so, increment file_counter so that the next incoming data package will be 
            # written to a new file
            if(len(icmp_data) == 8 and icmp_data.decode("utf-8") == "file_end"):
                file_counter = file_counter + 1
            else:
                filePath = os.path.join(self.options["savePath"], str(file_counter) + ".file")
                with open(filePath, "ab+") as f:
                    f.write(icmp_data)