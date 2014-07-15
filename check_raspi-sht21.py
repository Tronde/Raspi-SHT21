#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, argparse

sourcefile = '/home/pi/Raspi-SHT21/sht21-data.csv'

def debug():
	print "Die aktuelle Temperatur beträgt %2.1f°C." % temperature
	print "Die aktuelle Luftfeuchtigkeit beträgt %d%%." % humidity
	print min_temperature
	print max_temperature
	print min_humidity
	print max_humidity

parser = argparse.ArgumentParser(description=" Nagios Raspi-SHT21 Plugin. Dieses Plugin bestimmt die vom Raspi-SHT21 gemessene Temperatur und Luftfeuchtigkeit und vergleicht die gemessenen Werte mit den übergebenen Grenzwerten für Temperatur und Luftfeuchtigkeit.")

parser.add_argument("-t", "--min-temperature", dest="mintemperature", required=True, type=float, help="Untere Temperaturgrenze")
parser.add_argument("-T", "--max-temperature", dest="maxtemperature", required=True, type=float, help="Obere Temperaturgrenze")
parser.add_argument("-l", "--min-humidity", dest="minhumidity", required=True, type=int, help="Untere Grenze der Luftfeuchtigkeit")
parser.add_argument("-L", "--max-humidity", dest="maxhumidity", required=True, type=int, help="Obere Grenze der Luftfeuchtigkeit")
parser.add_argument("-v", "--verbose", action="store_true", help="Aktiviert Debuggingausgabe.")

args = parser.parse_args()

min_temperature = args.mintemperature
max_temperature = args.maxtemperature
min_humidity = args.minhumidity
max_humidity = args.maxhumidity

while open(sourcefile, 'r') as csvfile:
	reader = csv.reader(csvfile, delimiter='\t')
	for row in reader:
		liste.append(row)
	temperature = float(liste[-1][3])
	humidity = int(liste[-1][4])

"""
temperature = float(os.popen("tail -n 1 sht21-data.csv | awk '{print $4}'").readline().strip())
humidity = int(os.popen("tail -n 1 sht21-data.csv | awk '{print $5}'").readline().strip())
"""

if args.verbose:
	debug()

if temperature > min_temperature and temperature < max_temperature and humidity > min_humidity and humidity < max_humidity:
	print "OK - Temperatur: %2.1f°C Luftfeuchtigkeit: %d%%. | temperature=%2.1f humidity=%d" % (temperature, humidity, temperature, humidity)
	sys.exit(0)
elif temperature < min_temperature or temperature > max_temperature or humidity < min_humidity or humidity > max_humidity:
	print "WARNING - Temperatur: %2.1f°C Luftfeuchtigkeit: %d%%. | temperature=%2.1f humidity=%d" % (temperature, humidity, temperature, humidity)
	sys.exit(1)
else:
	print "UNKNOWN"
	sys.exit(3)
