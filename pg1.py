import plc
from timer import Timer

t1 = Timer()

def exec():
    irrig = int(plc.IRRIG_PUMP_TIME.value) * 60
    plc.IRRIG_ELAPS_TIME.write(round(t1.elapsed(),1))
    if t1.running() and ((irrig - t1.elapsed() <= 0)): t1.stop(); plc.CH1.write(False); plc.START_CH1.write(None,8) 
    if plc.IN1.rising() and irrig > 0: plc.CH1.write(True); t1.stop(); t1.start()
    if plc.START_CH1.rising() and irrig > 0: plc.CH1.write(True); t1.stop(); t1.start()
    if plc.START_CH1.value == True and not plc.START_CH1.rising(): plc.START_CH1.write(False)

#End
    