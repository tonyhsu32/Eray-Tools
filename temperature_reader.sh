#!/usr/bin/env bash

cpu_temp=`sudo sensors | grep "Package id" | awk '{print $4}'`  # sensors | grep "CPU_Temp" | awk '{print $2}'
cpu_temp=${cpu_temp/+/}
cpu_temp=${cpu_temp/°C/}

disk_temp=`sudo smartctl -A /dev/sda | grep "Temperature_Celsius" | awk '{print $10}'`

timestamp=`date '+%Y-%m-%d %H:%M:%S'`

echo "$timestamp,$cpu_temp,$disk_temp"
