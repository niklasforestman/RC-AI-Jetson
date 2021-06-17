#___________KOPIERTER TEIL
from pyPS4Controller.controller import Controller
from PyQt5 import QtCore
import time
from adafruit_servokit import ServoKit
import board
import busio

# hier ist die dokumentation von der library https://pypi.org/project/pyPS4Controller/

throttle = 90.0
brake = 90.0
steering = 90.0



class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.Our_car_throttle = 90.0
        self.Our_car_brake = 90.0
        self.Our_car_steering = 0.0


    def on_R3_down(self, value):
        self.Our_car_throttle = 0.5 * (0.0000305185 * value + 1)
        #kit.servo[0].angle= 90 + 90 * self.Our_car_throttle
        controllValues(throttle = self.Our_car_throttle )
        print('throttle value: ', self.Our_car_throttle*90)
        #return throttle

    def on_R3_up(self, value):
        self.Our_car_throttle = 0.5 * (0.0000305185 * value + 1)
        #kit.servo[0].angle= 90 + 90 * self.Our_car_throttle
        controllValues(throttle = self.Our_car_throttle)

        print('throttle value: ', self.Our_car_throttle*90)
        #return throttle

    def on_L3_right(self, value):
        self.Our_car_steering = 0.0000305185 * value
        controllValues(steering =  self.Our_car_steering)

        print('steering value', self.Our_car_steering)
        #return steering

    def on_L3_left(self, value):
        self.Our_car_steering = 0.0000305185 * value
        controllValues(steering =  self.Our_car_steering)

        print('steering value', self.Our_car_steering)
        #return steering

    def on_R3_left(self, value):
        self.Our_car_brake = 0.5 * (0.0000305185 * value + 1)
        #kit.servo[0].angle= 90 - 90 * self.Our_car_brake
        controllValues(brake = self.Our_car_brake)

        print('breaking value: ', self.Our_car_brake*-90)
        #return brake

    def on_R3_right(self, value):
        self.Our_car_brake = 0.5 * (0.0000305185 * value + 1)
        #kit.servo[0].angle= 90 - 90 * self.Our_car_brake
        controllValues(brake = self.Our_car_brake)

        print('breaking value: ', self.Our_car_brake*-90)
        #return brake

#____________________
    '''
    def output(self):
        brake = self.on_R3_left(self.event.value) + self.on_R3_right(self.event.value)
        throttle = self.on_R3_down(self.event.value) + self.on_R3_up(self.event.value)
        steering = self.on_L3_left(self.event.value) + self.on_L3_right(self.event.value)

        return brake, throttle, steering
    '''
#___________________


def controllValues(**kwargs):
    print("calling controllValue")
    for key, value in kwargs.items():
        if key == "throttle":
            print("key throttle detected")
            throttle = value
            kit.servo[0].angle = 90 + 90 * throttle

        if key == "brake":
            print("key brake detected")

            brake = value
            kit.servo[0].angle = 90 - 90 * brake

        if key == "steering":
            steering = value
            kit.servo[1].angle = 90 + 90 * steering
            
    
    



if __name__ == "__main__":
    print("Initializing Servos")
    i2c_bus0=(busio.I2C(board.SCL_1, board.SDA_1))
    print("Initializing ServoKit")
    kit = ServoKit(channels=16, i2c=i2c_bus0)
    print("Done initializing")


    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()     #timeout=60)
