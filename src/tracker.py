from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread, Signal, QTimer, QObject
from pynput import mouse
import time
import json


class Tracker(QThread):
    def __init__(self):
        super().__init__()
        self.time = time.time()
        self.timeline = []
        self.tracking = True
        self.duration = 10
        self.pause_duration = 2
        self.pauses = [0]
        self.loadConf()
    
    def loadConf(self):
        with open("resources/config.json", "r") as f:
            conf = json.load(f)
            self.duration = conf["tracking-duration"]
            self.pause_duration = conf["pause-duration"]

    def saveConf(self):
        with open("resources/config.json", "w") as f:
            json.dump(
                {
                    "tracking-duration": self.duration,
                    "pause-duration": self.pause_duration
                }, f
            )


    def run(self):
        self.listener = mouse.Listener(on_move=self.on_move)
        self.listener.run()

    def on_move(self, x, y):
        if self.tracking:
            if self.timeline != []:
                if time.time()-self.timeline[-1][2] > self.pause_duration:
                    self.pauses.append(len(self.timeline)-1)
            self.timeline.append((x,y,time.time()))
            if time.time()-self.timeline[0][2] > self.duration:
                self.timeline.pop(0)
                pauses = [0]
                for pause in self.pauses:
                    if pause-1 >= 0:
                        pauses.append(pause-1)
                self.pauses = pauses


