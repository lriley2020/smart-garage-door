## WLAN setup / access point mode
If the system cannot connect to a WLAN, it opens its own access point with the following steps
- SSID: hgdo
- Password: hgdo1234

Entering your own WLAN data:
- Establish a connection to the above-mentioned WLAN
- Go to http://192.168.4.1 (recommended: Chrome, Edge)
- Select your own WLAN and enter your password

The system will connect to the WLAN and will be assigned an IP by the router. If it's not on the first month

The access point is sometimes unstable, especially with Android. But it works well with laptop/iPhone.

After setup, it is recommended to change the cfgApPass parameter and create an individual password (at least 8 characters

The WLAN data can be set to default using http://x.x.x.x/resetwifi.

## Software update
The *.bin files can be flashed via USB or via OTA using https://github.com/marcelstoer/nodemcu-pyflasher
The html/css/js files for the web interface can also be uploaded later from the 'data' directory
  
Deletion (Erase) is usually not necessary.
If the ESP8266 is deleted before flashing, the WLAN access data will be deleted and the configuration will be lost

#### OTA
Before an over-the-air update, communication with the drive must be stopped: http://x.x.x.x/stopcom
Only then can the new *.bin file be uploaded via http://x.x.x.x/update.
