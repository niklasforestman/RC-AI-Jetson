import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import keras
import tensorflow
from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Conv2D, Convolution2D, MaxPooling2D, Dropout, Flatten, Dense
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from imgaug import augmenters as iaa
import cv2
import pandas as pd
import ntpath
import random


def zoom(image):
    zoom = iaa.Affine(scale=(1, 1.3)) #Zoom mit scale, Affine sorgt dafür, dass Linien im Bild erhalten bleiben
    image = zoom.augment_image(image) #Apply die Zoom-Parameter auf das Bild
    return image


# Verschieben des Bildes
def pan(image):
    pan = iaa.Affine(translate_percent= {"x" : (-0.1, 0.1), "y": (-0.1, 0.1)})
    image = pan.augment_image(image)
    return image


# Rotieren des Bildes
def rotate(image):
    rotate = iaa.Affine(translate_percent= {"x" : (-0.1, 0.1), "y": (-0.1, 0.1)})
    # image = pan.augment_image(image)
    return image


# Helligkeit eines Bildes verändern
def img_random_brightness(image):
    brightness = iaa.Multiply((0.2, 1.2))
    image = brightness.augment_image(image)
    return image


# Farben eines Bildes verändern
def img_random_color(image):
    # brightness = iaa.Multiply((0.2, 1.2))
    # image = brightness.augment_image(image)
    return image


# Ein Bild wird gespiegelt
def img_random_flip(image, steering_angle):
    image = cv2.flip(image,1)
    steering_angle = -steering_angle
    return image, steering_angle


def random_augment(image, steering_angle):
    image = mpimg.imread(image)
    if np.random.rand() < 0.5:
        image = pan(image)
    if np.random.rand() < 0.5:
        image = zoom(image)
    if np.random.rand() < 0.5:
        image = img_random_brightness(image)
    if np.random.rand() < 0.5:
        image, steering_angle = img_random_flip(image, steering_angle)

    return image, steering_angle


def img_preprocess(img):
    #img = img[60:135,:,:] #Das Bild kann zugeschnitten werden auf einen bestimmten Bereich
    img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV) #colormap für NVIDIA-Model
    #img = cv2.GaussianBlur(img,  (3, 3), 0) #Blur um Bild zu smoothen
    img = cv2.resize(img, (200, 66)) #Auf richtige Größe für Model bringen
    img = img/255 #Bild normalisieren
    return img


def batch_generator(image_paths, steering_ang, batch_size, istraining): #, throttle_list
    while True:
        batch_img = []
        batch_steering = []
        batch_throttle = []
        for i in range(batch_size):

            random_index = random.randint(0, len(image_paths) - 1)

            if istraining:  # falls die Funktion im Modelltraining aufgerufen werden soll, dann sollen die Bilder augmentiert werden
                im = mpimg.imread(image_paths[random_index])
                steering = steering_ang[random_index]
                # throttle = throttle_list[random_index]
            else:
                print('die Einstellung für istraining ist falsch gewählt"')

            im = img_preprocess(im)
            batch_img.append(im)
            batch_steering.append(steering)
            # batch_throttle.append(throttle)

        yield (np.asarray(batch_img), np.asarray(batch_steering))   # , np.asarray(batch_throttle))


def nvidia_model():
    model = Sequential()
    model.add(Conv2D(24, kernel_size=(5, 5), strides=(2, 2), input_shape=(66, 200, 3), activation='relu'))
    model.add(Conv2D(36, kernel_size=(5, 5), strides=(2, 2), activation='relu'))
    model.add(Conv2D(48, kernel_size=(5, 5), strides=(2, 2), activation='relu'))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(Dropout(0.5))

    model.add(
        Flatten())  # Mit Flatten wird aus den feature maps eine aneinanderreihung von Knoten erstellt, die im nächsten fully-connected layer verarbeitet werden

    model.add(Dense(100, activation='elu'))  # elu ist kein Schreibfehler
    #   model.add(Dropout(0.5))

    model.add(Dense(50, activation='elu'))  # elu verhindert ein dead-relu
    #   model.add(Dropout(0.5))

    model.add(Dense(10, activation='elu'))
    #   model.add(Dropout(0.5))

    model.add(Dense(2))  # Der letzte Layer hat zwei Knoten, einmal für steering_angle und einmal für Gas/Bremse

    optimizer = Adam(lr=1e-3)
    model.compile(loss='mse', optimizer=optimizer)  # Mean Squared Error
    return model


def load_img_steering(datadir, data):
    image_path = []
    steering = []
    throttle = []
    brake = []
    for i in range(len(data)):
        indexed_data = data.iloc[i]  # indexed_data ist nur eine Zeile  der ganzen Tabelle
        image_path.append(os.path.join(datadir, str(int(indexed_data[0])) + '.jpg'))
        # image_path.append(indexed_data[0]) #
        brake.append(float(indexed_data[1]))
        throttle.append(float(indexed_data[2]))
        steering.append(float(indexed_data[3]))

    image_paths = np.asarray(image_path)
    steerings = np.asarray(steering)
    throttle = np.asarray(throttle)
    return image_paths, steerings, throttle


def img_preprocess(img):
    #img = img[60:135,:,:] #Das Bild kann zugeschnitten werden auf einen bestimmten Bereich
  img = cv2.cvtColor(img, cv2.COLOR_RGB2YUV) #colormap für NVIDIA-Model
    #img = cv2.GaussianBlur(img,  (3, 3), 0) #Blur um Bild zu smoothen
  img = cv2.resize(img, (200, 66)) #Auf richtige Größe für Model bringen
  img = img/255 #Bild normalisieren
  return img


data = pd.read_csv("daten/data.csv", sep=',') #sep = ';' falls mit ; getrennt

image_paths, steerings, throttle = load_img_steering('daten/img/', data)

combined_data = [steerings, throttle]

combined_data = np.swapaxes(combined_data, 0, 1)    #tauscht die Achsen des Arrays

# Train-Test-Split durchführen
# statt steerings später combined data, Modell muss aber angepasst werden
X_train, X_valid, y_train, y_valid = train_test_split(image_paths, steerings, test_size=0.2, random_state=6)

model = nvidia_model()
print(model.summary())

# Hier könnte man ein earyl-stopping integrieren, dass das Training abgebrochen wird, wenn die Validation_loss wieder steigt
early_stopping_callback = tensorflow.keras.callbacks.EarlyStopping(monitor='val_loss', patience=4, restore_best_weights=True, verbose=1)
batch_size = 50 # willkürlich auf 50
history = model.fit(batch_generator(X_train, y_train, batch_size, 1),
                                  steps_per_epoch=int(len(X_train)/batch_size), # Die gesamte Anzahl an Bildern geteilt durch die batch_size, mit der der batch_generator aufgerufen wird, ist die Anzahl wie oft das Training aufgerufen wird
                                  validation_data=batch_generator(X_valid, y_valid, 10, 1), #validation funktioniert noch nicht
                                  validation_steps=10, # so oft wird der batch_generator aufgerufen, um zu validieren https://stackoverflow.com/questions/45943675/meaning-of-validation-steps-in-keras-sequential-fit-generator-parameter-list
                                  epochs=10,
                                  callbacks=[early_stopping_callback],
                                  verbose=1,
                                  shuffle = 1)

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['training', 'validation'])
plt.title('Loss')
plt.xlabel('Epoch')
plt.show()

model.save('model.h5') #Hier kann das Modell gespeichert werden, um es später zu verwenden
print("ende")