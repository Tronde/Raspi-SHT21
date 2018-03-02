Raspi-SHT21
===========

Überwachung von Temperatur und Luftfeuchtigkeit mit dem Raspberry Pi und dem SHT-21 Sensor.

Die Version 2.0.0 dieses Projekts kann darüber hinaus Messwerte verarbeiten, die von einem ESP8266 mit angeschlossenem DHT22-Sensor übermittelt werden.

*If you need information on how to use this software in English, please feel free to ask. I will provide english documentation on demand.*

## Informationen über dieses Repo und die verwendete Software ##

Beim Raspi-SHT21 handelt es sich um eine Sensorerweiterung für den Raspberry Pi. Die Sensorerweiterung und die dazugehörige Software stammt im Original von [www.emsystech.de](http://www.emsystech.de) und wird hier von mir weiterentwickelt.

## Ziele ##

Ich möchte eine Lösung schaffen, die zur Überwachung von Temperatur und Luftfeuchtigkeit in Serverräumen oder ähnlichen Umgebungen wie z.B. Kühlräumen, Terrarien, Wohnräumen, etc. verwendet werden kann. Bei Erreichen definierter Grenzwerte soll eine E-Mail verschickt werden.

Findet ihr einen Fehler, funktioniert etwas nicht wie erwartet, oder wünscht ihr euch eine neue Funktion, so freue ich mich, wenn ihr einen [Issue](https://github.com/Tronde/Raspi-SHT21/issues) eröffnet.

## Funktionen ##

* Temperaturüberwachung (-40 - 125°C)
* Messung der Luftfeuchtigkeit (0 - 100% relative Luftfeuchtigkeit)
* Visualisierung der Messwerte im Browser, als Text und Verlaufsdiagramm
* Anzeige der Messwerte direkt im Browsertab
* E-Mail Benachrichtigung bei Überschreitung definierter Grenzwerte

Für die von ESP8266 übermittelten Werte gilt:
* Import und Speicherung der zuletzt übermittelten Messwerte in einer JSON-Datei
* Darstellung von Temperatur und Luftfeuchtigkeit auf einem Dashboard
* Verlaufsdiagramme und E-Mail-Alarm sind noch **nicht** implementiert

## Installation ##

Im folgenden findet ihr eine kleine Installationsanleitung für den Raspi-SHT21.

### Voraussetzungen ###

* Raspberry Pi, auf dem Raspbian Stretch läuft
* Das [SHT21 Breakout Board](http://www.emsystech.de/produkte/feuchtigkeitssensor-sht21/)

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

Zuerst werden nun die gewünschten Grenzwerte definiert und die benötigten Parameter zum Versand von E-Mail angegeben. Dies geschieht in der Datei `mail_report.py`:

```bash
# Variables ##################################################################
maxtemp=38.0    # upper limit for temperature
mintemp=-14.0   # lower limit for temperature
maxhumidity=40  # upper limit for humidity
minhumidity=28  # lower limit for humidity
fromaddr="foo@example.com"
toaddr="bar@example.com" # address for email notification
webroot="/var/www/html/sht21.json"
##############################################################################
# Function to edit ###########################################################
def send_mail(string):
    msg = MIMEText(string)
    msg['Subject'] = string
    msg['From'] = fromaddr
    msg['To'] = toaddr

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("username", "password") # Set parameter accordingly
    s.sendmail(fromaddr, toaddr, msg.as_string())
    s.close
##############################################################################
```

Die Aktivierung der E-Mail-Alarmierung erfolgt in der Datei `sht21_job.sh`, durch Entfernen des Kommentarzeichens '#' vor `./mail_report.py`.

Anschließend wird die Software und die benötigten Pakete mit Hilfe des Installationsskriptes installiert:

```bash
sudo bash ./setup.sh
```

Das Setup-Skript prüft zuerst, ob es über die benötigten Benutzerrechte für die Installation verfügt. Anschließend werden die benötigten Pakete installiert:

```bash
PACKAGE_LIST="lighttpd spawn-fcgi libdbi1 libfam0 php-cgi php-readline php-cli rrdtool librrd8 libterm-readkey-perl libterm-readline-perl-perl python3-rpi.gpio i2c-tools"
```

Die für die Anzeige im Webbrowser benötigten Dateien werden direkt in das Webroot des LIGHTTPD unter `/var/www/html` kopiert. Der Pfad der Pfad kann über die Variable `WEBROOT` im Skript `setup.sh` angepasst werden.

Am Ende gibt das Skript einen Hinweis auf, wie der Cronjob einzurichten ist, welcher die regelmäßige Abfrage des SHT21-Sensors steuert.

Wer bereits einen Webserver auf seinem Pi betreibt, muss das Skript vor der Installation entsprechend anpassen, um zu verhindern, dass evtl. schon vorhandene Dateien auf dem Pi überschrieben werden.

Für weitere Hinweise werft bitte einen Blick in das [Pojekt-Wiki](https://github.com/Tronde/Raspi-SHT21/wiki).
