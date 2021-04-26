from pyPS4Controller.controller import Controller
import time



throttle = 0
brake = 0
steering = 0

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_R3_down(self, value):
        throttle = 0.5*(0.0000305185*value + 1)
        print(throttle)

    def on_R3_up(self, value):
    
        throttle = 0.5*(0.0000305185*value + 1)
        print(throttle)

    def on_L3_right(self, value):
        steering = 0.0000305185*value 
        print(steering)

    def on_L3_left(self, value):
        steering = 0.0000305185*value
        print(steering)

    def on_R3_left(self, value):
        brake = 0.5*(0.0000305185*value + 1)
        print(brake)

    def on_R3_right(self, value):
    
        brake = 0.5*(0.0000305185*value + 1)
        print(brake)

        

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window

controller.listen(timeout=60)