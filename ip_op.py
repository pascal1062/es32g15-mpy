'''
    Input Output of es32g15 board
    T1-T2-T3-T4 ADC GPIO I014-IO27-IO33-IO32
    VI1-VI2 ADC 0-10V GPIO IO36-IO39. Ii1-Ii2 4-20mA GPIO IO34-IO35
    IN1-IN2-IN3-IN4 GPIO I019-IO18-IO5-IO17
    CH1-CH2-CH3-CH4 GPIO I012-IO13-IO21-IO23
    VO1-VO2 (0-10V or 4-20Ma) GPIO IO25-IO26
'''
import math
from machine import Pin, ADC, DAC


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
    #AnalogInput class. ADC GPIO I014-IO27-IO33-IO32  OR  ADC 0-10V GPIO IO36-IO39 4-20mA IO34-IO35
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
    #BinaryInput class. GPIO I019-IO18-IO5-IO17
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
    #BinaryOutput class. GPIO I012-IO13-IO21-IO23
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


class AnalogOutput():
    #AnalogOutput class. (0-10V or 4-20Ma set on dip switch) GPIO IO25-IO26
    def __init__(self, instance, name, pin):
        self._dac = DAC(Pin(pin))
        self._instance = instance
        self._name = name
        self._newvalue = None
        self._lastvalue = None
         
    def get_name(self):
        return self._name    

    def get_value(self):
        return self._newvalue

    def set_value(self, val):
        if isinstance(val, int):
            slp = int((val - 0) * (255 - 0) / (100 - 0) + 0)
            slp = max(0, min(slp, 255))
            self._newvalue = slp
            self._dac.write(slp)
        else:
            return

    def changed(self):
        if self._newvalue != self._lastvalue:
            val = True
        else:
            val = False
        self._lastvalue = self._newvalue
        return val

    def greater(self):
        if (self._newvalue != self._lastvalue) and (self._newvalue > self._lastvalue):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val

    def smaller(self):
        if (self._newvalue != self._lastvalue) and (self._newvalue < self._lastvalue):
            val = True
            self._lastvalue = self._newvalue
        else:
            val = False
        return val

    #Set Property
    value = property(get_value, set_value)
    name = property(get_name)
    

#End