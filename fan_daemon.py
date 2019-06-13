#!/usr/bin/python3

import libmicon
import subprocess
import time


while True:
	test = libmicon.micon_api("/dev/ttyS1")
	current_fan = test.send_read_cmd(libmicon.fan_set_speed)
	current_fan2 = test.send_read_cmd(0x38)
	print("Current fan speed:\t",current_fan[0],"\t",current_fan2[0])

	high_sensor = 0
	high_drive = 0

	p = subprocess.Popen("""sensors | grep temp1 | gawk '{print $2}' | sed 's/[+°CF]//g'""", stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	for x in output.splitlines():
		tmp_sensor = float(x.decode("utf-8"))
		if tmp_sensor > high_sensor:
			high_sensor = tmp_sensor

	p = subprocess.Popen("""hddtemp /dev/sd* | gawk -F: '{print $3}' | sed 's/[ °CF]//g'""", stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	for x in output.splitlines():
        	tmp_sensor = float(x.decode("utf-8"))
        	if tmp_sensor > high_drive:
                	high_drive = tmp_sensor

	print ("Highest temp sensor:\t",high_sensor)
	print ("Highest HDD temp:\t",high_drive)

	if high_sensor > 62 or high_drive > 42:
		new_speed=3
	elif high_sensor > 58 or high_drive > 37:
                new_speed=2
	else:
		new_speed=1

	test.send_write_cmd(1,0x33,new_speed)
	test.port.close()
	time.sleep(120)
quit()
