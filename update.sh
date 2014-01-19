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
apt-get update
check $?

# Aktuelle Dateien aus dem Repository holen ###################
