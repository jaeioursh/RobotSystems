from move import Move
import numpy as np

paths=[
    [ [0.0,0.0],[1.0,0.0],[1.0,1.0],[0.0,1.0],[0.0,0.0] ], #0
    [ [0.5,0.0],[0.5,1.0] ], # 1
    [ [0.0,0.0],[1.0,0.0],[0.0,1.0],[1.0,1.0] ], #2
    [ [0.0,0.0],[1.0,0.0],[0.0,0.5],[1.0,1.0],[0.0,1.0] ], #3
    [ [0.0,0.0],[0.0,0.5],[1.0,0.5],[1.0,0.0],[1.0,1.0] ], #4
    [ [1.0,0.0],[0.0,0.0],[0.0,0.5],[1.0,1.0],[0.0,1.0] ], #5
    [ [1.0,0.0],[0.0,0.0],[0.0,1.0],[1.0,1.0],[1.0,0.5],[0.0,0.5] ], #6
    [ [0.0,0.0],[1.0,0.0],[0.0,1.0] ], #7
    [ [0.0,0.0],[1.0,0.0],[0.0,1.0],[1.0,1.0],[0.0,0.0] ], #8
    [ [1.0,0.0],[0.0,0.0],[0.0,0.5],[1.0,0.5],[1.0,0.0],[1.0,1.0] ] ] #9

print(paths)
def write(string,move,dx,dy,paths):
    angs=[0.0 for i in range(4)]
    i=0
    for s in string:
        
        idx=int(s)
        path=paths[idx]
        x,y=path[0]
        angs=move.IK2(0,-(x+i+dx),y+dy,angs)
        move.motor(angs,1000)
        for p in path:
            x,y=p
            angs=move.IK2(-1,-(x+i+dx),y+dy,angs)
            print(angs)
            move.motor(angs,500)
        angs=move.IK2(0,-(x+i+dx),y+dy,angs)
        print(angs)
        move.motor(angs,1000)
        i+=1

move=Move()
write("012",move,20,0,paths)
move.home()

        
