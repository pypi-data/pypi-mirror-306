import time
# from thrift import *
from thrift.server import TServer

from drivers.multimeter.dmm6000 import DMM6000Driver
from inst_manager import InstManager


# s = TServer.TSimpleServer()
# inst_manager = InstManager()
# processor = ExampleService.Processor(inst_manager)

# with InstManager() as inst_manager:
#     # 实例化一个ZDS5054型号的仪器
#     osc = inst_manager.inst_create(instrumentation="ZDS5054PRO", address='192.168.138.13', port=5025)
#
#     # 相当于面控的Clear按键
#     osc.commands.cls.write()
#
#     # 读取仪器系统信息
#     print(osc.commands.idn.read())
#     # 读取仪器制造商、型号、序列号、版本号
#     print(osc.manufacturer)
#     print(osc.model)
#     print(osc.serial)
#     print(osc.version)
#
#     osc.commands.root.stop.write()
#     osc.commands.root.run.write()
#
#     # 读取仪器通道1是否打开 语法：“:CHANnel1:DISPlay?”
#     print((f := osc.commands.ch[1].display.read()))
#
#     # 打开通道2 语法：“:CHANnel2:DISPlay 1”
#     osc.commands.ch[2].display.write(1)
#     # 语法：“:CHANnel2:DISPlay?”
#     print((s := osc.commands.ch[2].display.read()))

    # 关闭通道2 语法：“:CHANnel2:DISPlay 0”
    # osc.commands.ch[2].display.write(0)
    # 语法：“:CHANnel2:DISPlay?”
    # print((d := osc.commands.ch[2].display.read()))

    # 获取通道1探头类型命令语法
    # print(osc.commands.ch[1].units.syntax)
    # osc.write(osc.commands.ch[1].units.syntax + "?")
    # print((g := osc.read(1024, 2)))

    # 获取通道1探头类型 语法：“:CHANnel1:UNITs?”
    # print((h := osc.commands.ch[1].units.read()))

    # 设置通道1的垂直灵敏度
    # osc.commands.ch[1].scale.write(1.0)

    # 获取通道1的垂直灵敏度
    # print((j := osc.commands.ch[1].scale.read()))

    # 设置通道1的探头的衰减比
    # osc.commands.ch[1].probe.write(0.2)
    # print((k := osc.commands.ch[1].probe.read()))
    # osc.commands.ch[1].probe.write(10)
    # print((l := osc.commands.ch[1].probe.read()))

    # 打开测试峰值(可以不执行)
    # osc.commands.measure.vpp.base.ch[1].write()
    # 获取测试峰值
    # print(q := osc.commands.measure.vpp.base.ch[1].read())
    # print(w := osc.commands.measure.vpp.state.ch[1].read())
    # print(e := osc.commands.measure.vpp.current.ch[1].read())
    # print(r := osc.commands.measure.vpp.maximum.ch[1].read())
    # print(t := osc.commands.measure.vpp.minimum.ch[1].read())
    # print(y := osc.commands.measure.vpp.average.ch[1].read())
    # print(u := osc.commands.measure.vpp.deviation.ch[1].read())
    # print(i := osc.commands.measure.vpp.count.ch[1].read())
    # 获取测试峰值的语法
    # print((p := osc.commands.measure.vpp.base.ch[1].syntax))

    # 获取N周期有效值的当前值
    # print(o := osc.commands.measure.vavg.current.cycle.ch[1].read())
    # 获取全屏周期有效值的当前值
    # print(n := osc.commands.measure.vavg.current.display.ch[1].read())
    # 获取N/全屏周期有效值的语法
    # print(p := osc.commands.measure.vavg.base.cycle.ch[1].syntax)
    # print(a := osc.commands.measure.vavg.base.display.ch[1].syntax)

    # 获取N周期的比率测量状态、当前值
    # print(s := osc.commands.measure.vratio.state.cycle.ch[1].ch[2].read())
    # print(o := osc.commands.measure.vratio.current.cycle.ch[1].ch[2].read())

    # 获取直流、N周期的状态、当前值
    # print(o := osc.commands.measure.vrms.state.ac.cycle.ch[1].read())
    # print(s := osc.commands.measure.vrms.current.dc.cycle.ch[1].read())

    # 获取上升沿计数测量状态、当前值
    # print(o := osc.commands.measure.rcount.state.ch[1].read())
    # print(s := osc.commands.measure.rcount.current.ch[1].read())

    # 获取通道间的上升沿到上升沿延迟的测量状态、当前值
    # print(o := osc.commands.measure.rrdelay.state.ch[1].ch[2].read())
    # print(s := osc.commands.measure.rrdelay.current.ch[1].ch[2].read())

    # 配置建立保持通道
    # print(q := osc.commands.measure.shold.samp.read())
    # print(w := osc.commands.measure.shold.samp.either.write())
    # print(e := osc.commands.measure.shold.tch.read())
    # print(r := osc.commands.measure.shold.tch.ch[1].write())
    # print(t := osc.commands.measure.shold.dch.read())
    # print(y := osc.commands.measure.shold.dch.ch[2].write())

    # 配置高阈值
    # print(q := osc.commands.measure.threshold.upper.read())
    # print(w := osc.commands.measure.threshold.upper.write(80))
    # print(e := osc.commands.measure.threshold.upper.read())
    # print(r := osc.commands.measure.threshold.upper.write(90))

    # 配置测量范围
    # print(q := osc.commands.measure.scope.read())
    # print(w := osc.commands.measure.scope.zoom1.write())
    # print(e := osc.commands.measure.scope.read())
    # print(r := osc.commands.measure.scope.main.write())

    # 配置触发模式
    # print(a := osc.commands.trigger.mode.edge.write())
    # print(b := osc.commands.trigger.mode.read())
    # print(c := osc.commands.trigger.mode.timeout.write())
    # print(d := osc.commands.trigger.mode.read())

    # 配置超时触发超时时间参数
    # print(e := osc.commands.trigger.timeout.time.write(0.1))
    # print(f := osc.commands.trigger.timeout.time.read())
    # pass


with InstManager() as inst:
    dmm = inst.inst_create(instrumentation="DMM6001", address='192.168.138.14', port=4999)

    # 读取仪器系统信息
    print(dmm.commands.idn.read())
    # 读取仪器制造商、型号、序列号、版本号
    print(dmm.manufacturer)
    print(dmm.model)
    print(dmm.serial)
    print(dmm.version)

    # print(k := dmm.commands.measure.voltage.dc.default.read())
    # print(m := dmm.commands.measure.voltage.dc.minimum.default.read())
    # print(z := dmm.commands.measure.voltage.dc.range(1).read())
    # print(x := dmm.commands.measure.voltage.dc.range(0.1).maximum.read())
    # print(c := dmm.commands.measure.voltage.dc.range(0.01).resolution(0.001).read())
    # print(v := dmm.commands.measure.voltage.dc.maximum.resolution(0.001).read())

    # print(q := dmm.commands.measure.resistance.default.read())
    # print(w := dmm.commands.measure.resistance.minimum.maximum.read())
    # print(e := dmm.commands.measure.resistance.range(10000).read())
    # print(r := dmm.commands.measure.resistance.range(1000).maximum.read())
    # print(t := dmm.commands.measure.resistance.range(100).resolution(0.1).read())
    # print(y := dmm.commands.measure.resistance.maximum.resolution(1000).read())

    # print(w := dmm.commands.measure.frequency.default.read())

    # print(q := dmm.commands.measure.temperature.pt100.read())
    # print(w := dmm.commands.measure.temperature.pt100.c.read())

    # print(q := dmm.commands.measure.continuity.read())

    # dmm.commands.configure.voltage.dc.default.write()
    # dmm.commands.configure.voltage.dc.maximum.maximum.write()
    # dmm.commands.configure.voltage.dc.range(1).write()
    # dmm.commands.configure.voltage.dc.range(0.1).minimum.write()
    # dmm.commands.configure.voltage.dc.range(0.01).resolution(0.001).write()
    # dmm.commands.configure.voltage.dc.maximum.resolution(0.001).write()

    # print(dmm.write('FUNCtion "VOLTage:DC?"'))
    # print(dmm.read(1024, 2))

    # print(q := dmm.commands.sense.voltage.dc.range.syntax)
    # print(w := dmm.commands.sense.voltage.dc.range.range(1).write())
    # print(e := dmm.commands.sense.voltage.dc.range.minimum.write())
    # print(r := dmm.commands.sense.voltage.dc.range.minimum.read())

    # print(d := dmm.commands.impedance.auto.on.write())
    # dmm.commands.configure.voltage.dc.default.write()
    # print(k := dmm.commands.measure.voltage.dc.default.read())
    # pass
