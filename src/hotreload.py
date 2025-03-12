from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread, Signal, QTimer, QObject
from pynput import keyboard
import subprocess
import sys
import time


class HotReload(QThread):
    def __init__(self, hotkey: str = "<ctrl>+c", before=None, after=None):
        super().__init__()
        self.hotkey = hotkey
        self.before, self.after = before, after

    def reload(self):
        try:
            self.parent().envSaveGeometry()
        except AttributeError:
            pass
        if self.before != None:
            self.before()

        timeout = 2
        process = subprocess.Popen(
            [sys.executable] + sys.argv,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True
        )
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            if process.returncode != 0:
                process.kill()
        except subprocess.TimeoutExpired:
            self.listener.stop()
            if self.after != None:
                self.after()
            QApplication.quit()


    def start(self):
        hotkey_dict = {self.hotkey: self.reload}
        self.listener = keyboard.GlobalHotKeys(hotkey_dict)
        self.listener.start()