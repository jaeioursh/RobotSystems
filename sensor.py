from ezblock import __reset_mcu__
import time
__reset_mcu__()
time.sleep(0.01)
from ezblock import ADC
from ezblock import print


class Sensor:
    
    def __init__(self):


        self.adc_A0=ADC("A0")

        self.adc_A1=ADC("A1")

        self.adc_A2=ADC("A2")

    def read_ground(self):

        return [self.adc_A0.read(), self.adc_A1.read(), self.adc_A2.read()]

if __name__=="__main__":
    sensor=Sensor()
    while 1:
        print(sensor.read_ground())
        time.sleep(0.5)
