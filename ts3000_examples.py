#!/usr/bin/python3

import libmicon
import socket
import time

test = libmicon.micon_api("/dev/ttyS3",1)

##to enable debug info change to
#test = libmicon.micon_api(1)

##update the date for the lcd display
test.set_lcd_date()
test.cmd_force_lcd_disp(libmicon.lcd_disp_date)
time.sleep(1)

##set the ip address for the lcd display
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('10.255.255.255', 1))
host_ip = s.getsockname()[0]
s.close()
host_name = socket.gethostname()
test.set_lcd_buffer_short(libmicon.lcd_set_ipaddress,host_ip)
test.set_lcd_buffer_short(libmicon.lcd_set_hostname,host_name)

test.cmd_force_lcd_disp(libmicon.lcd_disp_hostname)
time.sleep(1)

##set link speed (just to gbps)
test.send_write_cmd(1,libmicon.lcd_set_linkspeed,libmicon.LINK_1000M)
test.send_write_cmd(1,0x37,libmicon.LINK_1000M)
test.cmd_force_lcd_disp(libmicon.lcd_disp_linkspeed)
time.sleep(1)

##set drive capacity graphs with bogus values
test.set_lcd_drives(libmicon.GRAPH_25p,libmicon.GRAPH_50p,libmicon.GRAPH_75p,libmicon.GRAPH_100p)
test.cmd_force_lcd_disp(libmicon.lcd_disp_diskcap)
time.sleep(1)

##set custom lcd message
test.set_lcd_buffer(libmicon.lcd_set_buffer0,"Terastation ARM","   Debian")
test.cmd_force_lcd_disp(libmicon.lcd_disp_buffer0)

##enable just the messages that we've configured so far.
test.send_write_cmd(1,libmicon.lcd_set_dispitem,0x3F)
test.send_write_cmd(1,libmicon.lcd_set_dispitem_ex,0x00)

##configure to cycle through displays via the display button
test.send_write_cmd(0,libmicon.lcd_changemode_button)

##configure to cycle through displays every ~3 seconds
#test.send_write_cmd(0,libmicon.lcd_changemode_auto)

##turn off all sata leds then cycle through them
#test.cmd_set_sataled(libmicon.LED_OFF,libmicon.SATA_ALL_LED)



test.cmd_set_led(libmicon.LED_OFF,bytearray([0x00,0xF0]))
for led in [libmicon.SATA5_GREEN, libmicon.SATA6_GREEN, libmicon.SATA7_GREEN, libmicon.SATA8_GREEN]:
	test.cmd_set_led(libmicon.LED_ON,led)
	time.sleep(1)
test.cmd_set_led(libmicon.LED_OFF,bytearray([0x00,0xF0]))


#turn off all LED then cycle through turning them on.
test.cmd_set_led(libmicon.LED_OFF,[0xFF,0x00])

for led in [libmicon.POWER_LED, libmicon.INFO_LED, libmicon.ERROR_LED, libmicon.LAN1_LED, libmicon.LAN2_LED, libmicon.FUNC1_LED, libmicon.FUNC2_LED]:
	test.cmd_set_led(libmicon.LED_OFF,led)
	test.cmd_set_led(libmicon.LED_ON,led)
	time.sleep(0.5)
	test.cmd_set_led(libmicon.LED_OFF,led)

#cycle through all the backlight combinations
for color in [libmicon.LCD_COLOR_RED, libmicon.LCD_COLOR_BLUE, libmicon.LCD_COLOR_GREEN, libmicon.LCD_COLOR_ORANGE, libmicon.LCD_COLOR_AQUA]:
	test.set_lcd_color(color)
	time.sleep(0.5)

#set LCD backlight brightness
for level in [libmicon.LCD_BRIGHT_OFF,libmicon.LCD_BRIGHT_LOW,libmicon.LCD_BRIGHT_MED,libmicon.LCD_BRIGHT_FULL]:
	test.set_lcd_brightness(level)
	time.sleep(0.25)

#run some standalone commands
#test.send_write_cmd(0,libmicon.lcd_disp_animation)

#try every possible sound setting.
test.cmd_sound(libmicon.BZ_MUSIC2)

test.port.close()
quit()
