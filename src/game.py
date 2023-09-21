from time import sleep
from threading import Thread

from pymem import Pymem
from pymem.exception import ProcessNotFound


class GameLauncher:
    _instance = None
    proc_name: str
    process: Pymem = None
    base: int = False
    is_alive: bool = False

    def __new__(cls, proc_name: str = "among us"):
        if cls._instance is None:
            cls._instance = super(GameLauncher, cls).__new__(cls)
            cls._instance.initialize(proc_name)
        return cls._instance

    def initialize(self, proc_name):
        self.proc_name = proc_name
        self.wait_for_process()
        #   TODO: fix start_monitoring_thread -> monitor_process() to check instance status

    def wait_for_process(self):
        while not self.process:
            try:
                self.process = Pymem(self.proc_name)
                self.is_alive = True
                #   print("hooked to {}".format(self.proc_name))
            except ProcessNotFound:
                self.is_alive = False
                sleep(1)

    def is_process_alive(self):
        if not self.process:
            self.is_alive = False
            return False

        """if self.process:
            try:
                if self.process.process_id:  # This will raise an exception if the process is not alive
                    return True

            except ProcessNotFound:
                self.is_alive = False
                return False
        return False"""

    def monitor_process(self):
        while True:
            self.is_process_alive()
            sleep(1)

    def start_monitoring_thread(self):
        monitoring_thread = Thread(target=self.monitor_process)
        monitoring_thread.daemon = True
        monitoring_thread.start()


