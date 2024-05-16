#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
from serial.serialutil import EIGHTBITS, PARITY_NONE

com_port = "COM3"
com_baud = 115200
com_bytesize = EIGHTBITS
com_parity = PARITY_NONE

ser = serial.Serial(com_port,com_baud,com_bytesize,com_parity)

if ser.isOpen():
    print("Success."+ser.name)
    print("To exit, press Ctrl+C")
else:
    print("Failed.")
    exit()

while True:
    try:
        ser_in=ser.read(ser.in_waiting)
        if ser_in:
            print(ser_in.decode("utf-8"))
            
    except KeyboardInterrupt:
        ser.close()
        print("Application Exit.")
        exit()