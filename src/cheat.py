from typing import List, Union
from time import sleep

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

    def change_speed(self, new_speed: float = 3.0):
        self.last_func_name = "change_speed"
        self.address = 0x0144BB70
        self.offsets = [0x5C, 0x4]
        self.end_offset = 0x14
        self.value = new_speed
        self.w2mem()

    def force_impostor(self):
        self.last_func_name = "force_impostor"

    def w2mem(self):
        self.update_arg_map()
        address = self.args.get("address")
        offsets = self.args.get("offsets")
        end_offset = self.args.get("end_offset")
        value = self.args.get("value")
        self.write2mem(address=address, offsets=offsets, end_offset=end_offset, value=value)

    def write2mem(self, address: int, offsets: List[int], end_offset: int, value: Union[int, float, str, bool]):
        if not self.base:
            self.base = module_from_name(self.process.process_handle, "GameAssembly.dll").lpBaseOfDll

        self.address = address
        self.offsets = offsets
        self.end_offset = end_offset
        self.value = value
        self.update_arg_map()

        if isinstance(value, int):
            method = self.process.write_int

        elif isinstance(value, float):
            method = self.process.write_float

        elif isinstance(value, str):
            method = self.process.write_char

        elif isinstance(value, bool):
            method = self.process.write_bool

        else:
            self.on_w_type(value)
            return False

        self.method = method.__name__

        method(self.memory_access(base=self.base + address, offsets=offsets) + end_offset, value)

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
