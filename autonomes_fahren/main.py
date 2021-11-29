# bei Session error die Kaera zurück setzen:
# sudo service nvargus-daemon restart

import threading
import sys
from adafruit_servokit import ServoKit
import board
import busio
import cv2
import numpy as np
from tensorflow import keras

from CV_Format import init_camera, capture_camera, close_camera
from Controller import MyController
#from SaveToCSV import init_CSV, save_data_to_CSV

CUDA_VISIBLE_DEVICES = ""

condition = threading.Condition()

brake, throttle, steering = 0, 0, 0

modus = 1

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)

print("Initializing Servos")
i2c_bus0 = busio.I2C(board.SCL_1, board.SDA_1)
print("Initializing ServoKit")
servo_kit = ServoKit(channels=16, i2c=i2c_bus0)
print("Done initializing")


def img_preprocess(img):
    #img = img[60:135,:,:] #Das Bild kann zugeschnitten werden auf einen bestimmten Bereich
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV) #colormap für NVIDIA-Model
    #img = cv2.GaussianBlur(img,  (3, 3), 0) #Blur um Bild zu smoothen
    img = cv2.resize(img, (200, 66)) #Auf richtige Größe für Model bringen
    img = img/255 #Bild normalisieren
    return img


class Thread_A(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global brake, throttle, steering  # made global here
        print(self.name, "started")
        controller.listen()
        print("FLAG")

class Thread_B(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global brake, throttle, steering, modus  # made global here
        print(self.name, "started")
        while True:

            if modus == 1:
                condition.acquire()
                (brake, throttle, steering, modus) = controller.output()  # Controller Inputs auslesen
                condition.release()
            else:
                condition.acquire()
                (brake, throttle, steering_trash, modus) = controller.output()  # Controller Inputs auslesen
                condition.release()
                print(steering)

            servo_kit.servo[0].angle = 90 + 20 * throttle  # artificially csaling throttle by a factor of 20/90

            if brake > 0.1:
                servo_kit.servo[0].angle = 90 - 90 * brake
            servo_kit.servo[1].angle = 90 + 90 * steering


class Thread_C(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global brake, throttle, steering, cap, model, modus  # made global here
        while True:
            if modus == 0:
                return_key, frame = cap.read()

                img = img_preprocess(frame)

                img = np.expand_dims(img, axis=0)

                model_output = model.predict(img)

                steering_value = model_output[0][0]
                throttle_value = model_output[0][1]
                steering_value = max(-1,min(1, steering_value))
                # print(steering_value)

                condition.acquire()
                # throttle = 1
                steering = steering_value
                condition.release()

                # Ausgabe des NNN in Globale Variable schreiben


model = keras.models.load_model("model.h5")

cap = init_camera() # Kameradienst starten / Kamera verbinden
if not cap:
    print('Kamera konnte nicht geoeffnet werden!')  # Fehlermeldung falls Fehler bei Initialisierung der Kamera
    sys.exit()

a = Thread_A("myThread_controller_listen")
b = Thread_B("myThread_pwm_out")
c = Thread_C("NNN auswerten")

a.start()
b.start()
c.start()

a.join()
b.join()
c.join()

close_camera(cap)