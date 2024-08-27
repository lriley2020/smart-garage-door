import network
import utime
from umqtt.simple import MQTTClient
import machine
import json
import uasyncio
from secrets import *


#led = machine.Pin("LED", machine.Pin.OUT)

## Door control code ##
door_output_pin = machine.Pin(0, mode=machine.Pin.OUT)


# We assume here that the initial status of the door will be closed #
door_status = "closed"

def button_impulse():
    door_output_pin.high()
    utime.sleep(0.5)
    door_output_pin.low()


def door_open():
    button_impulse()
    print("Opening door...")

def door_close():
    button_impulse()
    print("Closing door...")

def door_stop():
    button_impulse()
    print("Stopping door...")

### Setup wifi connection ###

ssid = Wifi.ssid
password = Wifi.password
hostname = Wifi.hostname

def wifi_setup():
    print("Starting WLAN connection...")
    network.hostname(hostname)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        utime.sleep(1)
    print("WLAN connection successful...")
    print(wlan.ifconfig())
    
wifi_setup()


## This function is called when there is a new message from the MQTT broker ###
def mqtt_callback(topic, msg):
    global door_status
    topic = topic.decode("utf-8")
    msg = msg.decode("utf-8")
    print(f"New message on topic '{topic}': {msg}")
    
    if topic == "home/homeassistant/status":
        if msg == "online":
            print("HA available again, sending device config")
            send_ha_discovery()
        elif msg == "offline":
            print("HA has gone offline...")
            
    if topic == "home/garage/garage-door/ctrl":
        ### We only have toggle functionality for now :( ###
        if msg == "OPEN":
            ## Record time that the open command was sent in case of a stop command ##
            global operation_start_time
            operation_start_time = utime.time()
            door_open()
            door_status = "opening"
            send_ha_status()
        elif msg == "CLOSE":
            ## Record time that the close command was sent in case of a stop command ##
            global operation_start_time
            operation_start_time = utime.time()
            door_close()
            door_status = "closing"
            send_ha_status()
        elif msg == "STOP":
            ## Check if we actually need to do anything - if the door is not in motion then we can ignore this message ##
            
            try:
                time_since_operation = utime.time() - operation_start_time
            except NameError:
                ## If the door has not been moved since the last reboot, this var is not set so we can just ignore ##
                print("Warning: stop command was ignored...")
                return
                
            ## If it's been >15s since a command was last sent, we assume door is no longer in motion and ignore the stop command ##
            if time_since_operation > 15:
                print("Warning: stop command was ignored...")
                return
            ## Now we must handle the stop command ##
            door_stop()
            door_status = "stopped"
            send_ha_status()
            

### Setup MQTT connection ###
mqtt_client_id = MQTT.client_id
mqtt_server = MQTT.server
mqtt_port = MQTT.port
mqtt_user = MQTT.user
mqtt_password = MQTT.password

def mqtt_connect():
    client = MQTTClient(mqtt_client_id, mqtt_server, port=mqtt_port, user=mqtt_user, password=mqtt_password)
    client.connect()
    client.set_callback(mqtt_callback)
    return client

def reconnect():
    print('Failed to connect to MQTT Broker. Rebooting...')
    utime.sleep(5)
    machine.reset()
    
try:
    print("Starting MQTT connection...")
    client = mqtt_connect()
except OSError:
    reconnect()
    
print("MQTT connection successful")

### Subscribe to our control topic ###
client.subscribe(b"home/garage/garage-door/ctrl")
### Subscribe to the homeassistant status topic so that we can re-publish our config when homeassistant reboots, so it recognises us again ###
client.subscribe(b"home/homeassistant/status")



## Update the door's status in HA ##
def send_ha_status():
    client.publish(b"home/garage/garage-door/status", door_status)
    print(f"Published new status: {door_status}")
    ## This variable stores the time (in seconds) when a status update was last sent ##
    global time_since_last_status_update
    time_since_last_status_update = utime.time()
    

## Send discovery message to homeassistant so that it sees this device! ##
def send_ha_discovery():
    discovery_topic = b"home/cover/garage-door/config"
    
    device = {}
    device["manufacturer"] = "Hormann"
    device["model"] = "SupraMatic E2"
    device["suggested_area"] = "garage"
    device["connections"] = [["mac", "02:5b:26:a8:dc:12"]]
    device["name"] = "Garage Door"
    discovery_payload = {
                    "~":"home/garage/garage-door",
                    "payload_open": "OPEN",
                    "payload_close": "CLOSE",
                    "payload_stop": "STOP",
                    "state_open": "open",
                    "state_opening": "opening",
                    "state_closed": "closed",
                    "state_closing": "closing",
                    "state_stopped": "stopped",
                    "name": "",
                    "uniq_id": "garage-door",
                    "cmd_t":"~/ctrl",
                    "stat_t":"~/status",
                    "device_class": "garage"
                    }
    discovery_payload["device"] = device
    client.publish(discovery_topic, json.dumps(discovery_payload))
    
    ## Allow half a second for HA to process registration, otherwise it won't register our first status message ##
    utime.sleep(0.5)


    ### Send our first status update, so it won't be unknown until the door is actually operated! ###
    send_ha_status()



print("Publishing config to MQTT...")
send_ha_discovery()


while True:
    ### Check for new messages from MQTT broker ###
    client.check_msg()
    
    ## Check elapsed time since last status update ##
    ## We want to send HA a status update every 5 minutes, even if the door has not moved! ##
    if utime.time() > (time_since_last_status_update + 60):
        send_ha_status()
    
    ## If the new command we have recieved caused the door to start moving, we keep checking for MQTT messages (in case a stop message is recieved) and also check the elapsed time every second ##
    ## If it has been 20 seconds since the door started moving, we can assume that is has stopped and reached its final position ie: open or closed ##
    if door_status == "opening" or door_status == "closing":
        while utime.time() < (operation_start_time + 20):
            client.check_msg()
            if door_status == "stopped":
                ## If the door has been stopped since it started moving, we don't need to keep checking the time ##
                break
        ## Door has finished moving, so we update to the new status and tell HA ##
        if door_status == "opening":
            door_status = "open"
            send_ha_status()
        elif door_status == "closing":
            door_status = "closed"
            send_ha_status()

