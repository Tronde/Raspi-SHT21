#!/bin/sh
# Autor: Joerg Kastning

# Variablen  ###########################################################

LogInterval=600
maxtemp=115.0			# Grenzwert ab dem eine Temperaturwarnung verschickt wird.
email="name@example.org"	# Zieladresse für die E-Mail-Benachrichtigung.

# Funktionen ###########################################################

tempalarm() { echo "ALARM: Die Temperatur hat den festgelegten Grenzwert überschritten!" | mailx -s "Temperaturalarm" "$email" ; }

# Hauptprogramm ########################################################

while true
do
	TimeString=$(date +"%d.%m.%Y %H:%M:%S")	
	Timestamp=$(date +%s)
	TimeOffset=$(date -d '1970-01-01 0 sec' +%s)
	
	Timestamp=$(($Timestamp - TimeOffset))		
				
	if [ $(($Timestamp % 5)) -eq 0 ]
	then
		Sht21Data=$(./sht21 S)
#		echo "$TimeString\t$Timestamp\t$Sht21Data" # Für Tests einkommentieren.
			
		if [ $(($Timestamp % $LogInterval)) -eq 0 ]
		then
			echo "$TimeString\t$Timestamp\t$Sht21Data" >> sht21-data.csv

			temp="$(tail -n1 sht21-data.csv | awk '{print $4}')"
			if [ $(echo "if (${temp} > ${maxtemp}) 1 else 0" | bc) -eq 1 ]
			then
        			tempalarm
			fi
	
			#./sht21 C > sht21-cosm.txt
			#./function-cosm-push.sh
			#./function-ftp-upload.sh
		fi
	fi	
	sleep 1
done
