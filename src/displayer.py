from os import system

class Displayer:
    display_success: bool = False
    display_error: bool = True
    last_func_name: str
    method: str
    args: dict = dict.fromkeys(
        [
            "base",
            "address",
            "offsets",
            "final_offset",
            "value"
        ])
    exception: str

    def __init__(self):
        super().__init__()

    @staticmethod
    def on_clear():
        system("cls")

    def on_success(self, ctx):
        print(f"[*] Successfully called {self.last_func_name} -> {ctx}")

    def on_error(self, e: Exception):
        print(f"At {self.last_func_name} [{self.method}] ({e})")
        for key, value in self.args.items():
            if key == "offsets":
                value = [hex(offset) for offset in value]
            elif isinstance(value, int):
                value = hex(value).upper()

            print(f"{key} -> {value}")

    @staticmethod
    def on_w_type(e):
        print(f"[!] Type not supported for \"{type(e)}\"")
