try:
    import HiwonderSDK.Board as Board
except:
    class Board:
        def setBusServoPulse(idx, angle, speed):
            pass

from time import sleep
import numpy as np
from copy import deepcopy as copy

def rx(theta):
    theta=np.pi*theta/180
    mat=np.zeros((3,3))
    mat[0,0]=1
    mat[1,1]=np.cos(theta)
    mat[2,2]=np.cos(theta)
    mat[1,2]=-np.sin(theta)
    mat[2,1]=np.sin(theta)
    return mat

    
def rz(theta):
    theta=np.pi*theta/180
    mat=np.zeros((3,3))
    mat[2,2]=1
    mat[1,1]=np.cos(theta)
    mat[0,0]=np.cos(theta)
    mat[0,1]=-np.sin(theta)
    mat[1,0]=np.sin(theta)
    return mat

def dst(length):
    line=np.zeros((3,1))
    line[0,0]=length
    return line

class Move:

    def __init__(self):
        self.lengths=[10.,10.,6.0]

    def position(self,angles,goal):
        a=angles
        l=self.lengths
        R=[rx(a[0]), rz(a[1]), rz(a[2]), rz(a[3])]
        L=[dst(l[0]),dst(l[1]),dst(l[2])]
        Lsum=np.zeros((3,1))
        for i in range(3):
            R[i+1]=np.matmul(R[i],R[i+1])
            Lsum+=np.matmul(R[i+1],L[i])
        #print(goal,Lsum)
        score=np.sqrt(np.sum((goal-Lsum)**2.0))
        return Lsum,score
    
    def IK(self,x,y,z):
        angles=[0.0 for i in range(4)]
        goal=np.array([[x],[y],[z]])
        step=40.0
        while step>.001:
            
            for i in range(4):
                
                pos,neg=copy(angles),copy(angles)
                pos[i]+=step
                neg[i]-=step
                _,nscore=self.position(neg,goal)
                
                _,pscore=self.position(pos,goal)
                _,base=self.position(angles,goal)
                if base<pscore and base<nscore:
                    continue
                #find direction to step in
                if pscore<nscore:
                    dir=1.0
                    prev=pscore
                    angles=pos
                else:
                    dir=-1.0
                    prev=nscore
                    angles=neg
                #step in direction multiple times
                while 1:
                    #print(angles,prev,pscore,nscore)
                    angles[i]+=dir*step
                    _,score=self.position(angles,goal)
                    if score>=prev: #if worse, undo step
                        angles[i]-=dir*step
                        break
                    prev=score
                angles=np.clip(angles,-110,110)
 
            step/=2.0

        return angles
        
    #1:claw, 2:turn, 3: wrist, 4:  elbow, 5: shoulder:, 6 turn 
    def set_angle(self,idx,angle,speed):
        angle=500-angle/90.0*400
        Board.setBusServoPulse(idx, int(angle), speed)
    
    def motor(self,angles,speed):
        ids=[6,5,4,3]
        angles=copy(angles)
        angles[0]*=-1
        angles[2]*=-1
        for i in range(4):
            self.set_angle(ids[i], angles[i], speed)
        sleep(speed/1000)
        
    def open(self,speed=350):
        self.set_angle(2, 0, speed)
        self.set_angle(1, 90, speed)
        sleep(speed/1000)

    def close(self,speed=350):
        self.set_angle(2, 0, speed)
        self.set_angle(1, 15, speed)
        sleep(speed/1000)
        
if __name__=="__main__":
    move=Move()
    #move.open()
    #move.close()
    #move.motor([0,0,0,0],1000)
    #print(move.position([90,0,90,90]))
    g=[10,10,0]
    pos=move.IK(g[0],g[1],g[2])
    print(pos)
    print(move.position(pos,np.array([g]).T))
    pos=[0,0,0,0]
    #pos=[-45,45,45,45]
    #move.motor(pos,1000)

