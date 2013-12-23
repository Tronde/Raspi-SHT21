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
# Installation der i1c-tools, lighttpd und php5-cgi
apt-get update && apt-get -y install i2c-tools lighttpd php5-cgi
check $?

# I2C-Treiberaktivierung
echo "I2C-Treiberaktivierung"
echo "i2c-dev" >>/etc/modules
check $? 
cp raspi-blacklist.conf /etc/modprobe.d/
adduser pi i2c
check $?
# Einrichtung des Webservers und Aktivierung von FastCGI
echo " Einrichtung des Webservers und Aktivierung von FastCGI"
adduser pi www-data
check $?
chown -R www-data:www-data /var/www
check $?
chmod -R 775 /var/www
check $?
lighty-enable-mod fastcgi
check $?
/etc/init.d/lighttpd force-reload
check $?
cp lighttpd.conf /etc/lighttpd/
check $?
cp -R Raspi-SHT21-V3_0_0/www/ /var/www/
check $?
echo "Erstellung von sht21-data.csv und des symbolischen Links."
touch ~/Raspi-SHT21/Raspi-SHT21-V3_0_0/sht21-data.csv
chown pi:pi ~/Raspi-SHT21/Raspi-SHT21-V3_0_0/sht21-data.csv
ln -s ~/Raspi-SHT21/Raspi-SHT21-V3_0_0/sht21-data.csv sht21-data.csv
check $?
