#!/usr/bin/python3

import platform
import time
import datetime
import serial
from serial import Serial


port = serial.Serial()
serial_port="/dev/ttyS0"
port = serial.Serial(serial_port, 57600, serial.EIGHTBITS, serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.25)

def send_miconv3(message):
	output = bytearray()
	output.extend(map(ord, message + "\r"))
	port.write(output)
	return (recv_miconv3())

def recv_miconv3():
	response = port.readline()
	return (response)

def eeprom_dump():
	width=16
	for y in range(64):
		hexline = ""
		strline = ""
		byte=(y*width)
		print (f"{byte:#0{6}x}",end='')
		for x in range(width):
			byte=(y*width)+x
			message = "EEPROM_READ "+ str(y*width+x) +" 1"
			output = bytearray()
			output.extend(map(ord, message + "\r"))
			port.write(output)

			result = port.readline()
			resultint  = int(result)
			resultbyte = resultint.to_bytes(1,'big')
			resultchar = (str(resultbyte, 'utf-8'))
			if not(resultchar.isprintable()):
				resultchar=" "
			strline = strline + resultchar
			resulthex  = resultbyte.hex()
			hexline = hexline + " " + resulthex
		print (hexline,strline)

#str= "SOUND 2319 50"

#send_miconv3(str)

#quit()

file = open("/etc/debian_version", "r")
version= "Debian " + file.readline().strip()
version = version.center(16,u"\u00A0")
title = "Terastation " + platform.machine()[:3].upper()

char= u"\u00A0"

send_miconv3("LCD_PUTS 0 "+ version)
send_miconv3("LCD_PUTS 1 "+ title)

#send_miconv3("LED_OFF 3 0")
#send_miconv3("LED_OFF 4 0")
#send_miconv3("LED_OFF 5 0")

#send_miconv3("LED_ON 3 0")
#send_miconv3("LED_ON 4 0")
#send_miconv3("LED_ON 5 0")

send_miconv3("LED_ON 0 0")

#eeprom_dump()


#for x in [1,2,3,4]:
#	recv_miconv3()


#str= "LCD_PUTS 0 What a \r"
#str2= "LCD_PUTS 1 Team! \r"

#output = bytearray()
#output.extend(map(ord, str))

#port.write(output)

#output = bytearray()
#output.extend(map(ord, str2))

#port.write(output)


#port.close()
