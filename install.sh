#!/bin/bash
# Name: Raspi-SHT21 Installationsscript
# Autor: Joerg Kastning
# Voraussetzungen: Raspian OS on the Pi
#
# Installation der i1c-tools, lighttpd und php5-cgi
apt-get update && apt-get -y install i2c-tools lighttpd php5-cgi

# I2C-Treiberaktivierung
echo "i2c-dev" >>/etc/modules
cp raspi-blacklist.conf /etc/modprobe.d/
adduser pi i2c

# Einrichtung des Webservers und Aktivierung von FastCGI
adduser pi www-data
chown -R www-data:www-data /var/www
chmod -R 775 /var/www
lighty-enable-mod fastcgi
/etc/init.d/lighttpd force-reload
cp lighttpd.conf /etc/lighttpd/
cp Raspi-SHT21-V3_0_0/www/* /var/www
ln -s ~/Raspi-SHT21-V3_0_0/sht21-data.csv sht21-data.csv
