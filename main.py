import time
import plc
import pg1
import pg2
import xfer

timer_1 = time.ticks_ms()

xfer._boot()

while True:

    plc.scan()
    xfer.exec()
    pg1.exec()
    pg2.exec()

    #scan led
    if time.ticks_diff(time.ticks_ms(), timer_1) >= 250:
        plc.SCAN_LED.value(1) if plc.SCAN_LED.value() == 0 else plc.SCAN_LED.value(0)
        timer_1 = time.ticks_ms()
  
#End
