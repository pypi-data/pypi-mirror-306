from commands.command import *


def create_class(mixin):

    class DMMResolutionValue(mixin):

        def __init__(self, dev, command_syntax: str):
            super().__init__(dev, command_syntax)
            self._default = mixin(dev, f"{self._command_syntax},DEF")
            self._maximum = mixin(dev, f"{self._command_syntax},MAX")
            self._minimum = mixin(dev, f"{self._command_syntax},MIN")

        def resolution(self, value: Union[float, int]):
            if not (isinstance(value, float) or isinstance(value, int)):
                raise ValueError("\033[93mOnly float or int type is allowed\033[0m")
            return mixin(self._device, f"{self._command_syntax},{value}")

        @property
        def default(self):
            return self._default

        @property
        def maximum(self):
            return self._maximum

        @property
        def minimum(self):
            return self._minimum

    class DMMRangeValue(mixin):

        def __init__(self, dev, command_syntax: str):
            super().__init__(dev, command_syntax)
            self._default = DMMResolutionValue(dev, f"{self._command_syntax} DEF")
            self._maximum = DMMResolutionValue(dev, f"{self._command_syntax} MAX")
            self._minimum = DMMResolutionValue(dev, f"{self._command_syntax} MIN")

        def range(self, value: Union[float, int]):
            if not (isinstance(value, float) or isinstance(value, int)):
                raise ValueError("\033[93mOnly float or int type is allowed\033[0m")
            return DMMResolutionValue(self._device, f"{self._command_syntax} {value}")

        @property
        def default(self):
            return self._default

        @property
        def maximum(self):
            return self._maximum

        @property
        def minimum(self):
            return self._minimum

    class DMMRangeValueNoResolution(mixin):

        def __init__(self, dev, command_syntax: str):
            super().__init__(dev, command_syntax)
            self._default = mixin(dev, f"{self._command_syntax} DEF")
            self._maximum = mixin(dev, f"{self._command_syntax} MAX")
            self._minimum = mixin(dev, f"{self._command_syntax} MIN")

        def range(self, value: Union[float, int]):
            if not (isinstance(value, float) or isinstance(value, int)):
                raise ValueError("\033[93mOnly float or int type is allowed\033[0m")
            return mixin(self._device, f"{self._command_syntax} {value}")

        @property
        def default(self):
            return self._default

        @property
        def maximum(self):
            return self._maximum

        @property
        def minimum(self):
            return self._minimum

    class DMMTypeCommand:

        def __init__(self, dev, command_syntax: str):
            self._dc = DMMRangeValue(dev, f"{command_syntax}:DC")
            self._ac = DMMRangeValue(dev, f"{command_syntax}:AC")

        @property
        def dc(self):
            return self._dc

        @property
        def ac(self):
            return self._ac

    class DMMTemperatureUnitValue(mixin):

        def __init__(self, dev, command_syntax: str):
            super().__init__(dev, command_syntax)
            self._default = CommandRead(dev, f"{self._command_syntax},DEF")
            self._c = mixin(dev, f"{self._command_syntax},C")
            self._f = mixin(dev, f"{self._command_syntax},F")
            self._k = mixin(dev, f"{self._command_syntax},K")

        @property
        def default(self):
            return self._default

        @property
        def c(self):
            return self._c

        @property
        def f(self):
            return self._f

        @property
        def k(self):
            return self._k

    class DMMTemperatureCommand(mixin):

        def __init__(self, dev, command_syntax: str):
            super().__init__(dev, command_syntax)
            self._default = DMMTemperatureUnitValue(dev, f"{self._command_syntax} DEF")
            self._pt100 = DMMTemperatureUnitValue(dev, f"{self._command_syntax} PT100")
            self._pt200 = DMMTemperatureUnitValue(dev, f"{self._command_syntax} PT200")
            self._pt500 = DMMTemperatureUnitValue(dev, f"{self._command_syntax} PT500")
            self._pt800 = DMMTemperatureUnitValue(dev, f"{self._command_syntax} PT800")
            self._pt1000 = DMMTemperatureUnitValue(dev, f"{self._command_syntax} PT1000")

        @property
        def default(self):
            return self._default

        @property
        def pt100(self):
            return self._pt100

        @property
        def pt200(self):
            return self._pt200

        @property
        def pt500(self):
            return self._pt500

        @property
        def pt800(self):
            return self._pt800

        @property
        def pt1000(self):
            return self._pt1000

    class DMMMeasureConfigCommand:

        def __init__(self, dev, command_syntax: str):
            self._voltage = DMMTypeCommand(dev, f"{command_syntax}:VOLTage")
            self._current = DMMTypeCommand(dev, f"{command_syntax}:CURRent")
            self._resistance = DMMRangeValue(dev, f"{command_syntax}:RESistance")
            self._capacitance = DMMRangeValueNoResolution(dev, f"{command_syntax}:CAPacitance")
            self._frequency = DMMRangeValueNoResolution(dev, f"{command_syntax}:FREQuency")
            self._period = DMMRangeValueNoResolution(dev, f"{command_syntax}:PERiod")
            self._temperature = DMMTemperatureCommand(dev, f"{command_syntax}:TEMPerature")
            self._continuity = mixin(dev, f"{command_syntax}:CONTinuity")
            self._diode = mixin(dev, f"{command_syntax}:DIODe")

        @property
        def voltage(self):
            return self._voltage

        @property
        def current(self):
            return self._current

        @property
        def resistance(self):
            return self._resistance

        @property
        def capacitance(self):
            if str(self._capacitance.dev.dev_name) == "multimeter":
                return self._capacitance
            else:
                return f"\033[93m'{self._capacitance.syntax}' {self._capacitance.dev.dev_name} not supported\033[0m"

        @property
        def frequency(self):
            return self._frequency

        @property
        def period(self):
            if str(self._period.dev.dev_name) == "DMM6001":
                return self._period
            else:
                return f"\033[93m'{self._period.syntax}' {self._period.dev.dev_name} not supported\033[0m"

        @property
        def temperature(self):
            return self._temperature

        @property
        def continuity(self):
            return self._continuity

        @property
        def diode(self):
            return self._diode

    return DMMMeasureConfigCommand
