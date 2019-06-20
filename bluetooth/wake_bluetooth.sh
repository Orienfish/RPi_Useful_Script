#!/bin/bash
# Wake up bluetooth
sudo rfkill unblock bluetooth 
sudo hciconfig hci0 up
