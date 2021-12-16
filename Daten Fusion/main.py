import cv2
import os
import csv
import numpy as np
import shutil
import re

fusions_daten = "fusions_daten"     # Ordnername mit den Bilder und der csv
dirname = os.path.dirname(__file__)
unter_ordner = os.listdir(dirname + "/" + fusions_daten)
print("Gefunde Ordner:", unter_ordner)

# bestehenden Output Ordner entfernen
if os.path.exists(dirname + "/Output"):
    shutil.rmtree(dirname + "/Output")

# Output Ordner neu erstellen
os.makedirs(dirname + "/Output")
os.makedirs(dirname + "/Output/img")

# CSV Datei erstellen
with open("Output/data.csv", mode='a+') as myCSV_file:  # oeffnet die CSV Datei mit Dateiname
    myCSV_writer = csv.writer(myCSV_file, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)  # legt die Synatx fuer die CSV fest
    myCSV_writer.writerow(['Index', 'Brake', 'Throttle', 'Steering'])  # schreibt diese Zeile in die CSV Datei al Header rein

counter = 0
for ordner in unter_ordner:     # Input Ordner durch gehen
    print("Ordner:", ordner, "wird kopiert")
    csv_path = dirname + "/" + fusions_daten + "/" + ordner + "/data.csv"
    images = os.listdir(dirname + "/" + fusions_daten + "/" + ordner + "/img", )  # liste aller Input Bilder
    images.sort(key=lambda f: int(re.sub('\D', '', f)))
    print(images)
    csv_inhalt = np.genfromtxt((csv_path), delimiter=',')    # input csv in Array lesen
    for index, line in enumerate(csv_inhalt):   # alle input Elemente des input Ordners duchgehen
        if index > 0:   # Kopzeile entfällt
            counter += 1
            with open("Output/data.csv", mode='a+') as myCSV_file:  # oeffnet die CSV Datei mit Dateiname
                myCSV_writer = csv.writer(myCSV_file, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)  # legt die Synatx fuer die CSV fest
                data = csv_inhalt[index]
                myCSV_writer.writerow([counter, data[1], data[2], data[3]])  # schreibt diese Zeile in die CSV Datei

            img = cv2.imread(dirname + "/" + fusions_daten + "/" + ordner + "/img/" + images[index-1])
            # normales Bild speichern
            cv2.imwrite(dirname + "/Output/img/" + str(counter) + ".jpg", img)

