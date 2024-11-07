# ZDS系列触发命令类定义
from commands.command import *


class TriggerOnlyReadCommand(CommandRead):
    pass


class TriggerOnlyWriteNoValueCommand(CommandWriteNoValue):
    pass


class TriggerValidRangeCheck:

    def __init__(self, value: float, _range: list = None):
        if range is None:
            return
        if not _range[0] <= value <= _range[1]:
            raise ValueError(f"Invalid value: {value}")


class TriggerRWCommand(CommandRead, CommandWrite):

    def __init__(self, dev, command_syntax: str, _range: list = None):
        super().__init__(dev, command_syntax)
        self._range: list = _range

    def write(self, value: Any) -> str:
        if isinstance(value, int) or isinstance(value, float):
            TriggerValidRangeCheck(float(value), self._range)
        return super().write(value)


class TriggerSweepCommand(CommandRead):

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._auto = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} AUTO")
        self._normal = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} NORMal")

    @property
    def auto(self):
        return self._auto

    @property
    def normal(self):
        return self._normal


class TriggerCoupingCommand(CommandRead):

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._dc = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} DC")
        self._ac = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} AC")
        self._lf_reject = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} LFReject")
        self._hf_reject = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} HFReject")

    @property
    def dc(self):
        return self._dc

    @property
    def ac(self):
        return self._ac

    @property
    def lf_reject(self):
        return self._lf_reject

    @property
    def hf_reject(self):
        return self._hf_reject


class TriggerModeCommand(CommandRead):

    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._edge = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} EDGE")
        self._pulse = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} PULSe")
        self._slope = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} SLOPe")
        self._video = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} VIDEo")
        self._runt = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} RUNT")
        self._p_runt = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} PRUNt")
        self._pattern = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} PATTern")
        self._n_edge = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} NEDGe")
        self._delay = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} DELay")
        self._timeout = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} TIMeout")
        self._shold = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} SHOLd")

    @property
    def edge(self):
        return self._edge

    @property
    def pulse(self):
        return self._pulse

    @property
    def slope(self):
        return self._slope

    @property
    def video(self):
        return self._video

    @property
    def runt(self):
        return self._runt

    @property
    def p_runt(self):
        return self._p_runt

    @property
    def pattern(self):
        return self._pattern

    @property
    def n_edge(self):
        return self._n_edge

    @property
    def delay(self):
        return self._delay

    @property
    def timeout(self):
        return self._timeout

    @property
    def shold(self):
        return self._shold


class TriggerSourceRWCommand:
    def __init__(self, dev, command_syntax: str, _range: list = None):
        self._ch: Dict[int, TriggerRWCommand] = DefaultDictPassKeyToFactory(
            lambda n: TriggerRWCommand(dev, f"{command_syntax} CHANnel{n}", _range)
        )

    @property
    def ch(self):
        return self._ch


class TriggerSourceCommand(CommandRead):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._ch: Dict[int, TriggerOnlyWriteNoValueCommand] = DefaultDictPassKeyToFactory(
            lambda n: TriggerOnlyWriteNoValueCommand(dev, f"{command_syntax} CHANnel{n}")
        )

    @property
    def ch(self):
        return self._ch


class TriggerEdgeSourceCommand(CommandRead):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._ch: Dict[int, TriggerOnlyWriteNoValueCommand] = DefaultDictPassKeyToFactory(
            lambda n: TriggerOnlyWriteNoValueCommand(dev, f"{command_syntax} CHANnel{n}")
        )
        self._line = TriggerOnlyWriteNoValueCommand(dev, f"{command_syntax} LINE")
        self._external = TriggerOnlyWriteNoValueCommand(dev, f"{command_syntax} EXTernal")

    @property
    def ch(self):
        return self._ch

    @property
    def line(self):
        return self._line

    @property
    def external(self):
        return self._external


class TriggerRootSlopeCommand(CommandRead):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._positive = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} POSitive")
        self._negative = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} NEGative")

    @property
    def positive(self):
        return self._positive

    @property
    def negative(self):
        return self._negative


class TriggerSlopeCommand(TriggerRootSlopeCommand):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._either = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} EITHer")

    @property
    def either(self):
        return self._either


class TriggerDelaySlopeCommand(CommandRead):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._rtor = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} RTOR")
        self._rtof = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} TROF")
        self._ftor = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} FTOR")
        self._ftof = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} FTOF")

    @property
    def rtor(self):
        return self._rtor

    @property
    def rtof(self):
        return self._rtof

    @property
    def ftor(self):
        return self._ftor

    @property
    def ftof(self):
        return self._ftof


class TriggerWhenCommand(CommandRead):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._p_greater = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} PGReater")
        self._p_less = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} PLESs")
        self._pg_less = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} PGLess")
        self._n_greater = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} NGReater")
        self._n_less = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} NLESs")
        self._ng_less = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} NGLess")

    @property
    def p_greater(self):
        return self._p_greater

    @property
    def p_less(self):
        return self._p_less

    @property
    def pg_less(self):
        return self._pg_less

    @property
    def n_greater(self):
        return self._n_greater

    @property
    def n_less(self):
        return self._n_less

    @property
    def ng_less(self):
        return self._ng_less


class TriggerRootWhenCommand(CommandRead):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._greater = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} GREater")
        self._less = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} LESS")
        self._in_range = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} INRange")

    @property
    def greater(self):
        return self._greater

    @property
    def less(self):
        return self._less

    @property
    def in_range(self):
        return self._in_range


class TriggerPuntWhenCommand(TriggerRootWhenCommand):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._none = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} NONE")

    @property
    def none(self):
        return self._none


class TriggerWindowCommand(CommandRead):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._ta = TriggerOnlyWriteNoValueCommand(dev, f"{command_syntax} TA")
        self._tb = TriggerOnlyWriteNoValueCommand(dev, f"{command_syntax} TB")
        self._tab = TriggerOnlyWriteNoValueCommand(dev, f"{command_syntax} TAB")

    @property
    def ta(self):
        return self._ta

    @property
    def tb(self):
        return self._tb

    @property
    def tab(self):
        return self._tab


class TriggerPolarityCommand(CommandRead):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._positive = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} POSitive")
        self._negative = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} NEGative")

    @property
    def positive(self):
        return self._positive

    @property
    def negative(self):
        return self._negative


class TriggerVideoStandardCommand(CommandRead):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._ntsc = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} NTSC")
        self._pal = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} PAL")
        self._secam = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} SECAM")

    @property
    def ntsc(self):
        return self._ntsc

    @property
    def pal(self):
        return self._pal

    @property
    def secam(self):
        return self._secam


class TriggerVideoSlopeCommand(CommandRead):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._any_line = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} ANYLine")
        self._gotoline = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} GOTOline")
        self._any_filed = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} ANYFiled")
        self._even_field = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} EVENfield")
        self._odd_field = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} ODDField")

    @property
    def any_line(self):
        return self._any_line

    @property
    def gotoline(self):
        return self._gotoline

    @property
    def any_filed(self):
        return self._any_filed

    @property
    def even_field(self):
        return self._even_field

    @property
    def odd_field(self):
        return self._odd_field


class TriggerPatternWhenCommand(TriggerPuntWhenCommand):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._out_range = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} OUTRange")

    @property
    def out_range(self):
        return self._out_range


class TriggerRootPatternTypeCommand(CommandRead):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._h = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} H")
        self._l = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} L")

    @property
    def high(self):
        return self._h

    @property
    def low(self):
        return self._l


class TriggerPatternTypeCommand(TriggerRootPatternTypeCommand):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._x = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} X")
        self._r = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} R")
        self._f = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} F")

    @property
    def ignore(self):
        return self._x

    @property
    def rise(self):
        return self._r

    @property
    def fall(self):
        return self._f


class TriggerTypeCommand(CommandRead):
    def __init__(self, dev, command_syntax: str):
        super().__init__(dev, command_syntax)
        self._setup = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} SETup")
        self._hold = TriggerOnlyWriteNoValueCommand(dev, f"{self._command_syntax} HOLd")

    @property
    def setup(self):
        return self._setup

    @property
    def hold(self):
        return self._hold


class TriggerEdgeCommand:
    def __init__(self, dev, command_syntax: str):
        self._source = TriggerEdgeSourceCommand(dev, f"{command_syntax}:SOURce")
        self._slope = TriggerSlopeCommand(dev, f"{command_syntax}:SLOPe")
        self._level = TriggerRWCommand(dev, f"{command_syntax}:LEVel", None)

    @property
    def source(self):
        return self._source

    @property
    def slope(self):
        return self._slope

    @property
    def level(self):
        return self._level


class TriggerPulseCommand:
    def __init__(self, dev, command_syntax: str):
        self._source = TriggerSourceCommand(dev, f"{command_syntax}:SOURce")
        self._when = TriggerWhenCommand(dev, f"{command_syntax}:WHEN")
        self._u_width = TriggerRWCommand(dev, f"{command_syntax}:UWIDth", [1e-9, 1])
        self._l_width = TriggerRWCommand(dev, f"{command_syntax}:LWIDth", [1e-9, 1])
        self._level = TriggerRWCommand(dev, f"{command_syntax}:LEVel", None)

    @property
    def source(self):
        return self._source

    @property
    def when(self):
        return self._when

    @property
    def u_width(self):
        return self._u_width

    @property
    def l_width(self):
        return self._l_width

    @property
    def level(self):
        return self._level


class TriggerSLOPECommand:
    def __init__(self, dev, command_syntax: str):
        self._source = TriggerSourceCommand(dev, f"{command_syntax}:SOURce")
        self._when = TriggerWhenCommand(dev, f"{command_syntax}:WHEN")
        self._tupper = TriggerRWCommand(dev, f"{command_syntax}:TUPPer", [1e-9, 1])
        self._tlower = TriggerRWCommand(dev, f"{command_syntax}:TLOWer", [1e-9, 1])
        self._window = TriggerWindowCommand(dev, f"{command_syntax}:WINDow")
        self._h_level = TriggerRWCommand(dev, f"{command_syntax}:HLEVel", None)
        self._l_level = TriggerRWCommand(dev, f"{command_syntax}:LLEVel", None)

    @property
    def source(self):
        return self._source

    @property
    def when(self):
        return self._when

    @property
    def upper(self):
        return self._tupper

    @property
    def lower(self):
        return self._tlower

    @property
    def window(self):
        return self._window

    @property
    def h_level(self):
        return self._h_level

    @property
    def l_level(self):
        return self._l_level


class TriggerVideoCommand:
    def __init__(self, dev, command_syntax: str):
        self._source = TriggerSourceCommand(dev, f"{command_syntax}:SOURce")
        self._polarity = TriggerPolarityCommand(dev, f"{command_syntax}:POLArity")
        self._standard = TriggerVideoStandardCommand(dev, f"{command_syntax}:STANdard")
        self._slope = TriggerSlopeCommand(dev, f"{command_syntax}:SLOPe")
        self._line = TriggerRWCommand(dev, f"{command_syntax}:LINE", [1, 525])
        self._level = TriggerRWCommand(dev, f"{command_syntax}:LEVel", None)

    @property
    def source(self):
        return self._source

    @property
    def polarity(self):
        return self._polarity

    @property
    def standard(self):
        return self._standard

    @property
    def slope(self):
        return self._slope

    @property
    def line(self):
        return self._line

    @property
    def level(self):
        return self._level


class TriggerRuntCommand:
    def __init__(self, dev, command_syntax: str):
        self._source = TriggerSourceCommand(dev, f"{command_syntax}:SOURce")
        self._slope = TriggerSlopeCommand(dev, f"{command_syntax}:SLOPe")
        self._when = TriggerPuntWhenCommand(dev, f"{command_syntax}:WHEN")
        self._tupper = TriggerRWCommand(dev, f"{command_syntax}:TUPPer", [2e-9, 1])
        self._tlower = TriggerRWCommand(dev, f"{command_syntax}:TLOWer", [2e-9, 1])
        self._window = TriggerWindowCommand(dev, f"{command_syntax}:WINDow")
        self._h_level = TriggerRWCommand(dev, f"{command_syntax}:HLEVel", None)
        self._l_level = TriggerRWCommand(dev, f"{command_syntax}:LLEVel", None)

    @property
    def source(self):
        return self._source

    @property
    def slope(self):
        return self._slope

    @property
    def when(self):
        return self._when

    @property
    def upper(self):
        return self._tupper

    @property
    def lower(self):
        return self._tlower

    @property
    def window(self):
        return self._window

    @property
    def h_level(self):
        return self._h_level

    @property
    def l_level(self):
        return self._l_level


class TriggerPatternCommand:
    def __init__(self, dev, command_syntax: str):
        self._a_src = TriggerSourceCommand(dev, f"{command_syntax}:ASRc")
        self._b_src = TriggerSourceCommand(dev, f"{command_syntax}:BSRc")
        self._a_pat = TriggerPatternTypeCommand(dev, f"{command_syntax}:APat")
        self._b_pat = TriggerPatternTypeCommand(dev, f"{command_syntax}:BPat")
        self._when = TriggerPatternWhenCommand(dev, f"{command_syntax}:WHEN")
        self._tupper = TriggerRWCommand(dev, f"{command_syntax}:TUPPer", [5e-9, 4])
        self._tlower = TriggerRWCommand(dev, f"{command_syntax}:TLOWer", [4e-9, 4])
        self._level = TriggerSourceRWCommand(dev, f"{command_syntax}:LEVel", None)

    @property
    def a_src(self):
        return self._a_src

    @property
    def b_src(self):
        return self._b_src

    @property
    def a_pat(self):
        return self._a_pat

    @property
    def b_pat(self):
        return self._b_pat

    @property
    def when(self):
        return self._when

    @property
    def upper(self):
        return self._tupper

    @property
    def lower(self):
        return self._tlower

    @property
    def level(self):
        return self._level


class TriggerNEdgeCommand:
    def __init__(self, dev, command_syntax: str):
        self._source = TriggerSourceCommand(dev, f"{command_syntax}:SOURce")
        self._slope = TriggerRootSlopeCommand(dev, f"{command_syntax}:SLOPe")
        self._edge_num = TriggerRWCommand(dev, f"{command_syntax}:EDGEnum", [1, 65535])
        self._idle = TriggerRWCommand(dev, f"{command_syntax}:IDLE", [1e-8, 4])
        self._level = TriggerRWCommand(dev, f"{command_syntax}:LEVel", None)

    @property
    def source(self):
        return self._source

    @property
    def slope(self):
        return self._slope

    @property
    def edge_num(self):
        return self._edge_num

    @property
    def idle(self):
        return self._idle

    @property
    def level(self):
        return self._level


class TriggerDelayCommand:
    def __init__(self, dev, command_syntax: str):
        self._a_src = TriggerSourceCommand(dev, f"{command_syntax}:ASRc")
        self._b_src = TriggerSourceCommand(dev, f"{command_syntax}:BSRc")
        self._slope = TriggerDelaySlopeCommand(dev, f"{command_syntax}:SLOPe")
        self._when = TriggerRootWhenCommand(dev, f"{command_syntax}:WHEN")
        self._tupper = TriggerRWCommand(dev, f"{command_syntax}:TUPPer", [1e-9, 1])
        self._tlower = TriggerRWCommand(dev, f"{command_syntax}:TLOWer", [1e-9, 1])
        self._level = TriggerSourceRWCommand(dev, f"{command_syntax}:LEVel", None)

    @property
    def a_src(self):
        return self._a_src

    @property
    def b_src(self):
        return self._b_src

    @property
    def slope(self):
        return self._slope

    @property
    def when(self):
        return self._when

    @property
    def upper(self):
        return self._tupper

    @property
    def lower(self):
        return self._tlower

    @property
    def level(self):
        return self._level


class TriggerTimeoutCommand:
    def __init__(self, dev, command_syntax: str):
        self._source = TriggerSourceCommand(dev, f"{command_syntax}:SOURce")
        self._slope = TriggerSlopeCommand(dev, f"{command_syntax}:SLOPe")
        self._time = TriggerRWCommand(dev, f"{command_syntax}:TIMe", [8e-9, 0.8])
        self._level = TriggerRWCommand(dev, f"{command_syntax}:LEVel", None)

    @property
    def source(self):
        return self._source

    @property
    def slope(self):
        return self._slope

    @property
    def time(self):
        return self._time

    @property
    def level(self):
        return self._level


class TriggerSholdCommand:
    def __init__(self, dev, command_syntax: str):
        self._d_src = TriggerSourceCommand(dev, f"{command_syntax}:DSrc")
        self._c_src = TriggerSourceCommand(dev, f"{command_syntax}:CSrc")
        self._slope = TriggerRootSlopeCommand(dev, f"{command_syntax}:SLOPe")
        self._pattern = TriggerRootPatternTypeCommand(dev, f"{command_syntax}:PATTern")
        self._type = TriggerTypeCommand(dev, f"{command_syntax}:TYPE")
        self._s_time = TriggerRWCommand(dev, f"{command_syntax}:STIMe", [2e-9, 1])
        self._h_time = TriggerRWCommand(dev, f"{command_syntax}:HTIMe", [2e-9, 1])
        self._level = TriggerSourceRWCommand(dev, f"{command_syntax}:LEVel", None)

    @property
    def d_src(self):
        return self._d_src

    @property
    def c_src(self):
        return self._c_src

    @property
    def slope(self):
        return self._slope

    @property
    def pattern(self):
        return self._pattern

    @property
    def type(self):
        return self._type

    @property
    def s_time(self):
        return self._s_time

    @property
    def h_time(self):
        return self._h_time

    @property
    def level(self):
        return self._level


class TriggerCommand(BaseCommand):

    def __init__(self, dev, command_syntax: str = ":TRIG"):
        # print("TriggerCommand Init")
        super().__init__(dev, command_syntax)
        self._state = TriggerOnlyReadCommand(dev, f"{self._command_syntax}:STATE")
        self._sweep = TriggerSweepCommand(dev, f"{self._command_syntax}:SWEEP")
        self._hold_off = TriggerRWCommand(dev, f"{self._command_syntax}:HOLDoff", [0, 16])
        self._sensitivity = TriggerRWCommand(dev, f"{self._command_syntax}:SENSitivity", [0, 1.0])
        self._coupling = TriggerCoupingCommand(dev, f"{self._command_syntax}:COUPling")
        self._mode = TriggerModeCommand(dev, f"{self._command_syntax}:MODE")
        self._edge = TriggerEdgeCommand(dev, f"{self._command_syntax}:EDGE")
        self._pulse = TriggerPulseCommand(dev, f"{self._command_syntax}:PULSe")
        self._slope = TriggerSlopeCommand(dev, f"{self._command_syntax}:SLOPe")
        self._video = TriggerVideoCommand(dev, f"{self._command_syntax}:VIDEO")
        self._runt = TriggerRuntCommand(dev, f"{self._command_syntax}:RUNT")
        self._p_runt = TriggerRuntCommand(dev, f"{self._command_syntax}:PRUNT")
        self._pattern = TriggerPatternCommand(dev, f"{self._command_syntax}:PATTern")
        self._n_edge = TriggerNEdgeCommand(dev, f"{self._command_syntax}:NEDGe")
        self._delay = TriggerDelayCommand(dev, f"{self._command_syntax}:DELay")
        self._timeout = TriggerTimeoutCommand(dev, f"{self._command_syntax}:TIMeout")
        self._shold = TriggerSholdCommand(dev, f"{self._command_syntax}:SHOLd")

    @property
    def state(self):
        return self._state

    @property
    def sweep(self):
        return self._sweep

    @property
    def hold_off(self):
        return self._hold_off

    @property
    def sensitivity(self):
        return self._sensitivity

    @property
    def coupling(self):
        return self._coupling

    @property
    def mode(self):
        return self._mode

    @property
    def edge(self):
        return self._edge

    @property
    def pulse(self):
        return self._pulse

    @property
    def slope(self):
        return self._slope

    @property
    def video(self):
        return self._video

    @property
    def runt(self):
        return self._runt

    @property
    def p_runt(self):
        return self._p_runt

    @property
    def pattern(self):
        return self._pattern

    @property
    def n_edge(self):
        return self._n_edge

    @property
    def delay(self):
        return self._delay

    @property
    def timeout(self):
        return self._timeout

    @property
    def shold(self):
        return self._shold
