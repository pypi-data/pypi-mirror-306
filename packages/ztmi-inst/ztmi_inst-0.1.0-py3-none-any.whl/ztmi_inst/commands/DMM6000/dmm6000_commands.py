from commands.ieee_commands import *
from commands.DMM6000.measure_config_commands import create_class
from commands.DMM6000.sense_commands import DMMSenseCommand, DMMAutoCommand


class DMMImpedanceCommand:

    def __init__(self, dev, command_syntax: str = "INPut:IMPedance"):
        self._auto = DMMAutoCommand(dev, f'{command_syntax}:AUTO')

    @property
    def auto(self):
        return self._auto


class DMM6000Command:

    def __init__(self, dev):
        self._tst = TST(dev)
        self._idn = IDN(dev)
        self._cls = CLS(dev)
        self._ese = ESE(dev)
        self._esr = ESR(dev)
        self._stb = STB(dev)
        self._psc = PSC(dev)
        self._measure = create_class(CommandRead)(dev, "MEASure")
        self._configure = create_class(CommandWriteNoValue)(dev, "CONFigure")
        self._sense = DMMSenseCommand(dev)
        self._impedance = DMMImpedanceCommand(dev)
        self._error = CommandRead(dev, "SYSTem:ERRor")

    @property
    def tst(self):
        return self._tst

    @property
    def idn(self):
        return self._idn

    @property
    def cls(self):
        return self._cls

    @property
    def ese(self):
        return self._ese

    @property
    def esr(self):
        return self._esr

    @property
    def stb(self):
        return self._stb

    @property
    def psc(self):
        return self._psc

    @property
    def measure(self):
        return self._measure

    @property
    def configure(self):
        return self._configure

    @property
    def sense(self):
        return self._sense

    @property
    def impedance(self):
        return self._impedance

    @property
    def error(self):
        return self._error
