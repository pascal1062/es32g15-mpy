import time
#import ai
from data_exchange_ser import DataExchange
from machine import RTC
import plc
import pg1
import pg2
#import modbus_comm

timer_1 = time.ticks_ms()
timer_2 = time.time()
plc.SET_TIME = True

# serial data exchange
xfer = DataExchange(1,57600,0,2)
read = None

#booting 
xfer.send_data({"route": "nred", "board": "es32g15", "state": "booting wait 1 sec..."})

def start_plc():
    pass
    #turn this def for one minute start modus_comm to load RTC time before starting main plc
    #peut-être mettre un While 60 sec ....

    
#function stop board
def _stop():
    xfer.send_data({"route": "nred", "board": "es32g15", "state": "soft reset command received..."})
    from machine import reset
    reset()


#function return date-time
def actualTime(t):
    date_str = "{:4}-{:02}-{:02}".format(t[0],t[1],t[2])
    time_str = "{:02}:{:02}:{:02}".format(t[3],t[4],t[5])
    return date_str+" "+time_str


def handle_xfer(msg):
    #_msg = msg[0].decode("utf8")
    _msg = msg.decode("utf8")
    #_sender = msg[1]
    if _msg == "/es32g15/system/exit": _stop()
    if _msg == "/es32g15/relayBoard/date-heure": xfer.send_recv({"date-time":str(actualTime(time.localtime()))})
    if _msg == "/es32g15/relayBoard/ch4/set/1": plc.CH4.value = True
    if _msg == "/es32g15/relayBoard/ch4/set/0": plc.CH4.value = False
    if _msg == "/es32g15/relayBoard/t1/get": xfer.send_recv({"T1":plc.T1.value})
    if _msg == "/es32g15/relayBoard/t2/get": xfer.send_recv({"T2":plc.T2.value})
    if _msg == "/es32g15/relayBoard/photo/get": xfer.send_recv({"PHOTO":plc.PH4.value})
    if _msg == "/es32g15/relayBoard/vi1/get": xfer.send_recv({"VI1":plc.VI1.value})


while True:
    #print(plc.T2.value, plc.T2.volt(), plc.T1.value, plc.T1.volt(),plc.variable1)
    pg1.exec()
    pg2.exec()
    #modbus_comm.exec()
    #plc.SCAN_LED.off()
    #time.sleep_ms(1)
    #plc.SCAN_LED.on()

    # Read data transfer
    read = xfer.send_recv()
    if read is not None:
        handle_xfer(read)

    if time.ticks_diff(time.ticks_ms(), timer_1) > 250:
        plc.SCAN_LED.value(1) if plc.SCAN_LED.value() == 0 else plc.SCAN_LED.value(0)
        timer_1 = time.ticks_ms()

    #if (time.ticks_diff(time(), timer_2) >= 3600) or plc.SET_TIME:
    #    RTC.datetime((plc.YEAR, plc.MONTH, plc.DAY, 0, plc.HOURS, plc.MINS, plc.SECS, 0))
    #    plc.SET_TIME = False
    #    timer_2 = time()

    if (time.time() - timer_2) >= 60:
        xfer.send_recv({"date-time":str(actualTime(time.localtime()))})
        timer_2 = time.time()
    
#End
