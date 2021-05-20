#!/usr/bin/python3

import libmicon
import time

print("")
print("Press Buttons on the Device and watch the ouput")
print("Enter CTRL-C to quit")
print("")

oldstate=0
while True:
	test = libmicon.micon_api("/dev/ttyS1")
	state=test.send_read_cmd(0x36)
	if oldstate != state:
		print("Button(s): ", end='')
		for button_num in range(8):
			if state[0] & (2**button_num) == 0:
				print(2**button_num," ", end='')
		print("")

	oldstate=state
	time.sleep(0.5)

test.port.close()
quit()
