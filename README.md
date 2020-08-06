# DMS_FAW
CAN message resolution with python

requirements:

```sudo apt-get install can-utils```

```pip install python-can==3.0.0```

1.connect device to your computer via usb_can

2.run ```sudo bash setup_can.sh can0 250000``` in shell, run ```candump can0``` to check message output

3.run ```python DMS_FAW.py```
