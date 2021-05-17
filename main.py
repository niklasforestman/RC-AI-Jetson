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

save_path = str('/home/maxi/STUD_ING_DATA/')
current_time = datetime.datetime.now()
run_name = current_time.strftime('%Y_%m_%d_%H_%M_%S')


if not os.path.isdir(save_path + run_name):
    os.mkdir(save_path + run_name)
if not os.path.isdir(save_path + run_name + '/img'):
    os.mkdir(save_path + run_name + '/img')

cap = init_camera()
if not cap:
    print('Kamera konnte nicht geoeffnet werden!')
    sys.exit()

index_image = 0
loop_counter = 0
controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
init_CSV()
while(True):
    (brake, throttle, steering) = controller.output()
    #process_controlling=multiprocessing.Process(target=process_controlling()) #TODO: Controller Funktion
    
    if loop_counter == 4:
        process_capture=multiprocessing.Process(target=capture_camera(cap, index_image))
        save_data_to_CSV(index_image, brake, throttle, steering)
        index_image += 1
        loop_counter = 0
    
    #process_controlling=multiprocessing.Process(target=process_controlling()) #TODO: Controller Funktion
    #CV_Format.capture_camera(cap) Capture
    loop_counter += 1
    time.sleep(0.02)

close_camera(cap)