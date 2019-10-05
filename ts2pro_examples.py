#!/usr/bin/python3

import libmicon
import socket
import time

test = libmicon.micon_api("/dev/ttyS1",1)


#turn off all LED then cycle through turning them on.
test.cmd_set_led(libmicon.LED_OFF,[0xFF,0x00])

for led in [libmicon.POWER_LED, libmicon.INFO_LED, libmicon.ERROR_LED]:
	test.cmd_set_led(libmicon.LED_OFF,led)
	test.cmd_set_led(libmicon.LED_ON,led)
	time.sleep(1)
	test.cmd_set_led(libmicon.LED_OFF,led)


#set LCD backlight brightness
for level in [libmicon.LCD_BRIGHT_OFF,libmicon.LCD_BRIGHT_LOW,libmicon.LCD_BRIGHT_MED,libmicon.LCD_BRIGHT_FULL]:
	test.set_lcd_brightness(level)
	time.sleep(0.25)

test.cmd_sound(libmicon.BZ_MUSIC2)

test.port.close()
quit()
