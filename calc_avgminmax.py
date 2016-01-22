#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Dieses Script liest die vorhandene Datei 'sht21-data.csv' ein und berechnet
 Durschnitt, Minimum und Maximum für die aufgezeichnete Temperatur und Luft-
 feuchtigkeit.

 (c) 2016 Tronde <tronde(aet)my-it-brain(Punkt)de>
 Lizenz: GPLv3
"""

import argparse, csv, sys

sourcefile = 'sht21-data.csv'
liste = []
lastitem = -1	# Bestimmt das letzte Element einer Liste
tempitem = 2	# Bestimmt den Temperaturwert innerhalb der Liste
humditem = 3	# Bestimmt den Luftfeuchtigkeitswert innerhalb der Liste
temperature = []
min_temp = 0
max_temp = 0
humidity = []
min_humid = 0
max_humid = 0

def debug():
    print ("Durchschnittstemperatur: %2.1f°C." % temp_avg)
    print ("Minimum: %2.1f°C" % min_temp)
    print ("Maximum: %2.1f°C" % max_temp)
    print ("Durchschnittliche Luftfeuchtigkeit: %d%% RH." % humid_avg)
    print ("Minimum: %d%% RH." % min_humid)
    print ("Maximum: %d%% RH." % max_humid)

parser = argparse.ArgumentParser(description=" Dieses Script liest die vorhandene Datei 'sht21-data.csv' ein und berechnet Durschnitt, Minimum und Maximum für die aufgezeichnete Temperatur und Luftfeuchtigkeit.")

parser.add_argument("-v", "--verbose", action="store_true", help="Aktiviert Debuggingausgabe.")

args = parser.parse_args()

with open(sourcefile, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        liste.append(row)
        temperature.append(float(liste[lastitem][tempitem]))
        humidity.append(int(liste[lastitem][humditem]))

temp_sum = sum(temperature)
temp_len = len(temperature)
temp_avg = temp_sum / temp_len
humid_sum = sum(humidity)
humid_len = len(humidity)
humid_avg = humid_sum / humid_len
min_temp = min(temperature)
max_temp = max(temperature)
min_humid = min(humidity)
max_humid = max(humidity)

if args.verbose:
    debug()

def writestatsincsv(temp_avg,min_temp,max_temp,humid_avg,min_humid,max_humid):
    row = temp_avg + "," + min_temp + "," + max_temp + "," + humid_avg + "," + min_humid + "," + max_humid + "\n"
    f = open('statistic_data.csv', 'w')
    f.write(row)
    f.close()
writestatsincsv(str("%2.1f" % temp_avg),str("%2.1f" % min_temp),str("%2.1f" % max_temp),str("%d" % humid_avg),str("%d" % min_humid),str("%d" % max_humid))

sys.exit(0)
