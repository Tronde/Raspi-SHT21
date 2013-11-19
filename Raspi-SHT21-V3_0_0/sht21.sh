#!/bin/sh

LogInterval=600

while true
do
	TimeString=$(date +"%d.%m.%Y %H:%M:%S")	
	Timestamp=$(date +%s)
	TimeOffset=$(date -d '1970-01-01 0 sec' +%s)
	
	Timestamp=$(($Timestamp - TimeOffset))		
				
	if [ $(($Timestamp % 5)) -eq 0 ]
	then
		Sht21Data=$(./sht21 S)
		echo "$TimeString\t$Timestamp\t$Sht21Data"
			
		if [ $(($Timestamp % $LogInterval)) -eq 0 ]
		then
			echo "$TimeString\t$Timestamp\t$Sht21Data" >> sht21-data.csv
	
			#./sht21 C > sht21-cosm.txt
			#./function-cosm-push.sh
			#./function-ftp-upload.sh
		fi
	fi	
	sleep 1
done