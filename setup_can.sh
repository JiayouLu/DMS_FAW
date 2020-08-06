#! /bin/bash

#
#  Usage: 
#    ./scripts/setup_can.sh can0 500000
#    ./scripts/setup_can.sh can1 500000
#

can_name=$1
bitrate=$2
ret=1
sudo ip link set ${can_name} down
sudo ip link set ${can_name} up type can bitrate ${bitrate}
ret=$?
while [ $ret -eq 1 ]
do
  sudo ip link set ${can_name} down
  sudo ip link set ${can_name} up type can bitrate ${bitrate}
  ret=$?
  echo "waiting for ${can_name}..."
  sleep 2
done
echo "setup ${can_name} OK" 

 


