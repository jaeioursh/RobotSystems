try :
    from ezblock import *
except ImportError :
    print (" This computer does not appear to be a PiCar - X system(/ opt / ezblock is not present ) . Shadowing hardware calls with substitute functions ")
    from sim_ezblock import *
from ezblock import __reset_mcu__
__reset_mcu__()

import time
import atexit
import math

time.sleep(0.01)

PERIOD = 4095
PRESCALER = 10
TIMEOUT = 0.02

dir_servo_pin = Servo(PWM('P2'))
camera_servo_pin1 = Servo(PWM('P0'))
camera_servo_pin2 = Servo(PWM('P1'))
left_rear_pwm_pin = PWM("P13")
right_rear_pwm_pin = PWM("P12")
left_rear_dir_pin = Pin("D4")
right_rear_dir_pin = Pin("D5")

S0 = ADC('A0')
S1 = ADC('A1')
S2 = ADC('A2')

Servo_dir_flag = 1
dir_cal_value = 0
cam_cal_value_1 = 0
cam_cal_value_2 = 0
motor_direction_pins = [left_rear_dir_pin, right_rear_dir_pin]
motor_speed_pins = [left_rear_pwm_pin, right_rear_pwm_pin]
cali_dir_value = [1, -1]
cali_speed_value = [0, 0]
#初始化PWM引脚
for pin in motor_speed_pins:
    pin.period(PERIOD)
    pin.prescaler(PRESCALER)

def set_motor_speed(motor, speed):
    global cali_speed_value,cali_dir_value
    motor -= 1
    if motor==1:
        speed*=0.9
    if speed >= 0:
        direction = 1 * cali_dir_value[motor]
    elif speed < 0:
        direction = -1 * cali_dir_value[motor]
    speed = abs(speed)
    if speed != 0:
        speed = int(speed )# + 50
    #speed = speed - cali_speed_value[motor]
    if direction < 0:
        motor_direction_pins[motor].high()
        motor_speed_pins[motor].pulse_width_percent(speed)
    else:
        motor_direction_pins[motor].low()
        motor_speed_pins[motor].pulse_width_percent(speed)

def motor_speed_calibration(value):
    global cali_speed_value,cali_dir_value
    cali_speed_value = value
    if value < 0:
        cali_speed_value[0] = 0
        cali_speed_value[1] = abs(cali_speed_value)
    else:
        cali_speed_value[0] = abs(cali_speed_value)
        cali_speed_value[1] = 0

def motor_direction_calibration(motor, value):
    # 0: positive direction
    # 1:negative direction
    global cali_dir_value
    motor -= 1
    if value == 1:
        cali_dir_value[motor] = -1*cali_dir_value[motor]


def dir_servo_angle_calibration(value):
    global dir_cal_value
    dir_cal_value = value
    set_dir_servo_angle(dir_cal_value)
    # dir_servo_pin.angle(dir_cal_value)

def set_dir_servo_angle(value):
    global dir_cal_value
    dir_servo_pin.angle(value+5)
def camera_servo1_angle_calibration(value):
    global cam_cal_value_1
    cam_cal_value_1 = value
    set_camera_servo1_angle(cam_cal_value_1)
    # camera_servo_pin1.angle(cam_cal_value)

def camera_servo2_angle_calibration(value):
    global cam_cal_value_2
    cam_cal_value_2 = value
    set_camera_servo2_angle(cam_cal_value_2)
    # camera_servo_pin2.angle(cam_cal_value)

def set_camera_servo1_angle(value):
    global cam_cal_value_1
    camera_servo_pin1.angle(-1 *(value+cam_cal_value_1))

def set_camera_servo2_angle(value):
    global cam_cal_value_2
    camera_servo_pin2.angle(-1 * (value+cam_cal_value_2))

def get_adc_value():
    adc_value_list = []
    adc_value_list.append(S0.read())
    adc_value_list.append(S1.read())
    adc_value_list.append(S2.read())
    return adc_value_list

def set_power(speed):
    set_motor_speed(1, speed)
    set_motor_speed(2, speed) 

def backward(speed):
    set_motor_speed(1, speed)
    set_motor_speed(2, speed)

def forward(speed,angle,t):
    set_dir_servo_angle(angle)
    if angle==0:
        set_motor_speed(1, speed) #right
        set_motor_speed(2, speed) #left

    else:
        ang=math.radians(angle)
        dir=angle/abs(angle)
        ang=abs(ang)
        adj=10.0/math.tan(ang)
        scale=(adj-6.0)/(adj+6.0)
        print(dir,scale)
    
        if dir>0:
            set_motor_speed(1, speed*scale) #right
            set_motor_speed(2, speed) #left
        else:
            set_motor_speed(1, speed) #right
            set_motor_speed(2, speed*scale) #left

    time.sleep(t)

def stop():
    set_motor_speed(1, 0)
    set_motor_speed(2, 0)


def Get_distance():
    timeout=0.01
    trig = Pin('D8')
    echo = Pin('D9')

    trig.low()
    time.sleep(0.01)
    trig.high()
    time.sleep(0.000015)
    trig.low()
    pulse_end = 0
    pulse_start = 0
    timeout_start = time.time()
    while echo.value()==0:
        pulse_start = time.time()
        if pulse_start - timeout_start > timeout:
            return -1
    while echo.value()==1:
        pulse_end = time.time()
        if pulse_end - timeout_start > timeout:
            return -2
    during = pulse_end - pulse_start
    cm = round(during * 340 / 2 * 100, 2)
    #print(cm)
    return cm

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


def test():
    #dir_servo_angle_calibration(-10) 
    #set_dir_servo_angle(-40)
    
    set_dir_servo_angle(0)
    time.sleep(1)
    kturn(-1)
def motor_stop():
    set_motor_speed(1, 0)
    set_motor_speed(2, 0)
    set_dir_servo_angle(0)


atexit.register(motor_stop)
#test()
while tricks() != 0:
    motor_stop()

# if __name__ == "__main__":
#     try:
#         # dir_servo_angle_calibration(-10) 
#         while 1:
#             test()
#     finally: 
#         stop()
