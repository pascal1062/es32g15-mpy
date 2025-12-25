'''
    Analog Input class
    ADC GPIO 
'''
from machine import Pin, ADC
import thermistor10KDegC as aic10K
import therm10KDegCPullD as aic10Kd

class AnalogInput():

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
        if attn == "0DB": self._adc.atten(ADC.ATTN_0DB)
        if attn == "2_5DB": self._adc.atten(ADC.ATTN_2_5DB)
        if attn == "6DB": self._adc.atten(ADC.ATTN_6DB)
        if attn == "11DB": self._adc.atten(ADC.ATTN_11DB)

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


T1 = AnalogInput(1, "temp", 95.0, 0, 14, aic10K, "11DB")
T1.first_value()

#End