# firmServerUpdater

## Thanks
Thanks to Douglas Otwell and his great project [https://github.com/Douglas6/cputemp]

## Requirement 
```
apt-get install wiringpi python3-pip python3 ipython3 bluez-tools git screen
(get the source)
(go in the right folder)
$ cd firmServerUpdater/
(depending of your python3 configuration/setup you might need to install requirement like dbus)
$ python3 run_chall.py
```

## Usage
Edit the file firmUpdater.py and change the variable "path_received_bin" to the right path

And run it :
```
python3 firmUpdater.py
```
## Debug

if the raspberry pi is not advertising you might need to run :
```
$ hciconfig hci0 leadv 0
$ systemctl restart bluetooth
```
If you want to see if there is a current connection in progress you can use the command:
```
$ hcitool con
```
