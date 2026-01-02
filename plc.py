'''
    ES32G15 board PLC inputs / outputs definitions
'''

from machine import Pin, ADC
from av import AnalogValue
from bv import BinaryValue
from ip_op import ThermistorInput
from ip_op import AnalogInput
from ip_op import BinaryInput
from ip_op import RelayOutput
from ip_op import AnalogOutput
import therm10KDegCPullD as aic10K
import ntc10KDegC_B3950 as aic10KB
import aicPhotocell as aicPhoto
import aicVin010V as aic010V
import therm10KDegCVIN10V as aic10K10V


#ES32 Board input-output definitions
#T1 = ThermistorInput(1, "temp_test", 95.0, -0.1, 14, 0.001129148, 0.000234125, 8.76741E-08) #B3950
#T1 = ThermistorInput(1, "sondeB3950", 90.0, 0, 14, 1.284850279E-3, 2.076544735E-4, 2.004280704E-07) #B3950
#T2 = ThermistorInput(2, "temp_ss", 90.0, -0.1, 27, 1.027280419e-3, 2.394255475e-4, 1.555646371e-7); T2.first_value()

T1 = AnalogInput(1, "sondeB3950", 90.0, 0, 14, aic10KB, "11DB"); T1.first_value()
T2 = AnalogInput(2, "sonde10K", 90.0, 0, 27, aic10K, "11DB"); T2.first_value()
PH4 = AnalogInput(4, "photocell", 90.0, 0, 32, aicPhoto, "11DB"); PH4.first_value()

#VI1 = AnalogInput(4, "volt_1", 90.0, 0, 36, aic010V, "6DB")
VI1 = AnalogInput(5, "volt_1", 90.0, 0, 36, aic10K10V, "6DB"); VI1.first_value()

IN1 = BinaryInput(1, "DI1", 19); IN1.value

CH1 = RelayOutput(1, "Relay_1", 12); CH1.value = False
CH2 = RelayOutput(1, "Relay_2", 13); CH2.value = False
CH3 = RelayOutput(1, "Relay_3", 21); CH3.value = False
CH4 = RelayOutput(1, "Relay_4", 23); CH4.value = False

VO1 = AnalogOutput(1, "AO1", 25); VO1.value = 0
VO2 = AnalogOutput(2, "AO2", 26); VO2.value = 0

SCAN_LED = Pin(15, Pin.OUT)
SCAN_LED.on()

START_CH1 = BinaryValue(1, "START_CH1")

def scan():
    T1.value; T2.value; PH4.value
    VI1.value
    IN1.value
    START_CH1.value

#End