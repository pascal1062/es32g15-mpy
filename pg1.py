import plc
from timer import Timer

t1 = Timer()

def exec():
    #plc.CH1.on() if plc.T2.value > 35 else plc.CH1.off()
    #if plc.IN1.rising(): plc.CH1.value = not plc.CH1.value 
    if t1.running() and ((60 - t1.elapsed() <= 0)): t1.stop(); plc.CH1.value = False
    if plc.IN1.rising(): plc.CH1.value = True; t1.stop(); t1.start()
    #if plc.IN1.falling(): plc.CH1.off()

    