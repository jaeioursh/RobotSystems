try :
    from ezblock import *
except ImportError :
    print (" This computer does not appear to be a PiCar - X system(/ opt / ezblock is not present ) . Shadowing hardware calls with substitute functions ")
    from sim_ezblock import *
from ezblock import __reset_mcu__


import time
import atexit
import math



class Motor:
    def __init__(self)

        self.DRIVE_SCALE=0.9
        self.DIRECTION_OFFSET=5

        PERIOD = 4095
        PRESCALER = 10
        TIMEOUT = 0.02

        self.dir_servo_pin = Servo(PWM('P2'))
        self.camera_servo_pin1 = Servo(PWM('P0'))
        self.camera_servo_pin2 = Servo(PWM('P1'))
        self.left_rear_pwm_pin = PWM("P13")
        self.right_rear_pwm_pin = PWM("P12")
        self.left_rear_dir_pin = Pin("D4")
        self.right_rear_dir_pin = Pin("D5")

        self.S0 = ADC('A0')
        self.S1 = ADC('A1')
        self.S2 = ADC('A2')

        self.Servo_dir_flag = 1
        self.dir_cal_value = 0

        self.motor_direction_pins = [self.left_rear_dir_pin, self.right_rear_dir_pin]
        self.motor_speed_pins = [self.left_rear_pwm_pin, self.right_rear_pwm_pin]
        self.cali_dir_value = [1, -1]
        self.cali_speed_value = [0, 0]
        #初始化PWM引脚
        for pin in self.motor_speed_pins:
            pin.period(PERIOD)
            pin.prescaler(PRESCALER)

        atexit.register(self.cleanup)

    def set_motor_speed(self,motor, speed):
       
        motor -= 1
        if motor==1:
            speed*=self.DRIVE_SCALE
        if speed >= 0:
            direction = 1 * self.cali_dir_value[motor]
        elif speed < 0:
            direction = -1 * self.cali_dir_value[motor]
        speed = abs(speed)
        if speed != 0:
            speed = int(speed )# + 50
        #speed = speed - cali_speed_value[motor]
        if direction < 0:
            self.motor_direction_pins[motor].high()
            self.motor_speed_pins[motor].pulse_width_percent(speed)
        else:
            self.motor_direction_pins[motor].low()
            self.motor_speed_pins[motor].pulse_width_percent(speed)


    def set_dir_servo_angle(self,value):
        self.dir_servo_pin.angle(value+self.DIRECTION_OFFSET)


    def set_camera_servo1_angle(self,value):
        self.camera_servo_pin1.angle(-1 *(value))

    def set_camera_servo2_angle(self,value):
        self.camera_servo_pin2.angle(-1 * (value))

    def get_adc_value(self):
        adc_value_list = []
        adc_value_list.append(self.S0.read())
        adc_value_list.append(self.S1.read())
        adc_value_list.append(self.S2.read())
        return adc_value_list

    def set_power(self,speed):
        self.set_motor_speed(1, speed)
        self.set_motor_speed(2, speed) 

    def backward(self,speed):
        self.set_motor_speed(1, speed)
        self.set_motor_speed(2, speed)

    def forward(self,speed,angle,t):
        self.set_dir_servo_angle(angle)
        if angle==0:
            self.set_motor_speed(1, speed) #right
            self.set_motor_speed(2, speed) #left

        else:
            ang=math.radians(angle)
            dir=angle/abs(angle)
            ang=abs(ang)
            adj=10.0/math.tan(ang)
            scale=(adj-6.0)/(adj+6.0)
            print(dir,scale)
        
            if dir>0:
                self.set_motor_speed(1, speed*scale) #right
                self.set_motor_speed(2, speed) #left
            else:
                self.set_motor_speed(1, speed) #right
                self.set_motor_speed(2, speed*scale) #left

        time.sleep(t)

    def stop(self):
        self.set_motor_speed(1, 0)
        self.set_motor_speed(2, 0)
        
    def cleanup(self):
        self.stop()

    def Get_distance(self):
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



if __name__ == "__main__":
    __reset_mcu__()
    time.sleep(0.01)

#     try:
#         # dir_servo_angle_calibration(-10) 
#         while 1:
#             test()
#     finally: 
#         stop()
