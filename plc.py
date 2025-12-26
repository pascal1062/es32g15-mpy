'''
    ES32G15 board PLC inputs / outputs definitions
'''

from machine import Pin, ADC
import ntc10KDegC_B3950 as aic10KB
import aicPhotocell as aicPhoto
import aicVin010V as aic010V
import therm10KDegCVIN10V as aic10K10V
import math
import time


class ThermistorInput():
    #ThermistorInput class. ADC GPIO I014-IO27-IO33-IO32
    def __init__(self, instance, name, filtr, calib, pin, A, B, C):
        self._pin = pin
        self._adc = ADC(Pin(pin))
        self._adc.atten(ADC.ATTN_11DB)
        self._instance = instance
        self._name = name
        self._filter = filtr
        self._calibration = calib
        self._A = A
        self._B = B
        self._C = C
        self._scan = 0
        self._presentvalue = 0.0
        self._newvalue = 0.0
        self._lastvalue = 0.0
        self._resolution = 65535.0
        self._vcc = 3.3
        self._vadj = 45000
        
    def get_calib(self):
        return self._calibration
    
    def set_calib(self, val):
        self._calibration = val

    def ad_value(self):
        return self._adc.read_u16()

    def volt(self):
        #v = round(self.ad_value() * (self._vcc / self._resolution),4)
        v = (self._adc.read_uv() - self._vadj)/1000000
        return v

    def steinhart(self, volt):
        #A = 1.027280419e-3
        #B = 2.394255475e-4
        #C = 1.555646371e-7
    
        Rt = 10000 * (3.3 / volt - 1)
        log_Rt = math.log(Rt)
        T_K = 1 / (self._A + (self._B * log_Rt) + (self._C * (log_Rt**3)))
        T_C = T_K - 273.15
        return T_C - 0.1

    def first_value(self):
        self._presentvalue = self.steinhart(self.volt()) + self._calibration
        self._lastvalue = self._presentvalue

    @property
    def value(self):
        self._newvalue = self.steinhart(self.volt()) + self._calibration
        self._presentvalue = round(self._lastvalue + (( 100.0 - self._filter) / 100.0 * (self._newvalue - self._lastvalue)), 5)      
        self._lastvalue = self._presentvalue
        return self._presentvalue
    
    @property
    def name(self):
        return self._name


class AnalogInput():
    #ThermistorInput class. ADC GPIO I014-IO27-IO33-IO32  OR  ADC 0-10V GPIO IO36-IO39 4-20mA IO34-IO35
    def __init__(self, instance, name, filtr, calib, pin, scale, attn):
        self._pin = pin
        self._adc = ADC(Pin(pin))
        self._instance = instance
        self._name = name
        self._scale = scale
        self._filter = filtr
        self._calibration = calib
        self._presentvalue = 0.0
        self._newvalue = 0.0
        self._lastvalue = 0.0
        self._vadj = 45000
        if attn == "0DB": self._adc.atten(ADC.ATTN_0DB) #1.00V
        if attn == "2_5DB": self._adc.atten(ADC.ATTN_2_5DB) #1.34V
        if attn == "6DB": self._adc.atten(ADC.ATTN_6DB) #2.00V
        if attn == "11DB": self._adc.atten(ADC.ATTN_11DB) #3.3V

    def get_calib(self):
        return self._calibration
    
    def set_calib(self, val):
        self._calibration = val

    def ad_value(self):
        return self._adc.read_u16()

    def volt(self):
        v = (self._adc.read_uv() - self._vadj)/1000000
        return v

    def aic(self):
        sr = self._scale
        _volt = self.volt()

        if sr.SCALE_RANGE[-1][0] < sr.SCALE_RANGE[0][0] and _volt <= sr.SCALE_RANGE[-1][0]: 
            return sr.SCALE_RANGE[-1][1]  
        if sr.SCALE_RANGE[-1][0] < sr.SCALE_RANGE[0][0] and _volt >= sr.SCALE_RANGE[0][0]: 
            return sr.SCALE_RANGE[0][1]   

        if sr.SCALE_RANGE[-1][0] > sr.SCALE_RANGE[0][0] and _volt <= sr.SCALE_RANGE[0][0]: 
            return sr.SCALE_RANGE[0][1]
        if sr.SCALE_RANGE[-1][0] > sr.SCALE_RANGE[0][0] and _volt >= sr.SCALE_RANGE[-1][0]: 
            return sr.SCALE_RANGE[-1][1]
        
        for i in range(len(sr.SCALE_RANGE) - 1): 
            volt1, val1 = sr.SCALE_RANGE[i] 
            volt2, val2 = sr.SCALE_RANGE[i+1] 

            if  (volt1 >= _volt >= volt2) or (volt1 <= _volt <= volt2):
                # Linear interpolation
                val = val1 + (val2 - val1) * ((_volt - volt1) / (volt2 - volt1))
                return val
           
        return self._lastvalue

    def first_value(self):
        self._presentvalue = self.aic() + self._calibration
        self._lastvalue = self._presentvalue

    @property
    def value(self):
        self._newvalue = self.aic() + self._calibration
        self._presentvalue = round(self._lastvalue + (( 100.0 - self._filter) / 100.0 * (self._newvalue - self._lastvalue)), 5)      
        self._lastvalue = self._presentvalue
        return self._presentvalue
    
    @property
    def name(self):
        return self._name
    

class BinaryInput():
    #BinaryInput class. ADC GPIO I019-IO18-IO5-IO17
    def __init__(self, instance, name, pin, default=False):
        self._pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self._instance = instance
        self._name = name
        self._newvalue = default
        self._lastvalue = default

    def changed(self):
        self.value
        if self._newvalue != self._lastvalue:
            val = True
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    def rising(self):
        self.value
        if self._newvalue != self._lastvalue:
            val = self._newvalue
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    def falling(self):
        self.value
        if (self._newvalue != self._lastvalue):
            val = not self._newvalue
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    @property
    def value(self):
        self._newvalue = True if self._pin.value() == 0 else False

        return self._newvalue
    
    @property
    def name(self):
        return self._name


class RelayOutput():
    #BinaryInput class. ADC GPIO I012-IO13-IO21-IO23
    def __init__(self, instance, name, pin):
        self._pin = Pin(pin, Pin.OUT)
        self._instance = instance
        self._name = name
        self._newvalue = None
        self._lastvalue = None
         
    def get_name(self):
        return self._name    

    def get_value(self):
        return self._newvalue

    def set_value(self, val):
        if isinstance(val, bool):
            self._newvalue = val
            self._pin.on() if self._newvalue else self._pin.off()
        else:
            return

    def changed(self):
        if self._newvalue != self._lastvalue:
            val = True
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    def rising(self):
        if (self._newvalue != self._lastvalue) and (not self._newvalue):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val

    def falling(self):
        if (self._newvalue != self._lastvalue) and (not self._newvalue):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val

    #Set Property
    value = property(get_value, set_value)
    name = property(get_name)


#ES32 Board input-output definitions
#T1 = ThermistorInput(1, "temp_test", 95.0, -0.1, 14, 0.001129148, 0.000234125, 8.76741E-08) #B3950
#T1 = ThermistorInput(1, "sondeB3950", 90.0, 0, 14, 1.284850279E-3, 2.076544735E-4, 2.004280704E-07) #B3950

T1 = AnalogInput(1, "sondeB3950", 90.0, 0, 14, aic10KB, "11DB") 
T1.first_value()
T2 = ThermistorInput(2, "temp_ss", 90.0, -0.1, 27, 1.027280419e-3, 2.394255475e-4, 1.555646371e-7) #10K3
T2.first_value()
PH4 = AnalogInput(4, "photocell", 90.0, 0, 32, aicPhoto, "11DB") 
PH4.first_value()

#VI1 = AnalogInput(4, "volt_1", 90.0, 0, 36, aic010V, "6DB")
VI1 = AnalogInput(5, "volt_1", 90.0, 0, 36, aic10K10V, "6DB")
VI1.first_value()

IN1 = BinaryInput(1, "DI1", 19)
IN1.value

CH1 = RelayOutput(1, "Relay_1", 12)
CH1.value = False
CH2 = RelayOutput(1, "Relay_2", 13)
CH2.value = False
CH3 = RelayOutput(1, "Relay_3", 21)
CH3.value = False
CH4 = RelayOutput(1, "Relay_4", 23)
CH4.value = False

SCAN_LED = Pin(15, Pin.OUT)
SCAN_LED.on()

variable1 = None

#End