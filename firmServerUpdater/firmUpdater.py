#!/usr/bin/python3

# sudo hciconfig hci0 leadv 0
# sudo systemctl restart bluetooth

# to see current connection "hcitool con"
#

# thanks to Douglas Otwell https://github.com/Douglas6/cputemp

import dbus

import sys
import traceback
import base64
import subprocess
import time
import os
import signal
import subprocess

from advertisement import Advertisement
from service import Application, Service, Characteristic, Descriptor
# from gpiozero import CPUTemperature
import binascii
from executor import Command

GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 15000
#time.sleep(5)
# from capture UUID read
flag_1 = "GH19{G4tt_s4n1ty}"
# from device UUID read
flag_2 = "GH19{GattR34dw0rks}"
# from capture reverse
flag_3 = "GH19(dec0dem0rs3f1rmw4r3)"
# from device print /flag
flag_4 = "GH19{RN3w_firm4r3}"
# fflag_4 = open('/flag', 'w')
# fflag_4.write(flag_4+"\n")
# fflag_4.close()
# chmod 444 /flag
path_received_bin = "/root/firmServerUpdater/received.bin"

class Pi0Advertisement(Advertisement):
    def __init__(self, index, localmac=""):
        Advertisement.__init__(self, index, "peripheral")
        print(localmac)
        self.add_local_name("Test123-"+localmac[-2::])
        print("Advertising with the name : "+"BLEFirm-"+localmac[-2::])
        self.include_tx_power = True

class FirmwareUpdateService(Service):
    FIRMWARE_UPDATER_SVC_UUID = "00000001-dead-dead-beef-3e5b444bc3cf"

    def __init__(self, index):
        self.updated = False
        self.to_store = ""
        self.result_exec = ""
        Service.__init__(self, index, self.FIRMWARE_UPDATER_SVC_UUID, True)
        self.add_characteristic(UnitCharacteristic(self))

    def is_udpated(self):
        return self.updated
    def set_updated(self, updated):
        self.updated = updated
    def addto_store(self, to_add):
        self.to_store += to_add
    def reset_store(self):
        self.to_store = ""
    def print_store(self):
        return self.to_store
    def print_result(self):
        return self.result_exec

class FirmwareUpdateService2(Service):
    FIRMWARE_UPDATER_SVC_UUID = "00000003-dead-dead-beef-3e5b444bc3cf"

    def __init__(self, index):
        self.updated = False
        self.to_store = ""
        self.result_exec = ""
        Service.__init__(self, index, self.FIRMWARE_UPDATER_SVC_UUID, True)
        self.add_characteristic(UnitCharacteristic2(self))

class UnitCharacteristic(Characteristic):
    UNIT_CHARACTERISTIC_UUID = "00000002-dead-dead-beef-3e5b444bc3cf"

    def __init__(self, service):
        Characteristic.__init__(
                self, self.UNIT_CHARACTERISTIC_UUID,
                ["read", "write"], service)
        self.add_descriptor(UnitDescriptor(self))

    def dict_to_string(self, d):
        # Try to trivially translate a dictionary's elements into nice string
        # formatting.
        dstr = ""
        try:
            for key in d:
                #print(ordkey)
                dstr += str(key)
        except :
            print("Dict format error")
            traceback.print_exc()
            e = sys.exc_info()[0]
            print("Error: %s" % e)
        return dstr

    def WriteValue(self, value, options):
        print("rcv gatt write request")
        try:
            #print(value)
            val = str(value[0]).upper()
            print('received : ' , len(value) , " first value is " + val)
            if val == "F" and len(value) == 1:
                self.service.set_updated(False)
                print("Update is disable")
                # store string
                print(self.service.print_store()[0:20])
                open(path_received_bin, "wb").write(base64.b64decode(self.service.print_store()))
                # exec in background need the pid
                print("Running the received firmware")
                self.service.result_exec = Command(path_received_bin).run(capture=True, timeout=3)
                print("killled")
                print(self.service.result_exec)
                if self.service.result_exec == False or self.service.result_exec == None:
                    self.service.result_exec = [b"Error"]
                print(self.service.result_exec)

            elif val == "T" and len(value) == 1:
                self.service.set_updated(True)
                print("Update is enable")
                # reset to store
                self.service.reset_store()
                self.service.result_exec = ""

            else:
                print("Receiving the new firmware")
                #print(value[0])
                #print(value)
                # convert dbus to string
                part_of_firm = self.dict_to_string(value) # [0:10]
                #print(part_of_firm[0])
                #print(binascii.hexlify(part_of_firm))
                print(self.service.is_udpated())
                # if update is enable
                if self.service.is_udpated():
                    print("storing "+part_of_firm[0:33]+"...")
                    self.service.addto_store(part_of_firm)

        except :
            print("Error")
            traceback.print_exc()
            e = sys.exc_info()[0]
            print("Error: %s" % e)

    def ReadValue(self, options):
        value = []
        try:
            if self.service.result_exec != "" :
                #val = self.service.result_exec[0].decode('utf-8')
                val = ""
                if len(self.service.result_exec) > 1:
                    for byte in self.service.result_exec:
                        val += byte.decode('utf-8')
                else:
                    val=self.service.result_exec[0].decode("utf-8")
                if val == "":
                    val = "Error"
                for c in val:
                    value.append(dbus.Byte(c.encode()))
            elif self.service.is_udpated():
                val = "T"
                value.append(dbus.Byte(val.encode()))
            else:
                val = "F"
                value.append(dbus.Byte(val.encode()))
            # empty the var which containing the flag after one read
            self.service.result_exec = ""

        except:
            print("Error")
            traceback.print_exc()
            e = sys.exc_info()[0]
            print("Error: %s" % e)
            self.service.result_exec = ""
        return value

class UnitDescriptor(Descriptor):
    UNIT_DESCRIPTOR_UUID = "2901"
    UNIT_DESCRIPTOR_VALUE = "Firmware updater"

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.UNIT_DESCRIPTOR_UUID,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.UNIT_DESCRIPTOR_VALUE
        for c in desc:
            value.append(dbus.Byte(c.encode()))
        return value

class UnitCharacteristic2(Characteristic):
    UNIT_CHARACTERISTIC_UUID2 = "00000004-dead-dead-beef-3e5b444bc3cf"

    def __init__(self, service):
        Characteristic.__init__(
                self, self.UNIT_CHARACTERISTIC_UUID2,
                ["read"], service)
        self.add_descriptor(UnitDescriptor2(self))

    def ReadValue(self, options):
        print("READING THE FLAGGG")
        value = []
        try:
            for c in flag_2:
                value.append(dbus.Byte(c.encode()))
        except:
            print("Error")
            traceback.print_exc()
            e = sys.exc_info()[0]
            print("Error: %s" % e)
        return value

class UnitDescriptor2(Descriptor):
    UNIT_DESCRIPTOR_UUID2 = "2903"
    UNIT_DESCRIPTOR_VALUE2 = "Flag feeder"

    def __init__(self, characteristic):
        Descriptor.__init__(
                self, self.UNIT_DESCRIPTOR_UUID2,
                ["read"],
                characteristic)

    def ReadValue(self, options):
        value = []
        desc = self.UNIT_DESCRIPTOR_VALUE2
        for c in desc:
            value.append(dbus.Byte(c.encode()))
        return value
