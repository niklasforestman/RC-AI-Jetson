import csv # benötigt um als .csv abspeichern zu können

# ----------------SETUP CODE FueR CSV-----------
# hier muss die CSV Datei mit einem Namen inittialisiert werden

dateiName = '/Users/timkayser/Documents/ProgrammSupport/PyCharm/reentry/csvFiles/' + label + '_EXACT.csv'  # dateiName = 'csvFiles/' + label + '.csv'


with open(dateiName, mode='w') as myCSV_file:  # oeffnet die CSV Datei mit Dateiname
    myCSV_writer = csv.writer(myCSV_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)  # legt die Synatx fuer die CSV fest
    myCSV_writer.writerow(['steeringAngle', 'throttle'])  # schreibt diese Zeile in die CSV Datei al Header rein

# ----------------SETUP CODE FueR CSV-----------


# ----------------CODE FueR CSV LOOP-----------
# Hier muss der Teil zum Abspeichern der laufenden Variablen in die CSV rein
with open(dateiName, mode='a') as myCSV_file:  # oeffnet die CSV Datei
    myCSV_writer = csv.writer(myCSV_file, delimiter=',', quotechar='"',quoting=csv.QUOTE_MINIMAL)  # legt die Synatx fuer die CSV fest
    myCSV_writer.writerow([mySteeringAngle, myThrottle)  # schreibt diese Zeile in die CSV Datei
# ----------------ENDE der CSV LOOP-----------

