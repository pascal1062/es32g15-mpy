import plc
from machine import RTC
from umodbus.serial import ModbusRTU

rtc = RTC()
client = ModbusRTU(addr=1, pins=(0,2), baudrate=9600) 

register_definitions = {
    "COILS": {
        "CH1": {
            "register": 0,
            "len": 1,
            "val": 0
        }
    },
    "HREGS": {
        "THERM_INPUT": {
            "register": 0,
            "len": 4,
            "val": [-40,-40,-40,-40]
        },
        "RTC" : {
            "register": 10,
            "len": 8,
            "val": [2000,1,1,0,0,0,5,0]
        }
    }
}

register_definitions['COILS']['CH1']['val'] = plc.CH4.value
register_definitions['HREGS']['THERM_INPUT']['val'][0] = int(round(plc.T2.value,2)*100)
register_definitions['HREGS']['THERM_INPUT']['val'][1] = int(round(plc.T1.value,2)*100)
register_definitions['HREGS']['THERM_INPUT']['val'][2] = int(plc.PH4.value)
register_definitions['HREGS']['THERM_INPUT']['val'][3] = int(plc.VI1.value)
#register_definitions['HREGS']['EXAMPLE_HREG']['on_get_cb'] = my_hr_get_cb
client.setup_registers(registers=register_definitions)

#def my_hr_get_cb(reg_type, address, val!:

LASTSET = 0

def exec():
    global LASTSET
    result = client.process()
    plc.CH4.value = True if client.get_coil(0) == 1 and not plc.CH4.value else None
    plc.CH4.value = False if client.get_coil(0) == 0 and plc.CH4.value else None
    client.set_coil(0,plc.CH4.value)
    client.set_hreg(0,int(round(plc.T2.value,2)*100))
    client.set_hreg(1,int(round(plc.T1.value,2)*100))
    client.set_hreg(2,int(plc.PH4.value))
    client.set_hreg(3,int(plc.VI1.value))

    #RTC registers 
    YEAR = client.get_hreg(10)
    MONTH = client.get_hreg(11)
    DAY = client.get_hreg(12)
    HOURS = client.get_hreg(13)
    MINS = client.get_hreg(14)
    SECS = client.get_hreg(15)
    TZ = client.get_hreg(16)
    SETTIME = client.get_hreg(17)

    if SETTIME != LASTSET:
        print("time set") 
        rtc.datetime((YEAR, MONTH, DAY, 0, HOURS, MINS, SECS, 0))
        LASTSET = SETTIME

#End