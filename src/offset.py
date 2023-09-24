from os.path import isfile
from json import dumps, load
from json.decoder import JSONDecodeError
from typing import List


class OffsetTable:
    game_offsets: dict
    address: int
    offsets: List[int]

    def __init__(self):
        self.OFFSET_PATH = "./src/offset.json"
        if not isfile(self.OFFSET_PATH):
            self.save_offsets()
        else:
            self.load_offsets()

    def load_offsets(self):
        try:
            self.game_offsets = dict(load(open(self.OFFSET_PATH)))

        except FileNotFoundError or JSONDecodeError:
            self.save_offsets()

    def read_address(self, key: str) -> int:
        return self.game_offsets.get(key)["address"]

    def read_offsets(self, key: str) -> List[int]:
        return self.game_offsets.get(key)["offsets"]

    def read_cheat_table(self, key: str):
        self.address, self.offsets = self.read_address(key), self.read_offsets(key)

    def save_offsets(self):
        open("./src/offset.json", "w", encoding="utf-8").write(dumps(offsets_table, ensure_ascii=False, indent=4))
        self.game_offsets = offsets_table


offsets_table = {
    "speed": {
        "address": 0x0282F5D8,
        "offsets": [0xB8, 0x0, 0xB8, 0x50],
        "default_value": 1.0
    },
    "vision": {
        "address": 0x0,
        "offsets": [0x0],
        "default_value": 0.0
    }
}

