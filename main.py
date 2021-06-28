import cv2
import sys
import multiprocessing
import time
import datetime
import os
import csv

from inc.CV_Format import init_camera, capture_camera, close_camera
from inc.Ps4Controller import MyController
from inc.SaveToCSV import init_CSV, save_data_to_CSV


global run_name
global save_path

# INIT + CONFIG
save_path = str('/home/STUD_ING_DATA/') #Speicherpfad
current_time = datetime.datetime.now()
run_name = current_time.strftime('%Y_%m_%d_%H_%M_%S') #Name des neuen Ordners, in dem die Bilder für den Run gespeichert werden


if not os.path.isdir(save_path + run_name):
    os.mkdir(save_path + run_name) # Ordner erstellen, falls nicht vorhanden
if not os.path.isdir(save_path + run_name + '/img'):
    os.mkdir(save_path + run_name + '/img') # Unterordner erstellen, falls nicht vorhanden

cap = init_camera() # Kameradienst starten / Kamera verbinden
if not cap:
    print('Kamera konnte nicht geoeffnet werden!') # Fehlermeldung falls Fehler bei Initialisierung der Kamera
    sys.exit()

index_image = 0 # Nutzung für Name des Bildes
loop_counter = 0 # Nicht mit jedem Durchlauf wird ein Bild gespeichert - umgeht pause
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False) #Klassenkonstruktor
init_CSV() #neue CSV erstellt und mit Kopfzeile beschrieben
while(True):

    k = cv2.waitKey(1)
    if k%256 == 27: # ESC pressed
        print("Escape hit, closing")
        break

    (brake, throttle, steering) = controller.output() # Controller Inputs auslesen
    #process_controlling=multiprocessing.Process(target=process_controlling()) #TODO: Controller Funktion
    
    if loop_counter == 4:
        # jeder fünfte Durchgang wird mit Bild und Controller Daten abgespeichert
        process_capture=multiprocessing.Process(target=capture_camera(cap, index_image))  # schnappt sich ein Bild
        save_data_to_CSV(index_image, brake, throttle, steering) # speichert Daten in CSV
        index_image += 1
        loop_counter = 0
    else:
        loop_counter += 1
    
    #process_controlling=multiprocessing.Process(target=process_controlling()) #TODO: Controller Funktion
    #CV_Format.capture_camera(cap) Capture
    time.sleep(0.02)

close_camera(cap)
