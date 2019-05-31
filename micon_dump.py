#!/usr/bin/python3

import libmicon

test = libmicon.micon_api("/dev/ttyS1")

print("")
print("Displaying values for all addresses that return data. See:")
print("https://buffalonas.miraheze.org/wiki/Terastation_Microcontroller_Interface")
print("for more information")
print("")

##configure to cycle through displays via the display button
for x in range(256):
	response=test.send_read_cmd(x)
	if response.hex() == "f4":
		continue
	print(hex(x),": ",response.hex())

test.port.close()
quit()
