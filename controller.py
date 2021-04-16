from ezblock import __reset_mcu__
import numpy as np
import time

from sensor import Sensor, Interpretor
from motor import Motor
from camera import Camera


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
            print(val)
            self.motor.forward(20,-1.0*val*self.scale,0.25)
    def run_camera(self):
        camera=Camera()
        self.motor.set_camera_servo1_angle(0)
        self.motor.set_camera_servo2_angle(-50)
        time.sleep(0.2)
        while 1:
            val=camera.read()
            print(val)
            #self.motor.set_camera_servo2_angle(-50)

            self.motor.forward(20,1.0*val*self.scale,0.25)
if __name__=="__main__":
    __reset_mcu__()
    time.sleep(0.01)
    controller=Controller(20)
    controller.run()
