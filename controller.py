from ezblock import __reset_mcu__
import numpy as np
import time

from sensor import Sensor, Interpretor
from motor import Motor



Vilib.camera_start(True)
Vilib.color_detect_switch(True)
from vilib import Vilib

#from ezblock import ADC
#from ezblock import print

class controller:
    def __init__(self,scale):
        self.scale=scale
        self.sensor=Sensor()
        self.inter=Interpretor(500,1.0)
        self.motor=Motor()
    
    def run(self):
        while 1:
            val=self.sensor.read_ground()
            val=self.inter.transform(val)
            self.motor.forward(60,val*self.scale,0.5)

if __name__=="__main__":
    __reset_mcu__()
    time.sleep(0.01)
    
    