import time
from do_every import DoEvery
import re
import json
import plc
from machine import RTC
from data_exchange_ser import DataExchange

# serial data exchange
xchg = DataExchange(1,57600,0,2)

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


#function stop board
def _stop():
    xchg.send_recv({"route": "nred", "board": "es32g15", "state": "soft reset command received..."})
    from machine import reset
    reset()


#function return date-time
def actualTime(t):
    date_str = "{:4}-{:02}-{:02}".format(t[0],t[1],t[2])
    time_str = "{:02}:{:02}:{:02}".format(t[3],t[4],t[5])
    return date_str+" "+time_str


#main execution
def exec():
    read = xchg.send_recv()
    try:
        msg = json.loads(read.decode("utf8"))

        if msg['brd'] == 1 and msg['val'] == "tsync" and regex.match(msg['t']):
            _set_time(msg['t'])

        if msg['brd'] == 1 and msg['req'] == "get":
            if msg['id'] == "sys" and msg['val'] == "time": xchg.send_recv({"date-time":str(actualTime(time.localtime()))})

            if msg['id'] == "T1" and msg['val'] == "null": xchg.send_recv({"T1":plc.T1.value})
            if msg['id'] == "T2" and msg['val'] == "null": xchg.send_recv({"T2":plc.T2.value})
            if msg['id'] == "VI1" and msg['val'] == "null": xchg.send_recv({"VI1":plc.VI1.value})
            if msg['id'] == "PHOTO" and msg['val'] == "null": xchg.send_recv({"PH4":plc.PH4.value})

        if msg['brd'] == 1 and msg['req'] == "set":
            if msg['id'] == "sys" and msg['val'] == "rst": _stop()
            if msg['id'] == "sys" and msg['val'] == "tsync": xchg.send_recv({"date-time":"sync"})

            if msg['id'] == "CH4" and msg['val'] == "On": plc.CH4.value = True if msg['val'] == "On" else False
            if msg['id'] == "BV1" and msg['val'] == "On": plc.START_CH1.value = True if msg['val'] == "On" else False
            if msg['id'] == "VO1" and type(msg['val']) is int and 0 <= msg['val'] <= 100: plc.VO1.value = msg['val']  
    except:
        pass


    if timer2.every(60):
        xchg.send_recv({"date-time":"sync"})

    if timer1.every(1):
        xchg.send_recv({"date-time":str(actualTime(time.localtime()))})

#End