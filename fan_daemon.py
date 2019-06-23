#!/usr/bin/python3

import libmicon
import subprocess
import time

with open("/proc/device-tree/model") as f:
    content = f.readlines()
device_model = (content[0].split(" ")[2])

translation_table = dict.fromkeys(map(ord, '°CF'), None)

##try reading micon version from each port to determine the right one
for port in ["/dev/ttyS1","/dev/ttyS3"]:
	test = libmicon.micon_api(port)
	result = test.send_read_cmd(0x83)
	if result:
		break
	test.port.close()

while True:
	current_fan = test.send_read_cmd(libmicon.fan_set_speed)
	current_fan2 = test.send_read_cmd(0x38)
	print("Current fan speed:\t",current_fan[0],"\t",current_fan2[0])

	high_sensor = 0
	high_drive = 0

	p = subprocess.Popen("""sensors""", stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()

	for x in output.splitlines():
		line = x.decode("utf-8")
		line = line.translate(translation_table)
		if line.find("temp1") == -1:
			continue
		tmp_sensor = float(line.split()[1])
		if tmp_sensor > high_sensor:
			high_sensor = tmp_sensor

	p = subprocess.Popen("""hddtemp /dev/sd*""", stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	for x in output.splitlines():
		line = x.decode("utf-8")
		line = line.translate(translation_table)
		tmp_sensor = float(line.split(":")[2])
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
	###never command it to stop, though we could

	test.send_write_cmd(1,0x33,new_speed)
	test.port.close()
	time.sleep(120)
quit()
