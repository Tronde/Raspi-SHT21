#!/bin/bash
# Name: email_alarm.sh
# Autor: Joerg Kastning
#
# Dieses Script richtet den E-Mailversand über einen Smarthost ein.
# Funktionen
function check() {
  if [ $1 -gt 0 ]; then
    echo "Uuups, hier ist was schiefgegangen"
    echo "exit $1"
    exit 1
  fi
}

echo "Installation der benötigten Pakete."
apt-get update && apt-get -y upgrade && apt-get -y install postfix libsasl2-modules bsd-mailx
postconf -e 'inet_protocols = ipv4'
/etc/init.d/postfix restart
