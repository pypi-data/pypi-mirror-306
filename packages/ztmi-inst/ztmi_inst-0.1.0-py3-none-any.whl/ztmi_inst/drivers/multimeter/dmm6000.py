from drivers.driver import Driver
from functools import cached_property
from commands.DMM6000.dmm6000_commands import DMM6000Command


class DMM6000Driver(Driver):

    def __init__(self, host, port):
        super().__init__(host, port)
        dev = self if isinstance(self, Driver) else None
        self._commands = DMM6000Command(dev)
        self.__idn_string = self._commands.idn.read()
        self._dev_name = self.model
        pass

    @cached_property
    def manufacturer(self):
        return self.__idn_string.split(" ")[0].strip()

    @cached_property
    def model(self):
        return self.__idn_string.split(" ")[1].strip()

    @cached_property
    def serial(self):
        return self.__idn_string.split(" ")[2].strip()

    @cached_property
    def version(self):
        return f"{self.__idn_string.split(" ")[3].strip()}".strip()

