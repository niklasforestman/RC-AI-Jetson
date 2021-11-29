#___________KOPIERTER TEIL
from pyPS4Controller.controller import Controller
# hier ist die dokumentation von der library https://pypi.org/project/pyPS4Controller/


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.Our_car_throttle = 0.0
        self.Our_car_brake = 0.0
        self.Our_car_steering = 0.0
        self.modus_taste = 0


    def on_R3_down(self, value):
        self.Our_car_throttle = 0.5 * (0.0000305185 * value + 1)


    def on_R3_up(self, value):
        self.Our_car_throttle = 0.5 * (0.0000305185 * value + 1)


    def on_L3_right(self, value):
        self.Our_car_steering = 0.0000305185 * value


    def on_L3_left(self, value):
        self.Our_car_steering = 0.0000305185 * value


    def on_R3_left(self, value):
        self.Our_car_brake = 0.5 * (0.0000305185 * value + 1)


    def on_R3_right(self, value):
        self.Our_car_brake = 0.5 * (0.0000305185 * value + 1)


    def on_circle_press(self): # ist die x-Taste obwohl hier circle steht
        self.modus_taste = 1
    
    def on_x_press(self): # ist die viereck-Taste obwohl hier circle steht
        self.modus_taste = 0
 
#____________________

    def output(self):
        return self.Our_car_brake,  self.Our_car_throttle , self.Our_car_steering, self.modus_taste
    
#___________________



