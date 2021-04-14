from ezblock import __reset_mcu__
import numpy as np
import time

from sensor import Sensor, Interpretor
from motor import Motor


#from vilib import Vilib
#Vilib.camera_start(True)
#Vilib.color_detect_switch(True)


#from ezblock import ADC
#from ezblock import print

class Controller:
    def __init__(self,scale):
        self.scale=scale
        self.sensor=Sensor()
        self.inter=Interpretor(500,1.0)
        self.motor=Motor()
    
    def run(self):
        while 1:
            val=self.sensor.read_ground()
            val=self.inter.transform(val)
            self.motor.forward(70,val*self.scale,0.5)

if __name__=="__main__":
    __reset_mcu__()
    time.sleep(0.01)
    controller=Controller(20)
    controller.run()