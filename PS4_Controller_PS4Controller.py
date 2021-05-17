#___________KOPIERTER TEIL
from pyPS4Controller.controller import Controller
import time

throttle = 0
brake = 0
steering = 0


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_R3_down(self, value):
        throttle = 0.5 * (0.0000305185 * value + 1)
        print(throttle)
        return throttle

    def on_R3_up(self, value):
        throttle = 0.5 * (0.0000305185 * value + 1)
        print(throttle)
        return throttle

    def on_L3_right(self, value):
        steering = 0.0000305185 * value
        print(steering)
        return steering

    def on_L3_left(self, value):
        steering = 0.0000305185 * value
        print(steering)
        return steering

    def on_R3_left(self, value):
        brake = 0.5 * (0.0000305185 * value + 1)
        print(brake)
        return brake

    def on_R3_right(self, value):
        brake = 0.5 * (0.0000305185 * value + 1)
        print(brake)
        return brake

#____________________
    def output(self):
        brake = self.on_R3_left(self.event.value) + self.on_R3_right(self.event.value)
        throttle = self.on_R3_down(self.event.value) + self.on_R3_up(self.event.value)
        steering = self.on_L3_left(self.event.value) + self.on_L3_right(self.event.value)

        return brake, throttle, steering
#___________________


class MyControllerThread_PS4lib(QtCore.QThread):
    threadFinished = QtCore.pyqtSignal(float, float, float)

    def __init__(self):
        super().__init__()

        self.controller = None
        self.axis_data = None
        self.button_data = None
        self.hat_data = None

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        # create instance of controller object
        #self.solver = solver

    def run(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value, 2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

                os.system('clear')

                self.threadFinished.emit(self.axis_data, self.button_data, self.hat_data )


if __name__ == "__main__":
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)

    controller.listen(timeout=60)
    print(controller.output())
