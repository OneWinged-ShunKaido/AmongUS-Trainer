from typing import List, Union
from time import sleep
import inspect

from src.displayer import Displayer
from src.game import GameLauncher

from pymem.process import module_from_name


class CheatTable(GameLauncher, Displayer):
    cmd_map: dict
    default_speed: int = 1
    nbr_impostor: int = 1
    address: int
    offsets: List[int]
    end_offset: int
    value: Union[int, float, str, bool, bytes]

    def __init__(self):
        super().__init__()
        self.set_commands_map()

    def set_commands_map(self):
        self.cmd_map = {
            "1": self.change_speed,
            "2": "",
            "3": "",
            "f2": self.change_speed,
            "f3": self.on_clear
            }

    def update_arg_map(self):
        self.args.update(
            dict(
                base=self.base,
                address=self.address,
                offsets=self.offsets,
                final_offset=self.end_offset,
                value=self.value
            ))

    def memory_access(self, base: int, offsets: List[int]):
        address = self.process.read_int(base)
        for offset in offsets:
            address = self.process.read_int(address + offset)

        return address

    def change_speed(self, new_speed: int = 0):
        self.last_func_name = "change_speed"
        self.address = 0x0144BB70
        self.offsets = [0x5C, 0x4]
        self.end_offset = 0x14
        self.value = 5.0
        self.w2mem()

    def force_impostor(self):
        self.last_func_name = "force_impostor"

    def w2mem(self):
        if not self.base:
            self.base = module_from_name(self.process.process_handle, "GameAssembly.dll").lpBaseOfDll

        self.update_arg_map()

        if isinstance(self.value, int):
            method = self.process.write_int

        elif isinstance(self.value, float):
            method = self.process.write_float

        elif isinstance(self.value, str):
            method = self.process.write_char

        elif isinstance(self.value, bool):
            method = self.process.write_bool

        else:
            self.on_w_type(self.value)
            return False

        self.method = method.__name__
        method(self.memory_access(self.base + self.address, offsets=self.offsets) + self.end_offset, self.value)

    def wr_custom_cheat(self, address: int, offsets: List[int], end_offset: int, value: Union[int, float, str, bool]):
        ...

    def call_cheat(self, key):
        #   print(f"key called: {key}")
        try:
            func = self.cmd_map.get(key)
            func()
            if self.display_success:
                self.on_success(...)

        except Exception as e:
            repr(e)
            if self.display_error:
                self.on_error(e)

        sleep(1)
        return True
