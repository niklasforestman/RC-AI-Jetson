#___________KOPIERTER TEIL
from pyPS4Controller.controller import Controller
from PyQt5 import QtCore
import time

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.Our_car_throttle = 0.0
        self.Our_car_brake = 0.0
        self.Our_car_steering = 0.0


    def on_R3_down(self, value):
        self.Our_car_throttle = 0.5 * (0.0000305185 * value + 1)
        print('throttle value: ', self.Our_car_throttle)
        #return throttle

    def on_R3_up(self, value):
        self.Our_car_throttle = 0.5 * (0.0000305185 * value + 1)
        print('throttle value: ', self.Our_car_throttle)
        #return throttle

    def on_L3_right(self, value):
        self.Our_car_steering = 0.0000305185 * value
        print('steering value', self.Our_car_steering)
        #return steering

    def on_L3_left(self, value):
        self.Our_car_steering = 0.0000305185 * value
        print(self.Our_car_steering)
        #return steering

    def on_R3_left(self, value):
        self.Our_car_brak = 0.5 * (0.0000305185 * value + 1)
        print('breaking value: ', self.Our_car_brak)
        #return brake

    def on_R3_right(self, value):
        self.Our_car_brak = 0.5 * (0.0000305185 * value + 1)
        print('breaking value: ', self.Our_car_brak)
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

if __name__ == "__main__":
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen()     #timeout=60)
