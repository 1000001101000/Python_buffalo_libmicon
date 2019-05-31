#!/usr/bin/python3

import libmicon
import time

test = libmicon.micon_api("/dev/ttyS1")

print("")
print("Displaying values for all addresses that return data. See:")
print("https://buffalonas.miraheze.org/wiki/Terastation_Microcontroller_Interface")
print("for more information")
print("")

##configure to cycle through displays via the display button

state=test.send_read_cmd(0x36)
oldstate=state
while True:
	state=test.send_read_cmd(0x36)
	if oldstate != state:
		print(state.hex())
		oldstate=state
	time.sleep(0.5)

test.port.close()
quit()
