from rossros import *
from sensor import Sensor,Sensor2, Interpretor
from motor import Motor


from ezblock import __reset_mcu__
#__reset_mcu__()

ground_sensor=Sensor()
def sense_ground():
    return ground_sensor.read_ground()



dist_sensor=Sensor2()
def sense_dist():
    return dist_sensor.read_dist()

    
inter=Interpretor(500,1.0)   
def interpret_ground(val):
    
    return inter.transform(val)
    
    
motor=Motor()
def control(vals):
    ground,dist=vals
    print(vals)
    if dist<20: #stop
        motor.forward(0,0,0)
        
    else:       #go
        motor.forward(20,-1.0*val*self.scale,0)
        
raw_ground=Bus()
int_ground=Bus()
distance=Bus()
 
 
producer_consumers=[]
producer_consumers.append( Consumer(control,[int_ground,distance],.2) )
producer_consumers.append( Producer(sense_ground,raw_ground,.1) )
producer_consumers.append( Producer(sense_dist,distance,.1) )
producer_consumers.append( ConsumerProducer(interpret_ground,raw_ground,int_ground,.1) )


runConcurrently(producer_consumers)

