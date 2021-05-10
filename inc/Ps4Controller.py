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
        return throttle

    def on_R3_up(self, value):
    
        throttle = 0.5*(0.0000305185*value + 1)
        print(throttle)
        return throttle
    def on_L3_right(self, value):
        steering = 0.0000305185*value 
        print(steering)
        return steering
    def on_L3_left(self, value):
        steering = 0.0000305185*value
        print(steering)
        return steering
    def on_R3_left(self, value):
        brake = 0.5*(0.0000305185*value + 1)
        print(brake)
        return brake
    def on_R3_right(self, value):
    
        brake = 0.5*(0.0000305185*value + 1)
        print(brake)
        return brake
    def output(self):

        brake= self.on_R3_left(self.event.value) + self.on_R3_right(self.event.value)
        throttle = self.on_R3_down(self.event.value) + self.on_R3_up(self.event.value)
        steering =  self.on_L3_left(self.event.value) + self.on_L3_right(self.event.value)

        return brake, throttle, steering
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window

controller.listen(timeout=60)
print(controller.output())
