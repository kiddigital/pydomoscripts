# pydomoscripts
Some Python(3) scripts for use with Domoticz

** Used/testen with Domoticz V4.9788 Beta and Dashticz v2 Beta on  RPi **

## script_device_DomLcdStandBy.py & script_time_DomLcdBright.py

The _script\_device\__ script is a scripts that gets called each time a device change occurs in Domoticz

The _script\_time\__ scripts gets called every 1 minute by Domoticz

Both scripts can use a prefilled dictionary object when doing _import domoticz_ which contains most (all?) devices of domoticz with their current state/values so there is no need to use a seperate interface (like JSON URL) to get values. Unfortunately, you can not use this dictionary to interact with the devices, except for simple On/Off devices.

How/why do I use these scripts:
* A have a virtual on/off switch which gets triggered through the JSON URL API by Dashticz. If the Dashticz dashboard goes in Standby mode, or comes out of it, the device URL is called to change the device state.
* This device state change triggers the Python event system and executes all *script\_device\_* scripts within the *scripts/python* directory
* So the *DomLcdStandBy* scripts checks if the reason for execution is indeed the state change of the expected device
** Depending on on or off, it increases or decreases the brightness of the display
* The second script *DomLcdBright* get called every minute and reads the actual brightness setting from the display
** If the value is different from the value within the virtual sensor that registers the brightness, given in percentage, the virtual sensor is updated with the new value

Note: the (remote) display in this case is the standard RPi touchscreen running on a Pi 3B with Raspian Stretch

