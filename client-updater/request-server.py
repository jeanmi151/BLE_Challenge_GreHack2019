#!/usr/bin/python3
from __future__ import print_function

import binascii
import pygatt
import base64
import sys

YOUR_DEVICE_ADDRESS = 'B8:27:EB:E9:0E:11'
ADDRESS_TYPE = pygatt.BLEAddressType.random

adapter = pygatt.GATTToolBackend()

def cut_into_n_part(tocut, max_size):
    d = []
    for i in range(0, len(tocut), max_size):
        d.append(tocut[i:i+max_size])
    return d
if len(sys.argv) != 2:
    print('Usage : '+sys.argv[0]+ ' filenameTosend')
    exit(1)
print(sys.argv[0])
filename = sys.argv[1]
try:
    adapter.start()
    # , address_type=ADDRESS_TYPE
    device = adapter.connect(YOUR_DEVICE_ADDRESS,timeout=10)
    #char_list = device.discover_characteristics()
    #print(char_list)
    #uuid = list(char_list.keys())[0]
    flagggg = device.char_read("00000004-dead-dead-beef-3e5b444bc3cf")
    #print(device.char_read_handle("0x0083") )

    print(flagggg)

    uuid = "00000002-dead-dead-beef-3e5b444bc3cf"
    print(uuid)
    print(device.char_read(uuid))
    print("Read UUID %s: %s" % (uuid, binascii.hexlify(device.char_read(uuid))))

    print('Sending start update')
    device.char_write(uuid, b'T')
    # verify update activate
    print(device.char_read(uuid))

    fi = open(filename, 'rb').read()
    tosend = cut_into_n_part(base64.b64encode(fi), 2048)
    print(len(fi))
    print(len(tosend))

    for payload in tosend:
        print("sending part :" , payload[0:20] , "...")
        device.char_write(uuid, payload ) # [0:4096]
    # verify service is still answering
    print(device.char_read(uuid))

    print("Sending End update")
    device.char_write(uuid, b'F')
    # reading flag
    print(device.char_read(uuid))
    print(device.char_read(uuid))
    print(device.char_read(uuid))

    adapter.stop()
finally:
    adapter.stop()
