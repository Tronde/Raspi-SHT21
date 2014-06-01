#!/bin/bash
# Name: Raspi-SHT21 Updatescript
# Autor: Joerg Kastning
#
# Funktionen ##################################################
function check() {
  if [ $1 -gt 0 ]; then
echo "Uuups, hier ist was schiefgegangen"
    echo "exit $1"
    exit 1
  fi
}

# Aktualisierung der Paketquellen #############################
#apt-get update # Update bis zur weiteren Verwendung deaktiviert.
#check $?

# Aktuelle Dateien in die Verzeichnisse kopieren ###################
echo "Erstellung von sht21-data.csv und des symbolischen Links."
touch /home/pi/Raspi-SHT21/sht21-data.csv
chown pi:pi /home/pi/Raspi-SHT21/sht21-data.csv
rm /var/www/sht21-data.csv
ln -s /home/pi/Raspi-SHT21/sht21-data.csv /var/www/sht21-data.csv
check $?
chown -R www-data:www-data /var/www
check $?
chmod -R 775 /var/www
check $?

# Einrichtung des logrotate scripts
cp /home/pi/Raspi-SHT21/raspi-sht21 /etc/logrotate.d/
check $?

# Installation des raspi-sht21.sh Start-Stop-Script
cp /home/pi/Raspi-SHT21/raspi-sht21.sh /etc/init.d/
cd /etc/init.d
update-rc.d raspi-sht21.sh defaults
check $?

# lighttpd zum Abschluss neustarten
service lighttpd restart
cd
exit 0
