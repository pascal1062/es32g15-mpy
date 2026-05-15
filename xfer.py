import time
from do_every import DoEvery
import re
import json
import plc
from machine import RTC
from com_rx_tx import DataExchange

# serial data exchange
#xchg = DataExchange(1,57600,0,2)
xchg = DataExchange(1,38400,0,2)

#variable
timer1 = DoEvery("timer1", "min")
timer2 = DoEvery("timer2", "min")

#rtc date-time
rtc = RTC()
regex = re.compile("^([2][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9])\s([0-9][0-9]:[0-5][0-9]:[0-5][0-9][-][0-9])$")


def _set_time(t):
    date_time = t

    year = int(date_time[0:4])
    month = int(date_time[5:7])
    day = int(date_time[8:10])
    hour = int(date_time[11:13])
    minute = int(date_time[14:16])
    second = int(date_time[17:19])
    subsecond = 0
    tz = int(date_time[19:21])
    rtc.datetime((year, month, day, 0, hour, minute, second, subsecond))
    print("RTC updated\n")


#send at boot
def _boot():
    xchg.send_recv({"route": "nred", "board": "es32g15", "state": "booting wait 1 sec..."})
    time.sleep(1)
    xchg.send_recv({"date-time":"sync"})


#function restart board
def _reset(type):
    xchg.send_recv({"route": "nred", "board": "es32g15", "state": "soft reset command received..."})
    from machine import reset, soft_reset
    if type == "hard":
        reset()
    elif type == "soft":
        soft_reset()


#function return date-time
def actualTime(t):
    date_str = "{:4}-{:02}-{:02}".format(t[0],t[1],t[2])
    time_str = "{:02}:{:02}:{:02}".format(t[3],t[4],t[5])
    return date_str+" "+time_str

#eval number on analog value
def ana_opts(m):
    return True if m is None or isinstance(m,(int,float)) else False

#main execution
def exec():
    plc_obj = {"T1":plc.T1.value, "T2":plc.T2.value, "PHOTO":plc.PH4.value, "VI1":plc.VI1.value, "DI1":plc.IN1.value, 
               "CH1":plc.CH1.value, "CH2":plc.CH2.value, "CH3":plc.CH3.value, "CH4":plc.CH4.value, "AO1":plc.VO1.value, 
               "AO2":plc.VO2.value, "BV1":plc.START_CH1.value, "AV1":plc.IRRIG_PUMP_TIME.value, "AV2":plc.IRRIG_ELAPS_TIME.value}
    
    read = xchg.send_recv()
    try:
        msg = json.loads(read.decode("utf8"))
        bin_opts = (None, True, False)
        prio_opts = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)

        if msg['brd'] == 1 and msg['val'] == "tsync" and regex.match(msg['t']):
            _set_time(msg['t'])

        if msg['brd'] == 1 and msg['req'] == "get":
            if msg['id'] == "sys" and msg['val'] == "time": xchg.send_recv({"date-time":str(actualTime(time.localtime()))})

            if msg['id'] == "PLC" and msg['val'] == "null": xchg.send_recv(plc_obj)
            if msg['id'] == "T1" and msg['val'] == "null": xchg.send_recv({"T1":plc.T1.value})
            if msg['id'] == "T2" and msg['val'] == "null": xchg.send_recv({"T2":plc.T2.value})
            if msg['id'] == "VI1" and msg['val'] == "null": xchg.send_recv({"VI1":plc.VI1.value})
            if msg['id'] == "PHOTO" and msg['val'] == "null": xchg.send_recv({"PH4":plc.PH4.value})
            if msg['id'] == "CH1" and msg['val'] == "prio": xchg.send_recv({"CH1.prio":plc.CH1.priority})
            if msg['id'] == "CH2" and msg['val'] == "prio": xchg.send_recv({"CH2.prio":plc.CH2.priority})
            if msg['id'] == "CH3" and msg['val'] == "prio": xchg.send_recv({"CH3.prio":plc.CH3.priority})
            if msg['id'] == "CH4" and msg['val'] == "prio": xchg.send_recv({"CH4.prio":plc.CH4.priority})
            if msg['id'] == "BV1" and msg['val'] == "prio": xchg.send_recv({"BV1.prio":plc.START_CH1.priority})
            if msg['id'] == "AV1" and msg['val'] == "prio": xchg.send_recv({"AV1.prio":plc.IRRIG_PUMP_TIME.priority})
            if msg['id'] == "AV2" and msg['val'] == "prio": xchg.send_recv({"AV2.prio":plc.IRRIG_ELAPS_TIME.priority})
            if msg['id'] == "AV3" and msg['val'] == "prio": xchg.send_recv({"AV3.prio":plc.POOL_ON_TIME.priority})
            if msg['id'] == "AV4" and msg['val'] == "prio": xchg.send_recv({"AV4.prio":plc.POOL_OFF_TIME.priority})
            if msg['id'] == "VO1" and msg['val'] == "prio": xchg.send_recv({"VO1.prio":plc.VO1.priority})
            if msg['id'] == "VO2" and msg['val'] == "prio": xchg.send_recv({"VO2.prio":plc.VO2.priority})

        if msg['brd'] == 1 and msg['req'] == "set":
            if msg['id'] == "sys" and msg['val'] == "rsthard": _reset("hard")
            if msg['id'] == "sys" and msg['val'] == "rstsoft": _reset("soft")
            if msg['id'] == "sys" and msg['val'] == "tsync": xchg.send_recv({"date-time":"sync"})

            if msg['id'] == "CH1" and msg['val'] in bin_opts and msg['prio'] in prio_opts: plc.CH1.write(msg['val'],msg['prio'])
            if msg['id'] == "CH2" and msg['val'] in bin_opts and msg['prio'] in prio_opts: plc.CH2.write(msg['val'],msg['prio'])
            if msg['id'] == "CH3" and msg['val'] in bin_opts and msg['prio'] in prio_opts: plc.CH3.write(msg['val'],msg['prio'])
            if msg['id'] == "CH4" and msg['val'] in bin_opts and msg['prio'] in prio_opts: plc.CH4.write(msg['val'],msg['prio'])
            if msg['id'] == "BV1" and msg['val'] in bin_opts and msg['prio'] in prio_opts: plc.START_CH1.write(msg['val'],msg['prio'])
            if msg['id'] == "AV1" and ana_opts(msg['val']) and msg['prio'] in prio_opts: plc.IRRIG_PUMP_TIME.write(msg['val'],msg['prio'])
            if msg['id'] == "AV2" and ana_opts(msg['val']) and msg['prio'] in prio_opts: plc.IRRIG_ELAPS_TIME.write(msg['val'],msg['prio'])
            if msg['id'] == "AV3" and ana_opts(msg['val']) and msg['prio'] in prio_opts: plc.POOL_ON_TIME.write(msg['val'],msg['prio'])
            if msg['id'] == "AV4" and ana_opts(msg['val']) and msg['prio'] in prio_opts: plc.POOL_OFF_TIME.write(msg['val'],msg['prio'])
            if msg['id'] == "VO1" and ana_opts(msg['val']) and msg['prio'] in prio_opts: plc.VO1.write(msg['val'],msg['prio'])
            if msg['id'] == "VO2" and ana_opts(msg['val']) and msg['prio'] in prio_opts: plc.VO2.write(msg['val'],msg['prio'])
    except:
        pass


    if timer2.every(60):
        xchg.send_recv({"date-time":"sync"})

    if timer1.every(1):
        xchg.send_recv(plc_obj)

#End