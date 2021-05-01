import cv2
import os


# gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values: 0 and 2)
# display_width and display_height determine the size of the window on the screen


def save_images(path):
    # To flip the image, modify the flip_method parameter (0 and 2 are the most common)
    print(gstreamer_pipeline(flip_method=0))
    i = 1  # Laufvariable für die Dateibenennung
    #cap = cv2.VideoCapture( gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    cap = cv2.VideoCapture("nvarguscamerasrc ! video/x-raw(memory:NVMM), width=(int)480, height=(int)360,format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv ! video/x-raw, format=(string)BGRx ! videoconvert !  appsink")
    if cap.isOpened():
        window_handle = cv2.namedWindow("CSI Camera", cv2.WINDOW_AUTOSIZE)
        # Window

        while True:
            return_key, frame = cap.read()
            cv2.imshow("CSI Camera", frame)
            pfad = str('/home/maxi/STUD_ING_DATA/' + str(i) + '.jpg')
            cv2.imwrite(pfad, frame)
            k = cv2.waitKey(10)
            #print(cap)
            #print(frame)
            if k % 256 == 27:  # ESC pressed
                print("Escape hit, closing...")
                break
            i = i + 1  # Die Laufvariable wird für die Dateibenennung verwendet
            print(f"Das {i}-te Bild wurde gerade gespeichert")

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Unable to open camera")


if __name__ == "__main__":
    path = '/home/STUD_ING_DATA/'
    save_images(path)
