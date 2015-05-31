Raspi-SHT21
===========

Überwachung von Temperatur und Luftfeuchtigkeit mit dem Raspberry Pi und dem SHT-21 Sensor.

## Informationen über dieses Repo und die verwendete Software ##

Beim Raspi-SHT21 handelt es sich um eine Sensorerweiterung für den Raspberry Pi. Die Sensorerweiterung und die dazugehörige Software stammt im Original von [www.emsystech.de](http://www.emsystech.de) und wird hier von mir weiterentwickelt. Die für die Visualisierung benötigte Javascript Libary stammt von [www.flotcharts.org](http://www.flotcharts.org)

Dieses Repo fast alle Quellen zusammen, die notwenig sind, um die von emsystech [beschriebene Lösung](http://www.emsystech.de/raspi-sht21/ "Raspi-SHT21 Sensorerweiterung für Raspberry Pi UPDATE 2!") zu verwirklichen und weiterzuentwickeln. Der Master-Branch von [flot](https://github.com/flot/flot) wurde als Submodule in dieses Repository integriert, um bei der weiteren Entwicklung stets auf die neueste Version zurückgreifen zu können.

## Ziele ##

Ich möchte eine Lösung schaffen, die zur Überwachung von Temperatur und Luftfeuchtigkeit in Serverräumen oder ähnlichen Umgebungen wie z.B. Kühlräumen, Terrarien, etc. verwendet werden kann. Bei Erreichen definierter Grenzwerte soll eine E-Mail verschickt werden.

Aktuell entwickle ich allein an diesem Projekt. Unterstützung ist jedoch herzlich willkommen.

Findet ihr einen Fehler, funktioniert etwas nicht wie erwartet, oder wünscht ihr euch eine neue Funktion, so freue ich mich, wenn ihr einen [Issue](https://github.com/Tronde/Raspi-SHT21/issues) eröffnet.

## Funktionen ##

* Temperaturüberwachung (-40 - 125°C)
* Messung der Luftfeuchtigkeit (0 - 100% relative Luftfeuchtigkeit)
* Visualisierung der Messwerte im Browser, als Text und Verlaufsdiagramm
* Anzeige der Messwerte direkt im Browsertab
* E-Mail Benachrichtigung bei Überschreitung definierter Grenzwerte

## Installation ##

Im folgenden findet ihr eine kleine Installationsanleitung für den Raspi-SHT21.

### Voraussetzungen ###

* Raspberry Pi, auf dem vorzugsweise Raspbian läuft
* Das [SHT21 Breakout Board](http://www.emsystech.de/produkt/sht21-breakout-board/)

### Installation aus Archivdatei ###

Das aktuelle Release findet ihr stets im Github Repository unter [https://github.com/Tronde/Raspi-SHT21/releases](https://github.com/Tronde/Raspi-SHT21/releases).

Nach dem Herunterladen des aktuellen Release, wird das Archiv in das Verzeichnis "Raspi-SHT21" im HOME-Verzeichnis des Pi-Users entpackt. Dies geschieht mit den folgenden Befehlen:

```bash
mkdir /PFAD/ZUM/ORDNER
tar -xzf archiv.tar.gz -C /PFAD/ZUM/ORDNER
```

### Installation über das Git Repository ###

Alternativ könnt ihr den jeweils aktuellsten Entwicklungsstand aus dem Master Branch des Repositories auschecken. Hierfür muss __git__ auf eurem Rechner installiert sein.

```bash
cd ~
git clone https://github.com/Tronde/Raspi-SHT21.git
cd Raspi-SHT21
```

### Erstkonfiguration ###

Zuerst werden nun die gewünschten Grenzwerte definiert. Die dazu benötigte Datei sht21.conf kann mit Hilfe der Datei sht21.muster erstellt werden, indem die Datei kopiert und die enthaltenen Parameter angepasst werden.

```bash
pi@raspberrypi:~/Raspi-SHT21$ cat sht21.muster 
# Variablen  ###########################################################

LogInterval=600
maxtemp=38.0                    # Grenzwert ab dem eine Temperaturwarnung verschickt wird.
mintemp=-14.0                    # Unterer Grenzwert ab dem eine Temperaturwarnung verschickt wird.
minhumidity=28                  # Mindestwert fuer die Luftfeuchtigkeit.
maxhumidity=50                  # Maximalwert fuer die Luftfeuchtigkeit.
# Unten wird die Empfänger-E-Mail-Adresse für Warnungen und Alarmierungen definiert.
# Für mehrere Empfänger sind die Adressen einfach durch Leerzeichen getrennt anzuhängen. Bsp:
# email="example@foo.bar example2@foo.bar"
email="example@foo.bar"      # Zieladresse für die E-Mail-Benachrichtigung.
pi@raspberrypi:~/Raspi-SHT21$ cp sht21.muster sht21.conf
pi@raspberrypi:~/Raspi-SHT21$ vim sht21.conf
```

Anschließend wird die Software und die benötigten Pakete mit Hilfe des Installationsskriptes installiert:

```bash
sudo bash ./install.sh
```

Wer bereits einen Webserver auf seinem Pi betreibt, muss das Skript vor der Installation entsprechend anpassen, um zu verhindern, dass evtl. schon vorhandene Dateien auf dem Pi überschrieben werden.

### Programmsteuerung ###

Die Messung wird durch ein Start/Stop-Skript gesteuert:
```bash
pi@jk-raspberrypi ~ $ sudo service raspi-sht21.sh 
Usage: /etc/init.d/raspi-sht21.sh {start|stop|status|restart}
pi@jk-raspberrypi ~ $
```

## Weitere Konfigurationsmöglichkeiten ##

### Logrotation ###

Durch das Installationsskript ''install.sh'' wird die Datei:
```bash
/etc/logrotate.d/raspi-sht21
```
erstellt. In der Standardeinstellung werden die Messwerte in der CSV-Datei wöchentlich rotiert. Dieses Verhalten kann in dieser Datei an die persönlichen vorlieben angepasst werden. Weitere Informationen zu logrotate findet man im Artikel [Logdateien](http://wiki.ubuntuusers.de/Logdateien?highlight=logrotate#Logrotate), im Ubuntuusers Wiki.

**/etc/logrotate.d/raspi-sht21:**
```bash
/home/pi/Raspi-SHT21/*csv {
        weekly
        missingok
        notifempty
        rotate 7
        compress
        delaycompress
        # mail foo@example.org
        # mailfirst
        sharedscripts
        create 0644 pi pi
        postrotate
                invoke-rc.d rsyslog rotate > /dev/null
        endscript
}
```

Man kann sich das jeweils letzte Log automatisch per E-Mail senden lassen. Dazu ist das Kommentarzeichen der beiden Zeilen
```bash
# mail foo@example.org
# mailfirst
```
zu entfernen und eine Empfänger-E-Mail-Adresse anzugeben.

Eine weitere Möglichkeit sich die Logs per E-Mail zusenden zu lassen besteht in der Einrichgung eines Cronjobs. Dazu kann folgender Befehl in der crontab genutzt werden:
```bash
mailx -s "Betreff" -a /pfad/zur/logdatei.csv.1 email@example.org
```

Für den E-Mailversand bei Über- bzw. Unterschreitung der definierten Grenzwerte, muss auf dem Pi ein Postfix installiert sein. Eine Beispielkonfiguration findet man auf [My-IT-Brain](http://www.my-it-brain.de) im Artikel [Postfix mit Gmail als Smarthost](http://www.my-it-brain.de/wordpress/postfix-mit-gmail-als-smarthost/).
