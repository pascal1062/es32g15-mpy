import time
#import ai
from machine import RTC
import plc
import pg1
import pg2
import modbus_comm

timer_1 = time.ticks_ms()
timer_2 = time()
plc.SET_TIME = True

print("...starting")

def start_plc():
    pass
    #turn this def for one minute start modus_comm to load RTC time before starting main plc
    #peut-être mettre un While 60 sec ....


while True:
    #print(plc.T2.value, plc.T2.volt(), plc.T1.value, plc.T1.volt(),plc.variable1)
    pg1.exec()
    pg2.exec()
    modbus_comm.exec()
    #plc.SCAN_LED.off()
    time.sleep_ms(1)
    #plc.SCAN_LED.on()

    if time.ticks_diff(time.ticks_ms(), timer_1) > 250:
        plc.SCAN_LED.value(1) if plc.SCAN_LED.value() == 0 else plc.SCAN_LED.value(0)
        timer_1 = time.ticks_ms()

    if (time.ticks_diff(time(), timer_2) >= 3600) or plc.SET_TIME:
        RTC.datetime((plc.YEAR, plc.MONTH, plc.DAY, 0, plc.HOURS, plc.MINS, plc.SECS, 0))
        plc.SET_TIME = False
        timer_2 = time()
    
#End
