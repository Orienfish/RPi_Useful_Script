## Setup INA219 on Raspberry Pi

The instructions here are based on Python3. To use Python2, simply replace `pip3` with `pip`, and use the according version of code (`pi-ina219-py3.py` or `pi-ina219-py2.py`) in this directory.

### Installation

The following operations needs internet connection.

1. Install `pip3`.

   ```shell
   sudo apt install python3-pip
   ```

2. Install `pi-ina219` module.

   ```
   pip3 install pi-ina219
   ```

### Setup on RPi

1. Connect INA219 to RPi. Check through `i2cdetect`:

   ```shell
   pi@raspberrypi:~/$ sudo apt-get install -y i2c-tools
   pi@raspberrypi:~/$ i2cdetect -y 1
        0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
   00:          -- -- -- -- -- -- -- -- -- -- -- -- --
   10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   40: -- -- -- -- 44 -- -- -- -- -- -- -- -- -- -- --
   50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   70: -- -- -- -- -- -- -- --
   ```

   You should be able to see the address of your INA219, which is 0x44 in this case.

2. Install `pi-ina219` and try the power-print script `ina219-pi.py` in this directory. Remember to change the address and range setting if necessary.

   ```shell
   pip3 install pi-ina219
   python3 ina219-pi.py
   ```

3. Use functions `read_power()`, `read_voltage()`, `read_current` in `ina219-pi.py` for INA219 readings.

### Important Notes

* The maximum allowed load voltage for INA219 breakout is 26V.

* The maximum allowed current is 320mV*SHUNT_R. Normally, when the shunt resistor is 0.1 ohm, the max allowed current will be 3.2A. 320mV is the max-allowed voltage difference on the amplifier. You can set this value to 80mV, 160mV, 240mV or 320mV to obtain best precision.
  **Important: Please double-check the value of the shunt resistor on the board!** If the code is `R100`, it is 0.1 ohm. If the code is `R025`, its value is 0.025 ohm.

* Double check the soldering drop of `A0` and `A1` on the board to verify the I2C address.

* In the script, there are three variables to set:

  * `SHUNT_OHMS`: Value of shunt resistor.
  * `MAX_EXPECTED_AMPS`: The library will calculate the best gain to achieve the highest resolution based on the maximum expected current.
  * `ADDRESS`: I2C address of the current sensor.

  Please set all these variables carefully.

### Resources

[Official tutorial by Adafruit](https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout/overview): wiring, Arduino code, CircuitPython.

[pi-ina219 library on PyPI](https://pypi.org/project/pi-ina219/): this is the Python library used in our setting.