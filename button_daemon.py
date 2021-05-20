#!/usr/bin/python3

##simple example of polling one button and taking an action if it is held down.

import libmicon
import os
import time

press_time=2
poll_speed=0.5 ##currently this is fast as we can reliably poll
button_num=1  ##buttons are each a power of 2, "1" is power button on most ARM devices
tickcnt=0

while True:
	test = libmicon.micon_api("/dev/ttyS1")
	state=int.from_bytes(test.send_read_cmd(0x36),byteorder="big") & button_num
	##power button on ts3400 0=pressed, 1=not pressed
	##if button held down start counting
	if state == 0:
		tickcnt=tickcnt +1
		if tickcnt > (press_time/poll_speed):
			test.set_lcd_buffer(0x90,"Shutting Down!!"," ")
			test.cmd_force_lcd_disp(libmicon.lcd_disp_buffer0)
			test.send_write_cmd(1,libmicon.lcd_set_dispitem,0x20)
			test.set_lcd_color(libmicon.LCD_COLOR_RED)
			test.set_lcd_brightness(libmicon.LCD_BRIGHT_FULL)
			test.cmd_sound(libmicon.BZ_MUSIC1)
			test.port.close() ##if we do something other than shutdown we'd probably skip this
			os.system('shutdown -h 0')
			tickcnt=0

	##reset counter if released
	else:
		tickcnt=0

	test.port.close()
	##currently this is fast as we can reliably poll
	time.sleep(poll_speed)
quit()
