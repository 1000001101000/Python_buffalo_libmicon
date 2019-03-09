#!/usr/bin/python3

import time
import datetime
import serial
from serial import Serial

retry_count = 2

CMD_MODE_READ		= 0x80

CMD_OPERATION_SOUND	= 0x30
DT_BZ_STOP	= 0x00
DT_BZ_MACHINE	= 0x01
DT_BZ_BUTTON	= 0x02
DT_BZ_CONTINUE	= 0x03
DT_BZ_SWITCH1	= 0x04
DT_BZ_SWITCH2	= 0x10
DT_BZ_MUSIC1	= 0x30
DT_BZ_MUSIC2	= 0x20

LED_ON		= 1
LED_OFF		= 0
LED_BLINK	= 2

CMD_LED_CPU	= 0x50
CMD_LED_ONOFF	= 0x51
CMD_LED_BLINK	= 0x52

POWER_LED	= [0x09,0x00]
INFO_LED        = [0x02,0x00]
ERROR_LED       = [0x04,0x00]
LAN1_LED	= [0x20,0x00]
LAN2_LED        = [0x40,0x00]
FUNC1_LED	= [0x10,0x00]
FUNC2_LED	= [0x80,0x00]
DISP_LED	= [0x00,0x80]

SATA_LED_ONOFF	= 0x58
SATA_LED_BLINK	= 0x59

SATA_ALL	= [0xFF,0xFF] ##works for off but not on? 
SATA_ALL_GREEN	= [0x00,0xFF]
SATA_ALL_RED	= [0xFF,0x00]

SATA1_RED	= [0x01,0x00]
SATA2_RED	= [0x02,0x00]
SATA3_RED       = [0x04,0x00]
SATA4_RED       = [0x08,0x00]
SATA5_RED       = [0x10,0x00]
SATA6_RED       = [0x20,0x00]
SATA7_RED       = [0x40,0x00]
SATA8_RED       = [0x80,0x00]

SATA1_GREEN	= [0x00,0x01]
SATA2_GREEN     = [0x00,0x02]
SATA3_GREEN     = [0x00,0x04]
SATA4_GREEN     = [0x00,0x08]
SATA5_GREEN     = [0x00,0x10]
SATA6_GREEN     = [0x00,0x20]
SATA7_GREEN     = [0x00,0x40]
SATA8_GREEN     = [0x00,0x80]

CMD_LCD_BRIGHTNESS	= 0x3A

CMD_LCD_LINK		= 0x20  ##0x31 0x00 - 0x05
CMD_LCD_DISK_USAGE	= 0x21  ## 4 bars controlled by bytes of 0x60 (bar height 00-0F, toggle up arrow with 1_)
CMD_LCD_IPADDRESS	= 0x22  ##write: top=0x80 bottom=0x81
CMD_LCD_OPMODE		= 0x23  ##write via 0x94; just top row via 0x82?
CMD_LCD_DATE		= 0x24  ##timer which can be updated at 0x70
CMD_LCD_BUFFER0		= 0x25  ##write via 0xA5 or 0x93 or 0x90?
CMD_LCD_BUFFER1         = 0x26  ##write via 0xA5 or 0x91?
CMD_LCD_BUFFER2         = 0x27  ##write via 0xA7 or 0x92?
CMD_LCD_BUFFER3         = 0x2B
CMD_LCD_BUFFER4         = 0x2C
CMD_LCD_BUFFER5         = 0x2D
CMD_LCD_BUFFER6         = 0x2E
CMD_LCD_BUFFER7         = 0x2F

## 0x00 = "No Link"
## 0x01 = "10Mbps HALF"
## 0x02 = "10Mbps FULL"
## 0x03 = "100Mbps HALF"
## 0x04 = "100Mbps FULL"
## 0x05 = "1000Mbps"

READ_ONLY_MODEL_STRING  = 0x83


class micon_api:
	port = serial.Serial('/dev/ttyS1', 38400, serial.EIGHTBITS, serial.PARITY_EVEN,\
                        stopbits=serial.STOPBITS_ONE, timeout=0.1)
	def __init__(self):
	##need to either figure out autodetect or take params

		port = serial.Serial()

	def calc_check_byte(self,bytes):
		checkbyte = 0x00
		for byte in bytes:
			checkbyte += byte
			checkbyte %= 256
		checkbyte^=0xFF
		checkbyte+=0x01
		checkbyte%=256
		return checkbyte

	def calc_checksum(self,bytes):
		checksum = 0x00
		for byte in bytes:
                	checksum += byte
		checksum%=256
		return checksum

	def send_bytes(self, output):
		self.port.write(output)

	def send_preamble(self):
		bytelist= [0xFF]*32
		preamble = bytearray(bytelist)
		self.send_bytes(preamble)

	def send_cmd(self, cmdbytes):
		response = 0xFF
		if type(cmdbytes) == "int":
			cmdbytes = bytearray([cmdbytes])
		cmdbytes.append(self.calc_check_byte(cmdbytes))
		print ("sending : ", bytes(cmdbytes).hex()," ",self.calc_checksum(cmdbytes)," ...", end="")
		for x in range(retry_count):
			self.send_bytes(cmdbytes)
			response = self.get_response()
			if self.calc_checksum(response) == 0:
				print ("OK")
				print ("Response: ", bytes(response).hex())
				print ("")
				return response
			self.send_preamble()
		print ("Error")

	def send_read_cmd(self, addrbyte):
		cmdbytes=bytearray()
		cmdbytes.append(0x80)
		cmdbytes.append(addrbyte)
		response = self.send_cmd(cmdbytes)
		if (response[0] & 0x80) == 0:
			print ("invalid response")
			return False
		response_len = response[0]^0x80
		if (response_len != (len(response)-3)):
			print ("invalid response")
			return False
		output = bytearray()
		for x in range(response_len):
			output.append(response[x+2])
		print ("response: ", bytes(output).hex())
		return output

	def send_write_cmd(self, length, addrbyte, databytes):
		#validate length or perhaps stop requiring it or something
		if type(databytes) == int:
                	databytes = bytearray([databytes])
		cmdbytes=bytearray()
		cmdbytes.append(length)
		cmdbytes.append(addrbyte)
		for databyte in databytes:
			cmdbytes.append(databyte)
		return self.send_cmd(cmdbytes)

	def get_response(self):
		##maybe add an option buffer size
		##it would be nice to stop hitting the timout.
		##we could also get cute and determine when to stop based on response
		response = self.port.read(32)
		return response

	def cmd_sound(self, soundcmd):
		return self.send_write_cmd(1, CMD_OPERATION_SOUND, soundcmd)

	def cmd_set_sataled(self, mode, led):
		led_mask = bytearray(led)
		inv_mask = bytearray()
		inv_mask.append(led_mask[0] ^ 0xFF)
		inv_mask.append(led_mask[1] ^ 0xFF)
		led_status=self.send_read_cmd(SATA_LED_BLINK)
		if mode != LED_BLINK:
			led_status[0] &= inv_mask[0]
			led_status[1] &= inv_mask[1]
		else:
			led_status[0] |= led_mask[0]
			led_status[1] |= led_mask[1]
		self.send_write_cmd(2,SATA_LED_BLINK,led_status)
		led_status=self.send_read_cmd(SATA_LED_ONOFF)
		if mode == LED_OFF:
			led_status[0] &= inv_mask[0]
			led_status[1] &= inv_mask[1]
		else:
			led_status[0] |= led_mask[0]
			led_status[1] |= led_mask[1]
		self.send_write_cmd(2,SATA_LED_ONOFF,led_status)

	def cmd_set_led(self, mode, led):
		led_mask = bytearray(led)
		inv_mask = bytearray()
		inv_mask.append(led_mask[0] ^ 0xFF)
		inv_mask.append(led_mask[1] ^ 0xFF)

		led_status=self.send_read_cmd(CMD_LED_CPU)
		led_status[0] |= led_mask[0]
		led_status[1] |= led_mask[1]
		self.send_write_cmd(2,CMD_LED_CPU,led_status)

		led_status=self.send_read_cmd(CMD_LED_BLINK)
		if mode != LED_BLINK:
			led_status[0] &= inv_mask[0]
			led_status[1] &= inv_mask[1]
		else:
			led_status[0] |= led_mask[0]
			led_status[1] |= led_mask[1]
		self.send_write_cmd(2,CMD_LED_BLINK,led_status)

		led_status=self.send_read_cmd(CMD_LED_ONOFF)
		if mode == LED_OFF:
			led_status[0] &= inv_mask[0]
			led_status[1] &= inv_mask[1]
		else:
			led_status[0] |= led_mask[0]
			led_status[1] |= led_mask[1]
		self.send_write_cmd(2,CMD_LED_ONOFF,led_status)
		#send_write_cmd(port,2,CMD_LED_CPU,inv_mask)

	def set_lcd_brightness(self, led_byte, lcd_byte):
		cmdbytes=bytearray([led_byte | lcd_byte])
		self.send_write_cmd(1,CMD_LCD_BRIGHTNESS,cmdbytes)

	def get_lcd_brightness(self):
        	self.send_read_cmd(CMD_LCD_BRIGHTNESS)

	#both unsure what this does, exactly and whether it's right
	def cmd_set_lcddisp(self, mode, led):
		led_mask = bytearray(led)
		inv_mask = bytearray()
		inv_mask.append(led_mask[0] ^ 0xFF)
		inv_mask.append(led_mask[1] ^ 0xFF)
		led_status = bytearray([0x00,0x00])
		led_status[0] = self.send_read_cmd(0x32)[0]
		led_status[1] = self.send_read_cmd(0x40)[0]
		if mode == LED_OFF:
			led_status[0] &= inv_mask[0]
			led_status[1] &= inv_mask[1]
		else:
			led_status[0] |= led_mask[0]
			led_status[1] |= led_mask[1]
		self.send_write_cmd(1,0x32,led_status[0])
		self.send_write_cmd(1,0x40,led_status[1])

	def cmd_force_lcd_disp(self, dispbyte):
		self.send_write_cmd(0,dispbyte,"")

	def set_lcd_buffer(self, bufferbyte, row1, row2):
		row1 = row1.ljust(16)
		row1 = row1[:16]
		row2 = row2.ljust(16)
		row2 = row2[:16]
		message = row1 + row2
		messagebytes = bytearray()
		messagebytes.extend(map(ord,message))
		self.send_write_cmd(32, bufferbyte,messagebytes)

	def set_lcd_buffer2(self, bufferbyte, message):
        	message = message.ljust(16)
        	message = message[:16]
        	messagebytes = bytearray()
        	messagebytes.extend(map(ord,message))
        	self.send_write_cmd(16, bufferbyte,messagebytes)

	def set_lcd_date(self):
		currentDT = datetime.datetime.now()
		##made sure it could go beyond 2099 because we must never forget Y2K
		##1-byte ensures it will only go to 2255 but future generations can deal with that.
		year=int(currentDT.strftime('%Y'))-2000
		mon=int(currentDT.strftime('%m'))
		day=int(currentDT.strftime('%d'))
		hour=int(currentDT.strftime('%H'))
		min=int(currentDT.strftime('%M'))
		sec=int(currentDT.strftime('%S'))
		output=bytearray([year,mon,day,hour,min,sec])
		self.send_write_cmd(6,0x70,output)

