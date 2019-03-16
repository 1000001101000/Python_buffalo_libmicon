#!/usr/bin/python3

import libmicon
import socket
import time

test = libmicon.micon_api("/dev/ttyS1")

test.cmd_sound(BZ_MUSIC1)

##to enable debug info change to
#test = libmicon.micon_api(1)
test.send_cmd(bytearray([0x02,0x50,0x0F,0x00]))
test.send_cmd(bytearray([0x02,0x51,0x06,0x00]))
#0x02 and 0x04 are ...pink power leds or something. the rest are gpio anyway

##all red drive leds on
test.send_cmd(bytearray([0x02,0x50,0x00,0xF0]))
test.send_cmd(bytearray([0x02,0x51,0x00,0xF0]))

##all red drive leds off
test.send_cmd(bytearray([0x02,0x50,0x00,0xF0]))
test.send_cmd(bytearray([0x02,0x51,0x00,0x00]))

##red sata blink
test.send_cmd(bytearray([0x02,0x50,0x00,0xF0]))
test.send_cmd(bytearray([0x02,0x51,0x00,0xF0]))
test.send_cmd(bytearray([0x02,0x52,0x00,0xF0]))

test.port.close()
quit()
