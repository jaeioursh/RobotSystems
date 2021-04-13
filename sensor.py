from ezblock import __reset_mcu__
import numpy as np
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

class Interpretor:

    def __init__(self, sensitivity, polarity):
        self.sen=sensitivity
        self.pol=polarity

    def transform(self, vals):
        vals=np.array(vals,dtype=float)
        mid=(np.max(vals)+np.min(vals))/2.0
        vals-=mid                                   #shift values down to be centered around zero
        vals+=self.sen/2                            #shift values up to be in sensitivity range
        vals[vals>self.sen]=self.sen                #clip values outside of sensitivity range
        vals[vals<0]=0
        if self.pol<0:                              #flip polarity if needed
            vals= -vals+np.max(vals)
        vals/=np.sum(vals)                           #scale so values add to 1
        return -1.0*vals[0]+vals[2]

if __name__=="__main__":
    sensor=Sensor()
    inter=Interpretor(500,1.0)
    while 1:
        val=sensor.read_ground()
        print(val,inter.transform(val))
        time.sleep(0.5)
