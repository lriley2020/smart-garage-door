# Operation via button
A button can be connected between pin D3 and GND. The control
The button can be activated time-controlled using the parameters cfgTimeOn and cfgTimeOff

##### Example
    "cfgTimeOn": 11, "cfgTimeOff": 13
The button can only be used from 11:00 a.m. to 1:00 p.m. Outside this time wi

##### Default
    "cfgTimeOn": 24, "cfgTimeOff": 0
The button is permanently blocked (since the hour is never > 24 and < 0).

# Automatic closing
For example, the gate can be closed automatically in the evening. For safety reasons
- short movement downwards
- Waiting period
- complete closure

##### Example
    "cfgAcTime": 22, "cfgAcDur1": 2, "cfgAcDur2": 30
If the gate is not closed at 10:00 p.m., it will go towards low a for 2s

##### Default
    "cfgAcTime": 24, "cfgAcDur1": 2, "cfgAcDur2": 30
The function is deactivated (since hour never > 24)
  
# Parcel service function (beta)
The parcel service function makes sense in combination with the keypad. You erm
The parcel service can then push its parcels into the garage and close the door
**Attention:** An opening width of more than 30cm may only be set w

The function can be enabled depending on the time (see operation via button)
**Attention:** The function is currently still being tested.

##### Default
    "cfgPdTimeOn": 24, "cfgPdTimeOff": 0
The function is permanently blocked (since the hour is never > 24 and < 0).
  
  
# Operation via keypad
A 4x4 keypad in combination with a PCF8574 can be connected via I2C

SDA: Pin D5
SCL: Pin D6
I2C address: 0x20 (= all jumpers plugged into the PCF8574)
  
<img src="https://i.ibb.co/K2q8grm/KeyPanel.png">
  
To activate the function you need to create a file called " at http://x.x.x.x/edit

    0000;0;Name;
    9999;0;Two;
    1234;1;DHLUPS;

The code must be exactly 4 characters long and cannot begin with "D" ("D" is
The number after it indicates the function:
- 0: Open
- 1: Parcel delivery function

Finally, a name of up to 10 characters long must be provided.

When you press the first button, a timer starts. After 8s a code can be entered again

# Operation via RFID
To activate the function you need to create a file called " at http://x.x.x.x/edit

    1234abcd;name;
    deadbeef;Two;
    aa55aa55;Three;

The RFID tag code must be exactly 8 characters long. The name can have a maximum of 10
  
# Record recent trips
The last trips are recorded at http://x.x.x.x/edit. The file name
The files are deleted after 3 months (cfgLogMonths).

##### Example
    11/3/2021, 1:50:44 p.m.: Keypad: Code 0000
    11/03/2021, 1:50:45 p.m.: Keypad: Open
    11/03/2021, 1:50:59 p.m.: Unknown: Open
    11/03/2021 1:54:43 p.m.: Keypad: Close
    11/03/2021, 1:55:04 p.m.: Unknown: Closed
    November 3rd, 2021, 2:06:20 p.m.: Button: Open
