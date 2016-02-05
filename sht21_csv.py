#!/usr/bin/env python3

# Copyright (c) 2015 Martin Steppuhn, www.emsystech.de. All rights reserved.
#
# Redistribution and use in source and binary, must retain the above copyright notice, and the following disclaimer.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

import sht21
import datetime

# Example for using the SHT21 Breakoutboard with the Raspberry Pi. Martin Steppuhn, www.emsystech.de
#
# This script appends the measurement of SHT21 to as simple Logfile. You can use a cronjob to call these script
# Use "crontab -e" and append the following line to call sht21_job.sh every 10 minutes:
# "*/10 * * * * /home/pi/sht21/sht21_csv.sh"
#
# Example:
# 16.06.2015 13:40     24.2    44
# 16.06.2015 13:50     24.5    43
# 16.06.2015 13:00     24.5    43
# 16.06.2015 13:10     24.3    42

sht21 = sht21.SHT21()
file = "log-sht21.txt"  # File for Datastorage

s = '{:%d.%m.%Y %H:%M}'.format(datetime.datetime.now())
try:
    (temp, humidity) = sht21.measure(1)
    s = s + "\t%s\t%d" % (temp, humidity)
except:
    s = s + "SHT21 I/O Error"
print(s)
with open(file, "a") as fp:
    s = s + "\r\n"
    fp.write(s)
