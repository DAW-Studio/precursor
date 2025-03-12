from PySide6.QtCore import QThread, Signal
from pynput import keyboard


class Shortcuts(QThread):
    hotkey_triggered = Signal(str)

    def __init__(self, hotkeys_funcs: dict):
        super().__init__()
        self.hotkeys_funcs = hotkeys_funcs
        self.hotkeys = {}
        for hotkey in hotkeys_funcs:
            self.hotkeys[hotkey] = lambda hk=hotkey: self.hotkey_triggered.emit(hk)

        self.hotkey_triggered.connect(self.handle_hotkey)

    def run(self):
        self.listener = keyboard.GlobalHotKeys(self.hotkeys)
        self.listener.run()

    def handle_hotkey(self, hotkey):
        if hotkey in self.hotkeys_funcs:
            self.hotkeys_funcs[hotkey]()