Raspi-SHT21 Release 2.x.x _english version below_
=========================

*Achtung: Dieser Branch ist in Entwicklung und bietet noch keine lauffähige Version der Software*

Für das Release v2.x soll das Projekt zuerst auf Python migriert werden und unter eine MIT-Lizenz gestellt werden.

Erweiterung des Raspi-SHT21 um weitere entfernte Sensoren. Als entfernte Sensoren kommen Mikrocontroller-Boards vom Typ esp8266 mit dem Sensor DHT22 zum Einsatz.

Die esp8266-Boards sollen in ein WLAN eingebunden werden, um die am DHT22 gemessenen Werte für Luftfeuchtigkeit und Temperatur per WLAN an den Raspi-SHT21 zu übermitteln. Der Raspi-SHT21 empfängt die Daten und speichert sie. Die gespeicherten Daten sollen auf einer Webseite zur Verfügung gestellt werden.


English version
===============

*Caution: This branch is under heavy development and does not provide a version of the software that is ready to run.*

Release v2.x migrates the project to a Python version, licensed unter an MIT-Licence.

The Raspi-SHT21 will be extended by remote sensors. The remote sensors are based on the Microcontroller _esp8266_ with an DHT22 attached to it.

It should be possible to connect the esp8266 boards to a wifi network to transmit the data measured by the DHT22 sensor to the Raspi-SHT21. The Raspi-SHT21 receives the data and stores it. The stored data should be published on a website.
