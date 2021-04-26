from pyPS4Controller.controller import Controller


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
       print("Hello world")

    def on_x_release(self):
       print("Goodbye world")
       print(throttle_max)
       print(throttle_min)

    def on_R3_up(self, value):
        throttle = value
        print(throttle)

    def on_R3_up(self, value):
        throttle_max = 0
        throttle_min = 0
        throttle = value
        print(throttle)
        if throttle_max <throttle:
            throttle_max = throttle
            
        if throttle_min > throttle:
            throttle_min = throttle
        



controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)

