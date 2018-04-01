#!/bin/bash
# Description: Script to setup, update and remove Raspi-SHT21
# Supported OS: Raspbian Stretch
# Author: Joerg Kastning
# License: MIT
#
# Usage: setup.sh [OPTION]
# Where OPTION=--uninstall|--update

if [ $UID -ne 0 ]; then
	echo
	echo "Error: Script must be run by superuser!"
	echo
	exit 1
else
	echo
	echo "Check: Script is run by superuser!"
	echo
fi

unset WWWROOT
unset PACKAGE_LIST
PACKAGE_LIST="lighttpd spawn-fcgi libdbi1 libfam0 php-cgi php-readline php-cli rrdtool librrd8 libterm-readkey-perl libterm-readline-perl-perl python3-rpi.gpio i2c-tools"
WEBROOT="/var/www/html"

if [ "$1" = "--uninstall" -o "$1" = "-uninstall" -o "$1" = "uninstall" ]; then
  apt -y remove ${PACKAGE_LIST}
  rm -rf ${WEBROOT}/chart-day.png ${WEBROOT}/chart-week.png ${WEBROOT}/*.json ${WEBROOT}/index.php ${WEBROOT}/import.php ${WEBROOT}/dashboard
  exit
fi

if [ "$1" = "--update" -o "$1" = "-update" -o "$1" = "update" ]; then
  echo "Place files in webroot"
  cp -rpv ./www/* ${WEBROOT}
  exit
fi

if [ `dpkg-query -l apache2 2>/dev/null 1>&2` ] || [ `dpkg-query -l nginx 2>/dev/null 1>&2` ]; then
  echo
  echo "Warning: There is already an other webserver installed on this system."
  echo "Please remove all installed webservers and restart the setup again."
  echo "Alternative: Setup the Raspi-SHT21 manually without using this setup script."
  echo
  exit 1
fi

# Enable I2C interface
# Code was copied from raspi-config tool
echo
echo "Enable I2C interface"
echo "===================="
echo
CONFIG=/boot/config.txt
SETTING=on
DEVICE_TREE="yes"
  DEFAULT=
  if [ -e $CONFIG ] && grep -q "^device_tree=$" $CONFIG; then
    DEVICE_TREE="no"
  fi

  CURRENT_SETTING="off" # assume disabled
  DEFAULT=--defaultno
  if [ -e $CONFIG ] && grep -q -E "^(device_tree_param|dtparam)=([^,]*,)*i2c(_arm)?(=(on|true|yes|1|))?$" $CONFIG; then
    CURRENT_SETTING="on"
    DEFAULT=
  fi
  if [ $SETTING != $CURRENT_SETTING ]; then
    echo "The I2C interface will be enabled after the next reboot of the system."
  fi
  sed $CONFIG -i -r -e "s/^((device_tree_param|dtparam)=([^,]*,)*i2c(_arm)?)(=[^,]*)?/\1=$SETTING/"
  if ! grep -q -E "^(device_tree_param|dtparam)=([^,]*,)*i2c(_arm)?=[^,]*" $CONFIG; then
    printf "dtparam=i2c_arm=$SETTING\n" >> $CONFIG
  fi
  if [ $SETTING = "off" ]; then
    return 0
  fi

# Enable I2C Driver
if [ ! `lsmod | grep -q i2c_dev` ]; then
  echo "i2c_dev" >>/etc/modules
fi

echo
echo "I2C driver is loaded"
echo "Adding user pi to group i2c"
usermod -aG i2c pi
if [ $? -ne 0 ]; then
  echo
  echo "Error adding user pi to group i2c"
  echo
  exit 1
else
  echo "Added user pi to group i2c successfully."
fi

echo
echo "Install packages required for Raspi-SHT21"
echo "========================================="
echo
#apt update
apt -y install ${PACKAGE_LIST}
if [ $? -ne 0 ]; then
  echo
  echo "Error $? during the installation of required packages."
  echo "Aborting installation"
  echo
  exit 1
else
  echo
  echo "Finished: Package installation"
  echo "=============================="
  echo
fi

echo "Configure lighttpd and enable FastCGI"
echo "====================================="
echo
echo "Adding user pi to group www-data"
usermod -aG www-data pi 
echo "Enable fastcgi"
lighty-enable-mod fastcgi fastcgi-php
echo "Reload lighttpd"
systemctl force-reload lighttpd
echo "Place files in webroot"
cp -rpv ./www/* ${WEBROOT}
echo "Set chgrp -R www-data on ${WEBROOT}"
chgrp -R www-data ${WEBROOT}

echo "====================="
echo "Installation finished"
echo "====================="

cat <<EOF
# Use "crontab -e" and append the following line to call sht21_job.sh every 10 minutes:
# "*/10 * * * * /home/pi/Raspi-SHT21/sht21_job.sh"
EOF
