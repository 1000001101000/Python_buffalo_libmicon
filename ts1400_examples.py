#!/usr/bin/python3

import libmicon
import time

test = libmicon.micon_api("/dev/ttyS1")
#test = libmicon.micon_api("/dev/ttyS1",1)


##turn off all sata leds then cycle through them
test.cmd_set_led(libmicon.LED_OFF,bytearray([0x00,0xF0]))
for led in [libmicon.SATA5_GREEN, libmicon.SATA6_GREEN, libmicon.SATA7_GREEN, libmicon.SATA8_GREEN]:
	test.cmd_set_led(libmicon.LED_ON,led)
	time.sleep(1)
test.cmd_set_led(libmicon.LED_OFF,bytearray([0x00,0xF0]))


#turn off all LED then cycle through turning them on.
test.cmd_set_led(libmicon.LED_OFF,[0xFF,0x00])

for led in [libmicon.INFO_LED, libmicon.ERROR_LED]:
	test.cmd_set_led(libmicon.LED_OFF,led)
	test.cmd_set_led(libmicon.LED_ON,led)
	time.sleep(1)
	test.cmd_set_led(libmicon.LED_OFF,led)

#play a sound
test.cmd_sound(libmicon.BZ_MUSIC2)

test.port.close()
quit()
