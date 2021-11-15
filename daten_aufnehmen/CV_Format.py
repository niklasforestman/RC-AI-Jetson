import cv2
#import os



# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen

def init_camera():
    cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)480, height=(int)360,format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert !  appsink")
    if cap.isOpened():
        return cap
    return False

def capture_camera(cap, index_image, save_path, run_name):
    return_key, frame = cap.read()
    pfad = save_path + run_name +  '/img/' + str(index_image) + '.jpg'
    cv2.imwrite(pfad, frame)

def close_camera(cap):
    cap.release()
    cv2.destroyAllWindows()
