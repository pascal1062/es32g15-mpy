import plc
#from machine import Pin

#CH2 = Pin(13, Pin.OUT)

def exec():
    plc.CH2.value = True if plc.T2.value < -10 else False