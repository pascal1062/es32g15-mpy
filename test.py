import time
from machine import Pin, ADC
from ai import AnalogInput as AI
import thermistor10KDegC as aic10K
import therm10KDegCPullD as aic10Kd
import math

T1 = AI(1, "temp", 95.0, -0.1, 14, aic10Kd)
T2 = AI(2, "temp", 95.0, -0.1, 27, aic10Kd)
#T1 = ADC(Pin(14))
#T1.atten(ADC.ATTN_11DB)

def steinhart(AD):
    A = 1.027280419e-3
    B = 2.394255475e-4
    C = 1.555646371e-7

    Rt = 10000 * (3.3 / AD - 1)
    #Rt = 10000 * (AD - 1 / 3.3)
    log_Rt = math.log(Rt)
    T_K = 1 / (A + (B * log_Rt) + (C * (log_Rt**3)))
    T_C = T_K - 273.15
    return T_C - 0.1

print("waiting IO scan")
for i in range(100):
    T1.value
    time.sleep(0.1)
    print(100-i)

while True:
    print(T1.value, T1.volt(), steinhart(T1.volt()), steinhart(T2.volt()))
    time.sleep(0.1)
    
#End