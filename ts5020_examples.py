#!/usr/bin/python3

import platform
import time
import libmicon

test = libmicon.micon_api_v3("/dev/ttyS0")

# set LCD display
line1 = ("Line 1").center(16, u"\u00A0")
line2 = "Line 2"

print(test.set_lcd(0, line1))
print(test.set_lcd(1, line2))

# sound test
print(test.sound(440, 500))

# turn off all LEDs
for i in range(16):
    test.set_led(i, "off")

# cycle modes on each LED
for i in range(16):
    test.set_led(i, "on")
    test.set_lcd(0, "LED " + str(i))
    time.sleep(0.5)
    test.set_led(i, "blink", 100)
    time.sleep(0.5)
    test.set_led(i, "off")

test.set_led(0, "on")
test.set_led(4, "on")
test.set_led(5, "on")

# print eeprom info
# print(test.eeprom_read(0))

test.eeprom_print(1024)
# eeprom_dump()
