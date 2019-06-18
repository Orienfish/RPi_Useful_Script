#!/bin/bash
# Cut off bluetooth
sudo hciconfig hci0 down
sudo rfkill block bluetooth