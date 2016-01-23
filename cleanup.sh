#!/bin/bash
# Name: Raspi-SHT21 Cleanupscript
# Autor: Joerg Kastning
# Beschreibung:
# Dieses Script macht die Raspi-SHT21 Installation rückgängig.

# Deinstallation nicht benötigter Pakete
apt-get -y --purge autoremove i2c-tools lighttpd php5-cgi bc

# I2C-Treiber deaktivieren
sed '/i2c-dev/d' /etc/modules >/etc/modules.tmp && mv /etc/modules.tmp /etc/modules
modprobe -r i2c_dev
# Nicht mehr benötigte Dateien aus älteren Versionen entfernen
if [ -e /etc/modprobe.d/raspi-blacklist.conf.bak ]
  then
    rm /etc/modprobe.d/raspi-blacklist.conf.bak
fi

# raspi-sht21.sh aus den runleveln und logrotate entfernen
update-rc.d -f raspi-sht21.sh remove
rm /etc/init.d/raspi-sht21.sh
rm /etc/logrotate.d/raspi-sht21

# lighttpd Verzeichnis aufraeumen
rm -rf /var/www/index.php /var/www/js /var/www/layout.css /var/www/sht21-data.csv /var/www/esp8266_data.csv /var/www/statistic_data.csv
rm /home/pi/Raspi-SHT21/sht21-data.csv
rm /home/pi/Raspi-SHT21/esp8266_data.csv
rm /home/pi/Raspi-SHT21/statistic_data.csv

# Benutzer aufraeumen
deluser pi www-data
deluser pi i2c

cd
exit 0
