from move import Move
import numpy as np
from datetime import datetime


paths=[
    [ [0.0,0.0],[1.0,0.0],[1.0,1.0],[0.0,1.0],[0.0,0.0] ], #0
    [ [0.5,0.0],[0.5,1.0] ], # 1
    [ [0.0,0.0],[1.0,0.0],[0.0,1.0],[1.0,1.0] ], #2
    [ [0.0,0.0],[1.0,0.0],[0.0,0.5],[1.0,1.0],[0.0,1.0] ], #3
    [ [1.0,1.25],[1.0,0.0],[0.0,0.75],[1.25,0.75] ], #4
    [ [1.0,0.0],[0.0,0.0],[0.0,0.5],[1.0,1.0],[0.0,1.0] ], #5
    [ [1.0,0.0],[0.0,0.0],[0.0,1.0],[1.0,1.0],[1.0,0.5],[0.0,0.5] ], #6
    [ [0.0,0.0],[1.0,0.0],[0.0,1.0] ], #7
    [ [0.0,0.0],[1.0,0.0],[0.0,1.0],[1.0,1.0],[0.0,0.0] ], #8
    [ [1.0,0.0],[0.0,0.0],[0.0,0.5],[1.0,0.5],[1.0,0.0],[1.0,1.0] ], #9
    [ [0.5,0.0] ], #: part 1
    [ [0.5,1.0] ] ] #: part 2

print(paths)
def write(string,move,dx,dy,paths, wait=False):
    angs=[0.0 for i in range(4)]
    i=0
    for s in string:
        SCALE=2.0
        DEPTH=5.1
        if s==":":
            idxs = [10,11]
        else:
            idxs=[int(s)]
        for idx in idxs:
            path=np.array(paths[idx])*SCALE
            x,y=path[0]
            angs=move.IK2(-2,-(x+i+dx),y+dy,angs)
            move.motor(angs,1000)
            for p in path:
                x,y=p
                angs=move.IK2(-DEPTH,-(x+i+dx),y+dy,angs)
                print(angs)
                move.motor(angs,500)
            angs=move.IK2(-2,-(x+i+dx),y+dy,angs)
            print(angs)
            move.motor(angs,1000)
            if idxs[-1]==idx:
                i+=SCALE*1.25

move=Move()
move.home()
now = datetime.now()
time = now.strftime("%H:%M")
print(time)
time="9:36" #01:28 # 09:36
write(time,move,13,0,paths)
move.home()

        
