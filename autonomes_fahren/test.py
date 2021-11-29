import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from tensorflow import keras
import cv2
from CV_Format import init_camera, capture_camera, close_camera
import sys

def img_preprocess(img):
    #img = img[60:135,:,:] #Das Bild kann zugeschnitten werden auf einen bestimmten Bereich
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV) #colormap für NVIDIA-Model
    #img = cv2.GaussianBlur(img,  (3, 3), 0) #Blur um Bild zu smoothen
    img = cv2.resize(img, (200, 66)) #Auf richtige Größe für Model bringen
    img = img/255 #Bild normalisieren
    return img

print("start")

cap = init_camera() # Kameradienst starten / Kamera verbinden
if not cap:
    print('Kamera konnte nicht geoeffnet werden!')  # Fehlermeldung falls Fehler bei Initialisierung der Kamera
    sys.exit()

print("Kamera ist init")

print("Tesnorflow Model wird geladen")
model = keras.models.load_model("model.h5")
print("Tensorflow Model ist geladen")

print(model.layers[0].input_shape)
print(model.summary())


while True:
    return_key, im = cap.read()
    
    im = img_preprocess(im)

    im = np.expand_dims(im, axis=0)

    model_output = model.predict(im)

    steering_value = model_output[0][0]
    throttle_value = model_output[0][1]

    print("steering value:", steering_value, "throttle value:", throttle_value)


print("end")