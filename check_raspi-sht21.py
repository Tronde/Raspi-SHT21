#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Nagios Raspi-SHT21 Plugin. Dieses Plugin bestimmt die vom Raspi-SHT21
 gemessene Temperatur und Luftfeuchtigkeit und vergleicht die	
 gemessenen Werte mit den übergebenen Grenzwerten für Temperatur und
 Luftfeuchtigkeit.
		
 @author : Jörg Kastning <joerg.kastning@synaxon.de>
 @version: 17.07.2014				

 Die benötigten Messwerte werden aus einer JSON-Datei eingelesen, welche
 sich im WEBROOT des Raspi-SHT21 befindet.
"""
 
import sys, argparse, json

WEBROOT="/var/www/html/sht21.json"
temperature = 0
humidity = 0

def debug():
	print "Die aktuelle Temperatur beträgt %2.1f°C." % temperature
	print "Die aktuelle Luftfeuchtigkeit beträgt %d%%." % humidity
	print min_temperature
	print max_temperature
	print min_humidity
	print max_humidity

parser = argparse.ArgumentParser(description=" Nagios Raspi-SHT21 Plugin. Dieses Plugin bestimmt die vom Raspi-SHT21 gemessene Temperatur und Luftfeuchtigkeit und vergleicht die gemessenen Werte mit den übergebenen Grenzwerten für Temperatur und Luftfeuchtigkeit.")

parser.add_argument("-d", "--dir", dest="directory", default="/var/www/html/sht21.json", help="Pfad zur JSON-Datei")
parser.add_argument("-t", "--min-temperature", dest="mintemperature", required=True, type=float, help="Untere Temperaturgrenze")
parser.add_argument("-T", "--max-temperature", dest="maxtemperature", required=True, type=float, help="Obere Temperaturgrenze")
parser.add_argument("-l", "--min-humidity", dest="minhumidity", required=True, type=int, help="Untere Grenze der Luftfeuchtigkeit")
parser.add_argument("-L", "--max-humidity", dest="maxhumidity", required=True, type=int, help="Obere Grenze der Luftfeuchtigkeit")
parser.add_argument("-v", "--verbose", action="store_true", help="Aktiviert Debuggingausgabe.")

args = parser.parse_args()

sourcefile = args.directory
min_temperature = args.mintemperature
max_temperature = args.maxtemperature
min_humidity = args.minhumidity
max_humidity = args.maxhumidity

try:
    with open(WEBROOT, 'r') as f:
        sht21_data = json.load(f)
except:
    print("Error: Could not open file sht21.json for reading")

temperature = sht21_data['temp']
humidity = sht21_data['humidity']


if args.verbose:
	debug()

if min_temperature < temperature < max_temperature and min_humidity < humidity < max_humidity:
	print "OK - Temperatur: %2.1f°C Luftfeuchtigkeit: %d%%. | temperature=%2.1f humidity=%d" % (temperature, humidity, temperature, humidity)
	sys.exit(0)
else:
	print "WARNING - Temperatur: %2.1f°C Luftfeuchtigkeit: %d%%. | temperature=%2.1f humidity=%d" % (temperature, humidity, temperature, humidity)
	sys.exit(1)
