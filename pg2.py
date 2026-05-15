import plc
import time
import sch
from automation import Automation as func

def exec():
    #
    heat = None
    heat = func.aswitch(heat, plc.T2.value, 5.0, 10.0)
    plc.CH2.write(heat)
    #
    hor = None
    hor = sch.execute(time.localtime(), int(plc.POOL_ON_TIME.value), int(plc.POOL_OFF_TIME.value))
    plc.CH3.write(hor)
    
#End