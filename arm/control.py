from move import Move 
from sensor import Sensor
import numpy as np

def to_pos(box):
    center=np.mean(box,axis=0)
    print(center)
    y,x=center
    y-=480/2
    x-=640/2

    y/=480/2
    x/=640/2

    y*=8.0+21
    x*=23.0/2.0
    
    return x,y
    
def main():
    move = Move()
    sensor=Sensor()
    img=sensor.capture()
    print(img.shape)
    boxes,img=sensor.identify(img)
    box=boxes[0]
    print(box)
    y,z=to_pos(box)
    print(y,z)
    
    move.open()
    pos=move.IK2(-2,-z,-y)
    move.motor(pos,3000)
    move.close()
    move.motor([0,0,0,0],3000)

main()
