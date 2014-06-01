Raspi-SHT21
===========

Überwachung von Temperatur und Luftfeuchtigkeit mit dem Raspberry Pi und dem SHT-21 Sensor

## Informationen über dieses Repo und die verwendete Software ##

Beim Raspi-SHT21 handelt es sich um eine Sensorerweiterung für den Raspberry Pi. Die Sensorerweiterung und die dazugehörige Software stammt von [www.emsystech.de](http://www.emsystech.de). Die für die Visualisierung benötigte Javascript Libary stammt von [www.flotcharts.org](http://www.flotcharts.org)

Dieses Repo fast alle Quellen zusammen, die notwenig sind, um die von emsystech [beschriebene Lösung](http://www.emsystech.de/raspi-sht21/ "Raspi-SHT21 Sensorerweiterung für Raspberry Pi UPDATE 2!") zu verwirklichen und weiterzuentwickeln. Der Master-Branch von [flot](https://github.com/flot/flot) wurde als Submodule in dieses Repository integriert, um bei der weiteren Entwicklung stets auf die neueste Version zurückgreifen zu können.

## Ziele ##

Ich möchte eine Lösung schaffen, die zur Überwachung von Temperatur und Luftfeuchtigkeit in Serverräumen oder ähnlichen Umgebungen wie z.B. Kühlräumen, Terrarien, etc. verwendet werden kann. Bei Erreichen definierter Grenzwerte soll eine E-Mail verschickt werden.

Aktuell entwickel ich allein an diesem Projekt. Unterstützung ist jedoch herzlich willkommen.

## Installation ##

Nach dem Herunterladen des aktuellen Release werden zuerst die gewünschten Grenzwerte definiert. Die dazu benötigte Datei sht21.conf kann mit Hilfe der Datei sht21.muster erstellt werden:

```bash
cp sht21.muster sht21.conf
```

Anschließend wird die Software und die benötigten Pakete mit Hilfe des Installationsskriptes installiert:

```bash
sudo bash ./install.sh
```

Wer bereits einen Webserver auf seinem Pi betreibt, muss das Skript vor der Installation entsprechend anpassen, um zu verhindern, dass evtl. schon vorhandene Dateien auf dem Pi überschrieben werden.

## Hinweise zur Nutzung ##

Durch das Installationsskript ''install.sh'' wird die Datei:
```bash
/etc/logrotate.d/raspi-sht21
```
erstellt. In der Standardeinstellung werden die Messwerte in der CSV-Datei wöchentlich rotiert. Dieses Verhalten kann in dieser Datei an die persönlichen vorlieben angepasst werden.

Die Messung wird durch ein Start/Stop-Skript gesteuert:
```bash
pi@jk-raspberrypi ~ $ sudo service raspi-sht21.sh 
Usage: /etc/init.d/raspi-sht21.sh {start|stop|status|restart}
pi@jk-raspberrypi ~ $
```

Für den E-Mailversand bei Über- bzw. Unterschreitung der definierten Grenzwerte, muss auf dem Pi ein Postfix installiert sein. Eine Beispielkonfiguration findet man auf [My-IT-Brain](http://www.my-it-brain.de) im Artikel [Postfix mit Gmail als Smarthost](http://www.my-it-brain.de/wordpress/postfix-mit-gmail-als-smarthost/).
