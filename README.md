# Python_buffalo_libmicon
Python3 Library for communicating with the microcontroller on the Buffalo Terastation

This library allows you to communicate with the onboard microcontroller which controls the LCD Display, LEDs, buzzer and other funcitons on most models of Buffalo Terastation. It uses Python3 and the PySerial library.

So far It has been tested on these model Terastations running Debian Stable:
* TS-WVHL/QVHL/6VHL/8VHL/RVHL
* TS3000 Series
* TS5000 Series
* TS1000 Series (TS1200 except the TS1200)


### Installation:

`apt-get install python3 python3-pip`

`pip3-install pyserial`

### Usage:

I've provided examples.py which demonstrates how to use most typical functions. It can be run either as:

`./examples.py` or `python3 examples.py`

To see the details of the messages being send and received enable debug mode by:
`conn = libmicon.micon_api("/dev/ttyS1",1)

For more details about the communication format and the available commands see:
https://buffalonas.miraheze.org/wiki/Terastation_Microcontroller_Interface
