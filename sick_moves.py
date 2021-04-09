from picarx_improved import *
import time

def parallel(dir):
    forward(90,20*dir,0.5)    
    forward(90,-15*dir,0.7)
    forward(-90,0,1.2)
def kturn(dir):
    forward(90,40*dir,1.0)    
    forward(-90,-40*dir,1.0)
    forward(90,0,1.0)

def tricks():
    print("1) turn left")
    print("2) turn right")
    print("3) forward")
    print("4) reverse")
    print("5) parallel left")
    print("6) parallel right")
    print("7) kturn left")
    print("8) kturn right")
    x=input(" ")
    
    if x=="1":
        forward(80,-20,2)
        return 1 
    if x=="2":
        forward(80,20,2)
        return 2 
    if x=="3":
        forward(80,0,2)
        return 3 
    if x=="4":
        forward(-80,0,2)
        return 4 
    if x=="5":
        parallel(-1.0)
        return 5  
    if x=="6":
        parallel(1.0)
        return 6 
    if x=="7":
        kturn(-1.0)
        return 7 
    if x=="8":
        kturn(1.0)
        return 8 
    return 0



def motor_stop():
    set_motor_speed(1, 0)
    set_motor_speed(2, 0)
    set_dir_servo_angle(0)



while tricks() != 0:
    motor_stop()

# if __name__ == "__main__":
#     try:
#         # dir_servo_angle_calibration(-10) 
#         while 1:
#             test()
#     finally: 
#         stop()
