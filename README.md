# Python_buffalo_libmicon
Python3 Library for communicating with the microcontroller on the Buffalo Terastation

This library allows you to communicate with the onboard microcontroller which controls the LCD Display, LEDs, buzzer and other funcitons on most models of Buffalo Terastation. It uses Python3 and the PySerial library.

So far It has been tested on these model Terastations running Debian Stable:
* TS-WVHL/QVHL/6VHL/8VHL/RVHL
* TS3000
* TS5000

***I'm still working on the TS1400, I can send commands successfully but am not receiving responses, considering the relatively few needed commands for the TS1400 I may just create a seperate version that only sends that subset of commands If I can't figure it out.

### Installation:

`apt-get install python3 python3-pip`

`pip3-install pyserial`

**Depending on the model you may need to change the serial port in libmicon.py, it's typically /dev/ttyS1 but on the TS3400 it is /dev/ttyS3. 

### Usage:

I've provided examples.py which demonstrates how to use most typical functions. It can be run either as:

`./examples.py` or `python3 examples.py`

To see the details of the messages being send and received enable debug mode by:
`conn = micon_api(1)`

For more details about the communication format and the available commands see:
https://buffalonas.miraheze.org/wiki/Terastation_Microcontroller_Interface
