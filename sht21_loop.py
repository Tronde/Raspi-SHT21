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
import time
import datetime

# Example for using the SHT21 Breakoutboard with the Raspberry Pi. Martin Steppuhn, www.emsystech.de
#
# This script appends as measurement of SHT21 to as simple Logfile.
#
# Example:
# 16.06.2015 13:44:00     24.2    44
# 16.06.2015 13:44:30     24.5    43
# 16.06.2015 13:45:00     24.5    43
# 16.06.2015 13:45:30     24.3    42

sht21 = sht21.SHT21()

interval = 5  # Intervall for measurement
file = "log_loop.txt"  # File for Datastorage

print("SHT21-Demo: Write measurement data every", interval, "seconds to", file)

while 1:
    if ((int(time.time()) % interval) == 0):
        try:
            (temp, humidity) = sht21.measure(1)
            timestamp = '{:%d.%m.%Y %H:%M:%S}'.format(datetime.datetime.now())
            s = "%s\t%s\t%d" % (timestamp, temp, humidity)
        except:
            s = "SHT21 I/O Error"
        print(s)
        with open(file, "a") as fp:
            s = s + "\r\n"
            fp.write(s)
        time.sleep(1)
    time.sleep(0.5)
