#!/usr/bin/python2

# Needs pyserial to be installed
# apt-get install python-serial (or python3-serial)

import serial
import time
import sys

# This specific machine settings
port = '/dev/ttyUSB0'
bdr = 115200
timeout = 0.7
cmd = 'Main.Model?'
if (len(sys.argv) == 2 and sys.argv[1] != ""):
    cmd = sys.argv[1]

com = serial.Serial(port=port,baudrate=bdr,timeout=timeout)

com.write(bytes("\r"+cmd+"\r"))
time.sleep(0.3)
result = com.read(255)

print result

com.close

sys.exit()
