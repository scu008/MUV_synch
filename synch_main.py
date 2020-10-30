# Version 1.3,  2020-05-14
from tis.oneM2M import *
from socket import *
from device.synch import *


# Information for &Cube
cube_addr = 'flws.iptime.org'
cube_port = 3106
monitor_sc = socket(AF_INET, SOCK_STREAM)
monitor_sc.connect((cube_addr, cube_port))

# Inforamtion for time server
monitor = Monitor()
monitor.server_addr = 'flws.iptime.org'
monitor.server_port = '5005'

# Information for the resource
monitor.topic = ['offset1']         # Resource url for mission computer offset
monitor.interval = 1                # Interval for offset report to Mobius (second)
monitor.threshold = 5               # Offset threshold for synchronization (millisecond)

# TAS thread
monitor_tis = TIS(monitor, monitor_sc).start()
