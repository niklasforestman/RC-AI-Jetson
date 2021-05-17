from PyQt5 import QtCore
import os
import pygame

# based on the sourcecode found in this repository:
# https://gist.github.com/claymcleod/028386b860b75e4f5472

class MyControllerThread_PYGAME(QtCore.QThread):
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




def printData(axis_data, button_data, hat_data):
    print(axis_data)        # oder save to .svg oder return, oder  aehnliches
    print(button_data)
    print(hat_data)

if __name__ == "__main__":
    myController = MyControllerThread_PYGAME
    myController.threadFinished.connect(printData)
    myController.start()

