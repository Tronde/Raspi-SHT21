#!/usr/bin/env python3
import os

def get_temperature():
	s = os.popen('vcgencmd measure_temp').readline()
	return (float(s.replace("temp=", "").replace("'C\n", "")))

# Example
if __name__ == "__main__":
	t = get_temperature()
	print("CPU-Temperature: %s °C " % t)
