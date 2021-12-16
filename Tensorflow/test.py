import cv2
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import keras
import cv2
import re
import pandas as pd
import ntpath
import random


def img_preprocess(img):
    #img = img[60:135,:,:] #Das Bild kann zugeschnitten werden auf einen bestimmten Bereich
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV) #colormap für NVIDIA-Model
    #img = cv2.GaussianBlur(img,  (3, 3), 0) #Blur um Bild zu smoothen
    img = cv2.resize(img, (100, 100)) #Auf richtige Größe für Model bringen
    img = img/255 #Bild normalisieren
    return img


print("start")


# print(len(im))
# print(len(im[0]))
# print(len(im[0][0]))
# print(len(im[0][0][0]))

model = keras.models.load_model("model.h5")

print(model.layers[0].input_shape)
print(model.summary())

dirname = os.path.dirname(__file__)
imagepath = dirname + "/daten/img"
images = os.listdir(imagepath)
print(images)
images.sort(key=lambda f: int(re.sub('\D', '', f)))
print(images)
true_data = np.genfromtxt(("daten/data.csv"), delimiter=',')    # alte csv in Array lesen
true_data = np.delete(true_data, 0, axis=0)     # labels entfernen

steering_plot = []
throttle_plot = []

counter = 0
for image in images:
    im = mpimg.imread("daten/img/" + image)

    im = img_preprocess(im)

    # plt.imshow(im)
    # plt.show()

    im = np.expand_dims(im, axis=0)

    model_output = model.predict(im)

    steering_value = model_output[0][0]
    steering_plot.append(steering_value)
    try:
        print("Image:", image, "steering value:", steering_value, ", true value: ", true_data[counter][3])
        throttle_plot.append(true_data[counter][3])
    except IndexError:
        pass
    counter += 1



plt.plot(steering_plot)
plt.plot(throttle_plot)
plt.legend(["model", "true"])
#plt.plot(throttle_plot)
plt.show()

print("end")