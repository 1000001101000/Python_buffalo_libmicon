#!/usr/bin/python3

import libmicon

test = libmicon.micon_api("/dev/ttyS1")

response=test.send_read_cmd(0x83)
print(str(response, 'utf-8'))

test.port.close()
quit()
