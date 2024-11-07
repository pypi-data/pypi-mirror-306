from commands.command import *


def _create_type_command(mixin, cmd_suffix):
    class DMMSenseTypeCommand:

        def __init__(self, dev, command_syntax: str):
            self._dc = mixin(dev, command_syntax + f":DC{cmd_suffix}")
            self._ac = mixin(dev, command_syntax + f":AC{cmd_suffix}")

        @property
        def dc(self):
            return self._dc

        @property
        def ac(self):
            return self._ac

    return DMMSenseTypeCommand


class DMMFunctionCommand(CommandRead):

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._voltage = (
            _create_type_command(CommandWriteNoValue, '"')(dev, f'{command_syntax} "VOLTage'))
        self._current = (
            _create_type_command(CommandWriteNoValue, '"')(dev, f'{command_syntax} "CURRent'))
        self._resistance = CommandWriteNoValue(dev, f'{command_syntax} "RESistance"')
        self._fresistance = CommandWriteNoValue(dev, f'{command_syntax} "FRESistance"')
        self._capacitance = CommandWriteNoValue(dev, f'{command_syntax} "CAPacitance"')
        self._frequency = CommandWriteNoValue(dev, f'{command_syntax} "FREQuency"')
        self._period = CommandWriteNoValue(dev, f'{command_syntax} "PERiod"')
        self._temperature = CommandWriteNoValue(dev, f'{command_syntax} "TEMPerature"')
        self._continuity = CommandWriteNoValue(dev, f'{command_syntax} "CONTinuity"')
        self._diode = CommandWriteNoValue(dev, f'{command_syntax} "DIODe"')

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
    def fresistance(self):
        return self._fresistance

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


class DMMSenseWRCommand(CommandWriteNoValue, CommandRead):
    pass


class DMMSenseMaxMinCommand(BaseCommand):

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._minimum = DMMSenseWRCommand(dev, f'{command_syntax} MIN')
        self._maximum = DMMSenseWRCommand(dev, f'{command_syntax} MAX')

    @property
    def minimum(self):
        return self._minimum

    @property
    def maximum(self):
        return self._maximum


class DMMAutoCommand(CommandRead):

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._off = CommandWriteNoValue(dev, f'{command_syntax} OFF')
        self._on = CommandWriteNoValue(dev, f'{command_syntax} ON')

    @property
    def off(self):
        return self._off

    @property
    def on(self):
        return self._on


class DMMSenseRangeCommand(DMMSenseMaxMinCommand):

    def __init__(self, dev, command_syntax: str = ':RANGe'):
        super().__init__(dev, command_syntax)
        self._auto = DMMAutoCommand(dev, f'{command_syntax}:AUTO')

    def range(self, value: Union[float, int]):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise ValueError("\033[93mOnly float or int type is allowed\033[0m")
        return CommandWriteNoValue(self._device, f'{self._command_syntax} {value}')

    @property
    def auto(self):
        return self._auto


class DMMSenseResolutionCommand(DMMSenseMaxMinCommand):

    def __init__(self, dev, command_syntax: str = ':RESolution'):
        super().__init__(dev, command_syntax)

    def resolution(self, value: Union[float, int]):
        if not (isinstance(value, float) or isinstance(value, int)):
            raise ValueError("\033[93mOnly float or int type is allowed\033[0m")
        return CommandWriteNoValue(self._device, f'{self._command_syntax} {value}')


class DMMSenseSetupQueryCommand:

    def __init__(self, dev, command_syntax: str):
        self._range = DMMSenseRangeCommand(dev, f'{command_syntax}:RANGe')
        self._resolution = DMMSenseResolutionCommand(dev, f'{command_syntax}:RESolution')

    @property
    def range(self):
        return self._range

    @property
    def resolution(self):
        return self._resolution


class DMMSenseBandwidthCommand(DMMSenseMaxMinCommand):

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._3 = CommandWriteNoValue(dev, f'{command_syntax} 3')
        self._20 = CommandWriteNoValue(dev, f'{command_syntax} 20')
        self._200 = CommandWriteNoValue(dev, f'{command_syntax} 200')

    @property
    def three(self):
        return self._3

    @property
    def twenty(self):
        return self._20

    @property
    def two_hundred(self):
        return self._200


class DMMSenseTempDefCommand(CommandRead):

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._def = CommandWriteNoValue(dev, f'{command_syntax} DEF')

    @property
    def default(self):
        return self._def


class DMMSenseTempTypeCommand(DMMSenseTempDefCommand):

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._pt100 = CommandWriteNoValue(dev, f'{command_syntax} PT100')
        self._pt200 = CommandWriteNoValue(dev, f'{command_syntax} PT200')
        self._pt500 = CommandWriteNoValue(dev, f'{command_syntax} PT500')
        self._pt1000 = CommandWriteNoValue(dev, f'{command_syntax} PT1000')

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
    def pt1000(self):
        return self._pt1000


class DMMSenseTempUnitCommand(DMMSenseTempDefCommand):

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._c = CommandWriteNoValue(dev, f'{command_syntax} C')
        self._f = CommandWriteNoValue(dev, f'{command_syntax} F')
        self._k = CommandWriteNoValue(dev, f'{command_syntax} K')

    @property
    def c(self):
        return self._c

    @property
    def f(self):
        return self._f

    @property
    def k(self):
        return self._k


class DMMSenseTemperatureCommand:

    def __init__(self, dev, command_syntax: str = "TEMPerature"):
        self._type = DMMSenseTempTypeCommand(dev, command_syntax)
        self._unit = DMMSenseTempUnitCommand(dev, command_syntax)

    @property
    def type(self):
        return self._type

    @property
    def unit(self):
        return self._unit


class DMMSenseCommand:

    def __init__(self, dev):
        self._function = DMMFunctionCommand(dev, "FUNCtion")
        self._voltage = _create_type_command(DMMSenseSetupQueryCommand, '')(dev, f'VOLTage')
        self._current = _create_type_command(DMMSenseSetupQueryCommand, '')(dev, f'CURRent')
        self._resistance = DMMSenseSetupQueryCommand(dev, 'RESistance')
        self._fresistance = DMMSenseSetupQueryCommand(dev, 'FRESistance')
        self._capacitance = DMMSenseRangeCommand(dev, 'CAPacitance')
        self._frequency = DMMSenseRangeCommand(dev, 'FREQuency')
        self._period = DMMSenseRangeCommand(dev, 'PERiod:VOLTage')
        self._bandwidth = DMMSenseBandwidthCommand(dev, 'DETector:BANDwidth')
        self._temperature = DMMSenseTemperatureCommand(dev)

    @property
    def function(self):
        return self._function

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
    def fresistance(self):
        return self._fresistance

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
    def bandwidth(self):
        return self._bandwidth
