import threading
import time
import datetime
import os
import sys
from adafruit_servokit import ServoKit
import board
import busio

from CV_Format import init_camera, capture_camera, close_camera
from Controller import MyController
from SaveToCSV import init_CSV, save_data_to_CSV


# global condition
condition = threading.Condition()

# global brake, throttle, steering
brake, throttle, steering = 0, 0, 0

# global modus # x-taste -> modus 1, viereck -> modus 0
modus = 0    # 0 = ruhezustand, 1 = Daten aufnehmen und servo output aktiv

save_path = str('/home/STUD_ING_DATA/')     # Speicherpfad
current_time = datetime.datetime.now()
run_name = current_time.strftime('%Y_%m_%d_%H_%M_%S')   # Name des neuen Ordners, in dem die Bilder für den Run gespeichert werden

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)

print("Initializing Servos")
i2c_bus0 = busio.I2C(board.SCL_1, board.SDA_1)
print("Initializing ServoKit")
servo_kit = ServoKit(channels=16, i2c=i2c_bus0)
print("Done initializing")


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
        self.modus_latch = 0
        self.index = 1

    def run(self):
        global brake, throttle, steering, modus  # made global here
        print(self.name, "started")
        while True:
            condition.acquire()
            (brake, throttle, steering, modus) = controller.output()  # Controller Inputs auslesen
            condition.release()

            # print("brake; ", brake, "throttle", throttle, "steering", steering)

            if modus == 1:
                brake, throttle, steering = 0, 0, 0

            servo_kit.servo[0].angle = 90 + 20 * throttle  # artificially csaling throttle by a factor of 20/90
            if brake > 0.1:
                servo_kit.servo[0].angle = 90 - 90*brake
            servo_kit.servo[1].angle = 90 + 90*steering


class Thread_C(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.last_time = 0
        self.image_index = 1

    def run(self):
        global brake, throttle, steering, modus  # made global here
        print(self.name, "started")
        init_CSV(save_path, run_name)
        while True:
            t = int(time.time() * 10)
            if t != self.last_time and modus == 1:
                condition.acquire()
                self.last_time = t
                save_data_to_CSV(self.image_index, brake, throttle, steering, save_path, run_name) # speichert Daten in CSV
                capture_camera(cap, self.image_index, save_path, run_name)
                condition.release()
                self.image_index += 1


if not os.path.isdir(save_path + run_name):
    os.makedirs(save_path + run_name)      # Ordner erstellen, falls nicht vorhanden
if not os.path.isdir(save_path + run_name + '/img'):
    os.mkdir(save_path + run_name + '/img')     # Unterordner erstellen, falls nicht vorhanden

cap = init_camera()  # Kameradienst starten / Kamera verbinden
if not cap:
    print('Kamera konnte nicht geoeffnet werden!')  # Fehlermeldung falls Fehler bei Initialisierung der Kamera
    sys.exit()

a = Thread_A("myThread_controller_listen")
b = Thread_B("myThread_pwm_out")
c = Thread_C("myThread_write_data")

b.start()
a.start()
c.start()

a.join()
b.join()
c.join()

close_camera(cap)
