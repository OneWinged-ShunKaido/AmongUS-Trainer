from typing import List, Union, Type
from time import sleep

from src.displayer import Displayer
from src.game import GameLauncher
from src.offset import OffsetTable

from pymem.process import module_from_name


class CheatTable(GameLauncher, Displayer, OffsetTable):
    cmd_map: dict
    default_speed: int = 1.0
    nbr_impostor: int = 1
    address: int
    offsets: List[int]
    end_offset: int
    value: Union[int, float, str, bool, bytes]

    def __init__(self):
        super().__init__()
        self.set_commands_map()
        self.save_offsets()

    def set_commands_map(self):
        self.cmd_map = {
            "f2": self.change_speed,
            "f3": self.on_clear
            }

    def update_arg_map(self):
        self.args.update(
            dict(
                base=self.base,
                address=self.address,
                offsets=self.offsets,
                value=self.value
            ))

    def memory_access(self, addr: int, offsets: List[int]):
        #   addr: 41762360
        #   address: 1831169379072
        address = self.process.read_longlong(self.base + addr)
        for i in range(len(offsets) - 1):
            try:
                address = self.process.read_longlong(address + offsets[i])

            except Exception as e:
                repr(e)
                return False

        return address + offsets[-1]

    """def memory_access(self, base: int, offsets: List[int]):
        address = self.process.read_int(base)
        for offset in offsets:
            address = self.process.read_int(address + offset)

        return address"""

    def change_speed(self, new_speed: float = 3.0):
        self.last_func_name = "change_speed"
        self.address = 0x027D3E38
        self.address, self.offsets = self.read_cheat_table("speed")
        self.value = new_speed
        current_speed = self.read_mem(addr=self.address, offsets=self.offsets, v_type=float)
        print(f"current speed: {current_speed}")
        new_speed = input("Enter new speed: ")
        try:
            new_speed = float(new_speed)

        except ValueError:
            new_speed = self.default_speed

        self.value = new_speed
        self.w2mem()

    def force_impostor(self):
        self.last_func_name = "force_impostor"

    def read_mem(self, addr: int, offsets: List[int], v_type: Union[Type[int], Type[float], Type[str], Type[bool]] = int):
        if not self.base:
            self.base = module_from_name(self.process.process_handle, "GameAssembly.dll").lpBaseOfDll
        self.base = module_from_name(self.process.process_handle, "GameAssembly.dll").lpBaseOfDll
        if v_type == int:
            method = self.process.read_longlong

        elif v_type == float:
            method = self.process.read_float

        elif v_type == str:
            method = self.process.read_string

        elif v_type == bool:
            method = self.process.read_bool

        else:
            self.on_v_type(v_type)
            return False

        return method(self.memory_access(addr=addr, offsets=offsets))

    def w2mem(self):
        self.update_arg_map()
        address = self.args.get("address")
        offsets = self.args.get("offsets")
        #   end_offset = self.args.get("final_offset")
        value = self.args.get("value")
        self.write2mem(address=address, offsets=offsets, value=value)

    def write2mem(self, address: int, offsets: List[int], value: Union[int, float, str, bool]):
        if not self.base:
            self.base = module_from_name(self.process.process_handle, "GameAssembly.dll").lpBaseOfDll

        self.address = address
        self.offsets = offsets
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

        method(self.memory_access(addr=address, offsets=offsets), value)

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
