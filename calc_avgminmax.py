#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
 Dieses Script liest die vorhandene Datei 'sht21-data.csv' ein und berechnet
 Durschnitt, Minimum und Maximum für die aufgezeichnete Temperatur und Luft-
 feuchtigkeit.

 (c) 2016 Tronde <tronde(aet)my-it-brain(Punkt)de>
 Lizenz: GPLv3
"""

import argparse
import csv
import sys

sourcefile = 'sht21-data.csv'
liste = []      # Nimmt den Inhalt von sourcefile auf
firstitem = 0   # Erstes Element einer Liste
lastitem = -1	# Bestimmt das letzte Element einer Liste
tempitem = 2	# Bestimmt den Temperaturwert innerhalb der Liste
humiditem = 3	# Bestimmt den Luftfeuchtigkeitswert innerhalb der Liste
temperature = []
humidity = []

def debug():
    print ("Durchschnittstemperatur: %2.1f°C." % temp_avg)
    print ("Minimum: " + min_t[tempitem] + "°C")
    print ("Maximum: " + max_t[tempitem] + "°C")
    print ("Durchschnittliche Luftfeuchtigkeit: %d%% RH." % int(humid_avg))
    print ("Minimum: " + min_h[humiditem] + " % RH")
    print ("Maximum: " + max_h[humiditem] + " % RH")

parser = argparse.ArgumentParser(description=" Dieses Script liest die vorhandene Datei 'sht21-data.csv' ein und berechnet Durschnitt, Minimum und Maximum für die aufgezeichnete Temperatur und Luftfeuchtigkeit.")

parser.add_argument("-v", "--verbose", action="store_true", help="Aktiviert Debuggingausgabe.")

args = parser.parse_args()

with open(sourcefile, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    for row in reader:
        liste.append(row)
        temperature.append(float(liste[lastitem][tempitem]))
        humidity.append(float(liste[lastitem][humiditem]))

min_t_helper = liste[firstitem][tempitem]
max_t_helper = liste[firstitem][tempitem]
min_h_helper = liste[firstitem][humiditem]
max_h_helper = liste[firstitem][humiditem]
for i in range(len(liste)-1):
    if min_t_helper > liste[i+1][tempitem]:
        min_t_helper = liste[i+1][tempitem]
        min_t = liste[i+1]
    if liste[i+1][tempitem] > max_t_helper:
        max_t_helper = liste[i+1][tempitem]
        max_t = liste[i+1]
    if min_h_helper > liste[i+1][humiditem]:
        min_h_helper = liste[i+1][humiditem]
        min_h = liste[i+1]
    if liste[i+1][humiditem] > max_h_helper:
        max_h_helper = liste[i+1][humiditem]
        max_h = liste[i+1]

temp_sum = sum(temperature)
temp_len = len(temperature)
temp_avg = temp_sum / temp_len
humid_sum = sum(humidity)
humid_len = len(humidity)
humid_avg = humid_sum / humid_len

if args.verbose:
    debug()

def writestatsincsv(temp_avg,min_t,max_t,humid_avg,min_h,max_h):
    row = temp_avg + "," + min_t + "," + max_t + "," + humid_avg + "," + min_h + "," + max_h + "\n"
    f = open('statistic_data.csv', 'w')
    f.write(row)
    f.close()
writestatsincsv(str("%2.1f" % temp_avg),str(min_t),str(max_t),str("%d" % humid_avg),str(min_h),str(max_h))

sys.exit(0)
