#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Description: Script to compare measured values with defined threshold values
# In case measured values are out of bound a notification e-mail will be send
#
# Supported OS: Raspbian Stretch
# Requirements: Host must be able to send mail
# Author: Joerg Kastning
# License: MIT

import configparser
import json
import smtplib
from email.mime.text import MIMEText

# Variables ##################################################################
maxtemp=38.0    # upper limit for temperature
mintemp=-14.0   # lower limit for temperature
maxhumidity=40  # upper limit for humidity
minhumidity=28  # lower limit for humidity
fromaddr="foo@example.com" # address for email notification
toaddr="bar@example.com"
webroot="/var/www/html/sht21.json"
##############################################################################
# Function to edit ###########################################################
def send_mail(string):
    msg = MIMEText(string)
    msg['Subject'] = string
    msg['From'] = fromaddr
    msg['To'] = toaddr

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("username", "password")
    s.sendmail(fromaddr, toaddr, msg.as_string())
    s.close
##############################################################################

def tempalarm(temperature):
    if (temperature > maxtemp):
        string="ALERT: The temperature is above the upper limit"
        send_mail(string)
    elif (temperature < mintemp):
        string="ALERT: The temperature is below the lower limit"
        send_mail(string)

def humidalarm(humidity):
    if (humidity > maxhumidity):
        string="ALERT: The humidity is above the upper limit"
        send_mail(string)
    elif (humidity < minhumidity):
        string="ALERT: The humidity is below the lower limit"
        send_mail(string)

def main():
    try:
        with open(webroot, 'r') as f:
            sht21_data = json.load(f)
    except:
        print("Error: Could not open file sht21.json for reading")

    temperature = sht21_data['temp']
    humidity = sht21_data['humidity']

    tempalarm(temperature)
    humidalarm(humidity)

if __name__ == "__main__":
    main()
