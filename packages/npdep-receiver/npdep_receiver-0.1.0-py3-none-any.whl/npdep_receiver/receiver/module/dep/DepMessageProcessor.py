import os
from pathlib import Path
from threading import *

from dep_common.type.MessageType import MessageType as DEPMessageType
from dep_reader.reader.Reader import Reader as DEPReader

class DepMessageProcessor():
    def __init__(self, options, connection, receiver) -> None:
        self.thread = Thread(target=self.__handleConnections)
        self.connection = connection
        self.isRunning = True
        self.reader = DEPReader()
        self.receiver = receiver
        self.options = options

    def __handleConnections(self): 
        while self.isRunning:   
            # Get the header
            header = self.connection.recv(3) 
            # If there is no header close the connection
            if(not header):
                self.connection.close()
                self.isRunning = False
            else:    
                h_type = header[0:1:1]
                h_length = header[1:3:1]
                h_type_int = int.from_bytes(h_type, "big")
                h_length_int = int.from_bytes(h_length, "big")
                
                payload = self.connection.recv(h_length_int)

                if(h_type_int == DEPMessageType.SYSTEM_INFORMATION_MESSAGE):
                    result = self.reader.processSystemInformationMessage(payload)
                    # Check if there is an exfiltration folder. If not create one
                    targetPath = os.path.join(self.options["savePath"], str(result["systemId"]))
                    targetDirExists = os.path.isdir(targetPath)
                    if(not targetDirExists):
                        os.mkdir(targetPath)
                    # Save SystemInformationMessage
                    self.receiver.systemInfoMessages.append(result)
                    self.isRunning = False

                elif(h_type_int == DEPMessageType.DATA_INFORMATION_MESSAGE):
                    result = self.reader.processDataInformationMessage(payload)
                    self.receiver.dataInfoMessages.append(result)
                    self.isRunning = False

                elif(h_type_int == DEPMessageType.DATA_CONTENT_MESSAGE):
                    result = self.reader.processDataContentMessage(payload)
                    # Check within DataInformationMessage for more information to get path
                    for dataInfo in self.receiver.dataInfoMessages:
                        if(result["systemId"] == dataInfo["systemId"] and result["sha256"] == dataInfo["sha256"]):
                            filePath = dataInfo["path"].replace(":", "_") # filePath needs to be sanitized
                            targetPath = os.path.join(self.options["savePath"], str(result["systemId"]), filePath)
                            targetPathObj = Path(targetPath)
                            Path(targetPathObj.parent).mkdir(parents=True, exist_ok=True)
                            with open(targetPathObj, "ab+") as f:
                                f.write(result["data"])
                else:
                    print("Message Type incorrect!")

    def start(self):
        self.thread.start()

    def terminate(self):
        self.connection.close()
        self.isRunning = False