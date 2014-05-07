#!/bin/bash
# Name: Raspi-SHT21 Installationsscript
# Autor: Joerg Kastning
# Voraussetzungen: Raspian OS on the Pi
#
# Funktionen
function check() {
  if [ $1 -gt 0 ]; then
    echo "Uuups, hier ist was schiefgegangen"
    echo "exit $1"
    exit 1
  fi
}
# Installation der i1c-tools, lighttpd, php5-cgi und weitere benötigte Pakete.
apt-get update && apt-get -y install i2c-tools lighttpd php5-cgi bc resolvconf
check $?

# I2C-Treiberaktivierung
echo "I2C-Treiberaktivierung"
echo "i2c-dev" >>/etc/modules
check $? 
cp /etc/modprobe.d/raspi-blacklist.conf /etc/modprobe.d/raspi-blacklist.conf.bak
cp raspi-blacklist.conf /etc/modprobe.d/
adduser pi i2c
check $?

# Einrichtung des Webservers und Aktivierung von FastCGI
echo " Einrichtung des Webservers und Aktivierung von FastCGI"
adduser pi www-data
check $?
lighty-enable-mod fastcgi
check $?
/etc/init.d/lighttpd force-reload
check $?
cp lighttpd.conf /etc/lighttpd/
check $?
cp -R www /var/
check $?

echo "Erstellung von sht21-data.csv und des symbolischen Links."
touch /home/pi/Raspi-SHT21/sht21-data.csv
chown pi:pi /home/pi/Raspi-SHT21/sht21-data.csv
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
