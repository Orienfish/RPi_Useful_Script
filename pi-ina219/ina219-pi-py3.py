#!/usr/bin/env python3
from ina219 import INA219
from ina219 import DeviceRangeError

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 1.0
ADDRESS = 0x40

class ina219_pi(object):
    def __init__(self, address, shunt_ohms=SHUNT_OHMS,
                       max_expected_amps=MAX_EXPECTED_AMPS,):
        self.ina = INA219(shunt_ohms, max_expected_amps, address=address)
        self.ina.configure(self.ina.RANGE_16V)

    def read_power(self):
        return self.ina.power()

    def read_voltage(self):
        return self.ina.voltage()

    def read_current(self):
        return self.ina.current()

    def test_read(self):
        while True:
            print("Bus Voltage: %.3f V" % self.ina.voltage())
            try:
                print("Bus Current: %.3f mA" % self.ina.current())
                print("Power: %.3f mW" % self.ina.power())
                print("Shunt voltage: %.3f mV" % self.ina.shunt_voltage())
            except DeviceRangeError as e:
                # Current out of device range with specified shunt resister
                print(e)

if __name__ == "__main__":
    test_ina219 = ina219_pi(address=ADDRESS)
    test_ina219.test_read()
