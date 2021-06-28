import csv # benötigt um als .csv abspeichern zu können

global savepath
global run_name

def init_CSV():
    with open((savepath + run_name + '/data.csv'), mode='a+') as myCSV_file:  # oeffnet die CSV Datei mit Dateiname
        myCSV_writer = csv.writer(myCSV_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)  # legt die Synatx fuer die CSV fest
        myCSV_writer.writerow(['Index', 'Brake', 'Throttle', 'Steering'])  # schreibt diese Zeile in die CSV Datei al Header rein

def save_data_to_CSV(index, brake, throttle, steering):
    with open((savepath + run_name + '/data.csv'), mode='a+') as myCSV_file:  # oeffnet die CSV Datei mit Dateiname
        myCSV_writer = csv.writer(myCSV_file, delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)  # legt die Synatx fuer die CSV fest
        myCSV_writer.writerow([index, brake, throttle, steering])  # schreibt diese Zeile in die CSV Datei
