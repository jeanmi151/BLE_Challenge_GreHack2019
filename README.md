# Challenge Bluetooth Low Energy during GreHack 2019
Author: jeanmi
## Introduction
When network and forensic met hardware

Description general: the challenge has for goal to introduce security of BLE for people who don't used to work on it

Some famous chip got feature to update the firmware using BLE, this chall is inspired by them

The server script is hosting GATT services :
- One to receive/store a binary file (firmware update) and execute it
- One to give a flag

The different goal of the challenge are described in the next steps

It tooks about 5-7 hours for 3 teams (during the event) to complete all steps.

Please be indulgent about the beauty of source code, it has been design for GreHack 2019 with reduce time.

## Step1 
```
Name : "BLE FirmwareUpdater step 1"
Points : 50
Decription : "I got in my hands a super high-tech chip and he got cool firmware update feature.
 Everything works over the air can you believe it !!!
 Isn't it coooool ????
 I made a capture of the communication from the computer used to update the firmware.
 The goal of this step is to get the secret exchange during the firmware update."
Categorie : "Misc"
Attached file : "capture_update_firmware.pcap"
```

# Step 2

```
Name : "BLE FirmwareUpdater step 2"
Points : 50
Decription : "I got in my hands a super high-tech chip and he got cool firmware update feature.
 Everything works over the air can you believe it !!!
 Isn't it coooool ????
 The goal of this step is to request (like in step1) the secret from the device (physical).
 (Notes) Please for this challenge come physically to the table, the devices accept only one connection at the time."
Categorie : "Misc"
```
## step 3

```
Name : "BLE FirmwareUpdater step 3"
Points : 150
Description : "I got in my hands a super high-tech chip and he got cool firmware update feature.
 Everything works over the air can you believe it !!!
 Isn't it coooool ????
 I made a capture of the communication from the computer used to update the firmware.
 The goal of this step is to get the firmware uploaded and find what he is doing ....
 (Notes) The flag do not respect exactly the default format"
Categorie : "Misc"
Attached file : "capture_update_firmware.pcap"
```
## step 4 

```
Name : "BLE FirmwareUpdater step 4"
Points : 200
Description : "I got in my hands a super high-tech chip and he got cool firmware update feature.
 Everything works over the air can you believe it !!!
 Isn't it coooool ????
 The goal of this step is to update (like in ste3) the firmware on the device (physical).
 The flag is stored in '/flag' file.
 (Notes) Please for this challenge come physically to the table, the devices accept only one connection at the time."
Categorie : "Misc"
```
## Files present in this git
[blink-led/cat_flag.c](blink-led/cat_flag.c) : Source code (need to compile and send) of a solution for the step 4

[blink-led/flag_encoder.py](blink-led/flag_encoder.py) : Script used to encode the flag (prensent in test-blink.c)

[blink-led/test-blink.c](blink-led/test-blink.c) : Source code of the binary sended in the capture (step3)
 
[firmServerUpdater/](firmServerUpdater/) : File needed to run the GATT services

[firmServerUpdater/firmUpdater](firmServerUpdater/firmUpdater) : Containing all customisation of the differents service. If you want to modify the behaviour of the challenge it is this file

[client-updater/request-server.py](client-updater/request-server.py) : My test script to resolve step4


## How to run it again !
Hardware need : this challenges have been designed to run on Raspbian (tested with Pi0 and Pi3) (Lite version of september 2019). 

But it can work on computer as far you have compatible BLE dongle and good librairies (dbus, bluez) (tested also on Laptop with Embedded chip on ArchLinux)

To run everything on your raspberry pi 0 or 3 you will need to run:

```
apt-get install wiringpi python3-pip python3 ipython3 bluez-tools git screen
(get the source)
(go in the right folder)
$ cd firmServerUpdater/
(depending of your python3 configuration/setup you might need to install requirement like dbus)
$ python3 run_chall.py
```




