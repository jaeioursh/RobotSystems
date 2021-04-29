from sensor import Sensor, Interpretor
from motor import Motor
from time import sleep
import time

from readerwriterlock import rwlock
import concurrent.futures

class Bus:
    def __init__(self):
        self.lock=rwlock.RWLockWriteD()
        self.message=None

    def write(self,data):
        with self.lock.gen_wlock():
            self.message=data

    def read(self):
        with self.lock.gen_rlock():
            return self.message

def sensor_function(vals_bus,delay):
    sensor=Sensor()
    #lock=Lock()
    while 1:
        with lock:
            val=sensor.read_ground()
            vals_bus.write(val)
        time.sleep(delay)

def interpreter_function(vals_bus,interpret_bus,delay):
    inter=Interpretor(500,1.0)
    #lock=Lock()
    while 1:
        #with lock:
        val=vals_bus.read(val)
        new_val=inter.transform(val)
        interpret_bus.write(new_val)
        print(new_val)
        time.sleep(delay)

def control_function(interpret_bus,delay):
    motor=Motor()
    scale=20.0
    while 1:
        val=interpret_bus.read()
        motor.forward(20,-1.0*val*self.scale,delay)

if __name__ == "__main__":
    
    vals_bus=Bus()
    interpret_bus=Bus()
    sensor_delay=1.0
    interpreter_delay=1.0
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        eSensor=executor.submit(sensor_function,vals_bus,sensor_delay )
        eInterpreter=executor.submit(interpreter_function,vals_bus,interpret_bus,interpreter_delay)
    eSensor.result()
    eInterpreter.result()
