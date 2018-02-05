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

# Modified by Joerg Kastning

import sht21
import time
import datetime
import subprocess
import os.path
import json
import rpi_cpu

# Example for using the SHT21 Breakoutboard with the Raspberry Pi. Martin Steppuhn, www.emsystech.de
#
# Every 10 minutes the measurement from the SHT21 is stored to a RRD-Tool Database.
# A JSON File and two charts (PNG) are generated and stored for a Webserver.
# index.php shows these data
#
# Install a webserver with path to "/home/pi/www"
# Install rrdtool: "sudo apt-get install rrdtool"
# Copy "index.php" to "/home/pi/www"
# Use "crontab -e" and append the following line to call sht21_job.sh every 10 minutes:
# "*/10 * * * * /home/pi/sht21/sht21_job.sh"

rrd_file = "sht21.rrd"     # Database file
www_path = "/var/www/html"  # Output (Chart)
json_file = "sht21.json"     # Output (JSON-Data)

def rrd_init():
    """Check if RRD Database ist available, if not, create it"""
    try:
        with open(rrd_file): pass
        print("RRD-Database [", rrd_file, "] found")
    except:
        print("Create RRD-Database: [", rrd_file, "]")
        cmd = [ "rrdtool", "create", "%s" % (rrd_file),
                "--step", '600',                    # 10min = 600
                "DS:temp:GAUGE:1800:U:U",           # Temperature, 30min Timeout,
                "DS:humidity:GAUGE:1800:U:U",       # Humidity, 30min Timeout,
                "DS:tcpu:GAUGE:1800:U:U",           # CPU-Temperature, 30min Timeout,
                "RRA:AVERAGE:0.5:1:288",         # 0.5 internal, store 48h @ 10min
                "RRA:AVERAGE:0.5:6:8760"]        # 0.5 internal, store 1 year @ 1hour
        subprocess.Popen(cmd)

def rrd_update(values):
    """Write values to RRD Database"""
    cmd = ["rrdtool", "update", rrd_file, "N:" + values]
    subprocess.Popen(cmd)

def rrd_graph(timespan,file):
    """Time in seconds (X-Axis) and Output-File"""
    print("Building graph from [%s], Timespan: %s Seconds" % (rrd_file,timespan))
    cmd = ["rrdtool", "graph", "%s/%s" % (www_path,file),
           "--start", "-%s" % (timespan),
           "--title=SHT21: %d Days of Temperature and Humidity " % (timespan/86400),
           "--vertical-label=Temperatur",
           "--watermark=www.emsystech.de",
           "--width=1000",
           "--height=500",
           "--alt-autoscale",
           "--lower-limit=-20",
           "--upper-limit=60",
           "--rigid",
           "--right-axis-label=Prozent",
           "--right-axis=1.25:25",
           "--slope-mode",
           "DEF:t=%s:temp:AVERAGE" % (rrd_file),
           "DEF:rh=%s:humidity:AVERAGE" % (rrd_file),
           "DEF:tcpu=%s:tcpu:AVERAGE" % (rrd_file),
           "CDEF:xrh=rh,0.8,*,20,-",
           "LINE2:t#FF0000:Temperatur",
           "LINE2:xrh#0000FF:Luftfeuchtigkeit",
           "LINE2:tcpu#00FF00:CPU-Temperatur"]
    subprocess.Popen(cmd)

sht21 = sht21.SHT21()
d = dict()
rrd_init()
d['time'] = '{:%d.%m.%Y %H:%M}'.format(datetime.datetime.now())
d['tcpu'] = rpi_cpu.get_temperature()
try:
    (d['temp'], d['humidity']) = sht21.measure(1)
except:
    d['temp']="-"
    d['humidity']="-"

rrd_update(str(d['temp'])+":"+str(d['humidity'])+":"+str(d['tcpu']))

# write measured data to data.json in webserver path
json = json.dumps(d)
print("Data: "+json)
with open(www_path+"/"+json_file, "w") as fp:
    fp.write(json)

# build charts if necessary

min = int(time.time() / 60)
# build day chart every 10 minutes or if not exist
if not (os.path.isfile(www_path+"/chart-day.png")) or ((min % 10) == 0):
    rrd_graph(1*24*60*60,"chart-day.png")
    # build week chart every hour or if not exist
    if not (os.path.isfile(www_path+"/chart-week.png")) or ((min % 60) == 0):
        rrd_graph(7*24*60*60,"chart-week.png")
