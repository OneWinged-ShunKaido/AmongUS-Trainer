from src.cheat import CheatTable
from keyboard import is_pressed


class AmongClient(CheatTable):

    def __init__(self):
        super().__init__()
        self.on_command_handler()

    def on_command_handler(self):
        key = False
        while self.is_alive:
            if is_pressed("1"):
                key = "1"

            elif is_pressed("2"):
                key = "2"

            elif is_pressed("F1"):
                key = "f1"

            elif is_pressed("F2"):
                key = "f2"

            elif is_pressed("F3"):
                key = "f3"

            if key:
                self.call_cheat(key)
                key = False

    """def get_pid(self):
        print(self.process.process_id)"""
