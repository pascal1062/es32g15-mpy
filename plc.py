'''
    ES32G15 board PLC inputs / outputs / variables definitions
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
T1 = AnalogInput(1, "sondeB3950", 90.0, -0.38, 0.045, 14, aic10KB, "11DB"); T1.first_value()
T2 = AnalogInput(2, "sonde10K", 90.0, -0.38, 0.045, 27, aic10K, "11DB"); T2.first_value()
PH4 = AnalogInput(4, "photocell", 90.0, 0, 0.045, 32, aicPhoto, "11DB"); PH4.first_value()

#VI1 = AnalogInput(4, "volt_1", 90.0, 0, 36, aic010V, "6DB")
VI1 = AnalogInput(5, "volt_1", 90.0, 1.26, 0.015, 36, aic10K10V, "6DB"); VI1.first_value()

IN1 = BinaryInput(1, "DI1", 19); IN1.value

CH1 = RelayOutput(1, "Relay_1", 12) #pompe irrig. start avec IN1 ou BV1
CH2 = RelayOutput(1, "Relay_2", 13) #heating panel
CH3 = RelayOutput(1, "Relay_3", 21) #pool pump
CH4 = RelayOutput(1, "Relay_4", 23) #for testing through xfer

VO1 = AnalogOutput(1, "AO1", 25)
VO2 = AnalogOutput(2, "AO2", 26)

SCAN_LED = Pin(15, Pin.OUT)
SCAN_LED.on()

START_CH1 = BinaryValue(1, "START_CH1")

IRRIG_PUMP_TIME = AnalogValue(1, "IRRIG_TIME"); IRRIG_PUMP_TIME.write(1)
IRRIG_ELAPS_TIME = AnalogValue(2, "IRRIG_TIME")
POOL_ON_TIME = AnalogValue(3, "POOL_ON"); POOL_ON_TIME.write(600)
POOL_OFF_TIME = AnalogValue(4, "POOL_OFF"); POOL_OFF_TIME.write(2100)


def scan():
    T1.value; T2.value; PH4.value
    VI1.value
    IN1.value
    START_CH1.value

#End