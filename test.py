#!/usr/bin/python3

import libmicon

test = libmicon.micon_api()

test.set_lcd_date()
##set custom lcd message
test.set_lcd_buffer(0xA0,"Terastation x86","   Debian 9.8")

#blank turn off all LEDs
test.cmd_set_led(libmicon.LED_OFF, [0xFF,0x0F] )

#enable power led and link led, set backlight as blue+green
test.cmd_set_led(libmicon.LED_ON, [0x29,0x06] )

#set lcd backlight to maximum
test.set_lcd_brightness(0xF0, 0x0F)

#display custom lcd message
test.cmd_force_lcd_disp(0x25)

#play a sound!
test.cmd_sound(0x20)

test.port.close()
quit()
