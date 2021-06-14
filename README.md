# Python_buffalo_libmicon
If this project helps you click the Star at the top of the page to let me know!

Python3 Library for communicating with the microcontroller on the Buffalo Terastation and some older Linkstations.

This library allows you to communicate with the onboard microcontroller which controls the LCD Display, LEDs, buzzer and other funcitons on most models of Buffalo Terastation. It uses Python3 and the PySerial library.

So far It has been tested on these model Terastations/Linkstations running Debian Stretch and Buster:
* TS-WVHL/QVHL/6VHL/8VHL/RVHL (Intel-based Terastation Pro)
* TS1000 Series (except the TS1200)
* TS3000 Series
* TS3010 Series
* TS5000 Series
* TS5020 Series
* TS6000 Series
* TS-XEL (Terastation ES)
* TS-WXL/XL/RXL (Terastation III)
* TS-HTGL (Terastation II Pro)
* TS-TGL (Terastation Pro)
* LS-GL


### Installation:

Debian:

`apt-get install python3 python3-pip`

`pip3-install pyserial`

other linux distros should be similar.

FreeBSD has packages for Python3 and comms/py-pyserial for the serial library.

### Usage:

I've provided examples.py which demonstrates how to use most typical functions. It can be run either as:

`./examples.py` or `python3 examples.py`

To see the details of the messages being send and received enable debug mode by:

`conn = libmicon.micon_api("/dev/ttyS1",1)`

Under Linux the serial port should just about always be /dev/ttyS1 but there are some configurations where it could be ttyS0/2/3. Under FreeBSD I've seen it as /dev/ttyu1, I assume other BSD variants are similar. I assume under Windows it would be COM2 or something similar but I have yet to hear from someone who has tried that. 

For more details about the communication format and the available commands see:
https://buffalonas.miraheze.org/wiki/Terastation_Microcontroller_Interface
