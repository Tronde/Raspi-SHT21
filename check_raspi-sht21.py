#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys
from optparse import OptionParser

def print_help():
	print """
	Nagios Raspi-SHT21 Plugin
	
	Dieses Plugin bestimmt die vom Raspi-SHT21 gemessene Temperatur und Luftfeuchtigkeit
	und vergleicht die gemessenen Werte mit den übergebenen Grenzwerten für Temperatur
	und Luftfeuchtigkeit.
	
	Usage: python check_raspi-sht21.py [OPTIONS]
	
	-t, --min-temperature		Legt die erlaubte Minimaltemperatur fest.
	-T, --max-temperature		Legt die erlaubte Maximaltemperatur fest.
	--min-humidity			Legt die erlaubte minimale Luftfeuchtigkeit fest.
	-H, --max-humidity		Legt die erlaubte maximale Luftfeuchtigkeit fest.
	
	Example:
	
	python check_raspi-sht21.py -t -20.0 -T 30.0 --min-humidity 20 --max-humidity 60
	"""

parser = OptionParser("check_raspi-sht21.py Optionen")
parser.add_option("-t", "--min-temperature", dest="mintemperature", help="Untere Temperaturgrenze")
parser.add_option("-T", "--max-temperature", dest="maxtemperature", help="Obere Temperaturgrenze")
parser.add_option("--min-humidity", dest="minhumidity", help="Untere Grenze der Luftfeuchtigkeit")
parser.add_option("-H", "--max-humidity", dest="maxhumidity", help="Obere Grenze der Luftfeuchtigkeit")

(optionen, args) = parser.parse_args()

min_temperature = optionen.mintemperature
max_temperature = optionen.maxtemperature
min_humidity = optionen.minhumidity
max_humidity = optionen.maxhumidity

if min_temperature == None or max_temperature == None or min_humidity == None or max_humidity == None:
	print_help()
	parser.error("Es wurden nicht alle notwendigen Optionen angegeben.")

temperature = os.popen("tail -n 1 sht21-data.csv | awk '{print $4}'").readline().strip()
humidity = os.popen("tail -n 1 sht21-data.csv | awk '{print $5}'").readline().strip()

print "Die aktuelle Temperatur beträgt %s°C." % temperature
print "Die aktuelle Luftfeuchtigkeit beträgt %s." % humidity
print min_temperature
print max_temperature
print min_humidity
print max_humidity

if temperature > min_temperature and temperature < max_temperature and humidity > min_humidity and humidity < max_humidity:
	print "OK - Temperatur: %s°C Luftfeuchtigkeit: %s%%." % (temperature, humidity)
	sys.exit(0)
elif temperature < min_temperature or temperature > max_temperature or humidity < min_humidity or humidity > max_humidity:
	print "WARNUNG - Temperatur: %s°C Luftfeuchtigkeit: %s%%." % (temperature, humidity)
	sys.exit(1)
else:
	print "UNKNOWN"
	sys.exit(3)
