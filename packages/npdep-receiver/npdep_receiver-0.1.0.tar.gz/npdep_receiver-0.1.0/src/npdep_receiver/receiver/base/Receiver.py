import os
from pathlib import Path

class Receiver():
    def __init__(self, id, options, logger) -> None:
        self.id = id
        self.options = options
        self.logger = logger
        self.isRunning = True
        self.socket = None
        self.thread = None
        self.__createDataDirectory()

    def __createDataDirectory(self):
        dirExists = os.path.isdir(self.options["savePath"])
        if(not dirExists):
            Path(self.options["savePath"]).mkdir(parents=True)


    def start(self):
        print("No special behaviour for start step implemented in receiver module: " + self.id)

    def handle(self):
        print("No special behaviour for handle step implemented in receiver module: " + self.id)

    def end(self):
        print("No special behaviour for end step implemented in receiver module: " + self.id)

    def start(self):
        self.thread.start()

    def terminate(self):
        self.socket.close()
        self.isRunning = False