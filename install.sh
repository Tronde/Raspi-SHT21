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
# Installation der i2c-tools, lighttpd, php5-cgi und weitere benötigte Pakete.
apt-get update && apt-get -y install i2c-tools lighttpd php5-cgi bc resolvconf
check $?

# Aktivierung der I2C Schnittstelle des Raspberry Pi
# Der Code wurde dem raspi-config Tool entnommen.
CONFIG=/boot/config.txt
SETTING=on
DEVICE_TREE="yes" # assume not disabled
  DEFAULT=
  if [ -e $CONFIG ] && grep -q "^device_tree=$" $CONFIG; then
    DEVICE_TREE="no"
  fi

  CURRENT_SETTING="off" # assume disabled
  DEFAULT=--defaultno
  if [ -e $CONFIG ] && grep -q -E "^(device_tree_param|dtparam)=([^,]*,)*i2c(_arm)?(=(on|true|yes|1))?(,.*)?$" $CONFIG; then
    CURRENT_SETTING="on"
    DEFAULT=
  fi
  if [ $SETTING != $CURRENT_SETTING ]; then
    echo "Die I2C-Schnittstelle wird beim nächsten Neustart aktiviert."
  fi
  sed $CONFIG -i -r -e "s/^((device_tree_param|dtparam)=([^,]*,)*i2c(_arm)?)(=[^,]*)?/\1=$SETTING/"
  if ! grep -q -E "^(device_tree_param|dtparam)=([^,]*,)*i2c(_arm)?=[^,]*" $CONFIG; then
    printf "dtparam=i2c_arm=$SETTING\n" >> $CONFIG
  fi
  if [ $SETTING = "off" ]; then
    return 0
  fi

# I2C-Treiberaktivierung
echo "I2C-Treiberaktivierung"
echo "i2c-dev" >>/etc/modules
modprobe i2c-dev
lsmod | grep i2c_dev
check $?
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
echo "Bitte starten Sie den Raspberry Pi zum Abschluss der Installation einmal neu!"
exit 0
