#!/bin/bash
# Autor: Joerg Kastning

# Variablen  ###########################################################

source ./sht21.conf

#LogInterval=600
#maxtemp=25.0			# Oberer Grenzwert ab dem eine Temperaturwarnung verschickt wird.
#mintemp=0.0			# Unterer Grenzwert ab dem eine Temperaturwarnung verschickt wird.
#minhumidity=28			# Mindestwert fuer die Luftfeuchtigkeit.
#maxhumidity=50			# Maximalwert fuer die Luftfeuchtigkeit.
#email="support@synaxon.de"	# Zieladresse für die E-Mail-Benachrichtigung.

# Funktionen ###########################################################

tempalarm() {
	
	temp="$(tail -n1 sht21-data.csv | awk '{print $4}')"
	if [ $(echo "if (${temp} > ${maxtemp}) 1 else 0" | bc) -eq 1 ]
	then
		echo "ALARM: Die Temperatur hat den festgelegten oberen Grenzwert überschritten!" | mailx -s "Temperaturalarm" "$email" ;
	fi

	temp="$(tail -n1 sht21-data.csv | awk '{print $4}')"
	if [ $(echo "if (${temp} < ${mintemp}) 1 else 0" | bc) -eq 1 ]
	then
		echo "ALARM: Die Temperatur hat den festgelegten unteren Grenzwert unterschritten!" | mailx -s "Temperaturalarm" "$email" ;
	fi
}

humidityalarm() {
	# Luftfeuchtigkeit aus Datei auslesen und Variable zuweisen.
	humidity="$(tail -n1 sht21-data.csv | awk '{print $5}')"

	# Prüfung, ob Luftfeuchtigkeit innerhalb definierter Parameter liegt.
	if [ $humidity -lt $minhumidity ]
	then
		echo "WARNUNG: Die Luftfeuchtigkeit ist zu niedrig!" | mailx -s "WARNUNG - Luftfeuchtigkeit zu niedrig!" "$email" ;
	fi

	if [ $humidity -gt $maxhumidity ]
	then
		echo "WARNUNG: Die Luftfeuchtigkeit ist zu hoch!" | mailx -s "WARNUNG - Luftfeuchtigkeit zu hoch!" "$email" ;
	fi
}

# Hauptprogramm ########################################################

echo $$ > /var/run/raspi-sht21.pid

while true
do
	TimeString=$(date +"%d.%m.%Y %H:%M:%S")	
	Timestamp=$(date +%s)
	TimeOffset=$(date -d '1970-01-01 0 sec' +%s)
	
	Timestamp=$(($Timestamp - TimeOffset))		
				
	if [ $(($Timestamp % 5)) -eq 0 ]
	then
		Sht21Data=$(./sht21 S)
#		echo -e "$TimeString\t$Timestamp\t$Sht21Data" # Für Tests einkommentieren.
			
		if [ "${Sht21Data%%[[:digit:]]*}" = "" ]; then
			if [ $(($Timestamp % $LogInterval)) -eq 0 ]
			then
				echo -e "$TimeString\t$Timestamp\t$Sht21Data" >> sht21-data.csv

				tempalarm
				humidityalarm

				#./sht21 C > sht21-cosm.txt
				#./function-cosm-push.sh
				#./function-ftp-upload.sh
			fi
		fi
	fi	
	sleep 1
done
