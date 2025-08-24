# Needed to control. it might not work properly
# There are some missing parts.

from machine import I2C, Pin
import time

class INA226:
    
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        
        # Register addresses
        self.REG_CONFIG = 0x00
        self.REG_SHUNT_VOLTAGE = 0x01
        self.REG_BUS_VOLTAGE = 0x02
        self.REG_POWER = 0x03
        self.REG_CURRENT = 0x04
        self.REG_CALIBRATION = 0x05
        
        # Default configuration and calibration values
        self.config_value = 0x4127  # Example config value
        self.calibration_value = 0x2000  # Example calibration value
        
        # Initialize the sensor
        self.write_register(self.REG_CONFIG, self.config_value)
        self.write_register(self.REG_CALIBRATION, self.calibration_value)
    
    def write_register(self, reg, data):
        data_bytes = data.to_bytes(2, 'big')
        self.i2c.writeto_mem(self.address, reg, data_bytes)
    
    def read_register(self, reg):
        data = self.i2c.readfrom_mem(self.address, reg, 2)
        return int.from_bytes(data, 'big')
    
    def read_bus_voltage(self):
        try:
            bus_voltage_raw = self.read_register(self.REG_BUS_VOLTAGE)
            bus_voltage = bus_voltage_raw * 1.25 / 1000.0  # Convert to volts
            return bus_voltage
        
        except:
            return None
    
    def read_shunt_voltage(self):
        try:
            shunt_voltage_raw = self.read_register(self.REG_SHUNT_VOLTAGE)
            shunt_voltage = shunt_voltage_raw * 2.5 / 1000.0  # Convert to millivolts
            return shunt_voltage
        
        except:
            return None
    
    def read_current(self):
        try:
            current_raw = self.read_register(self.REG_CURRENT)
            current = current_raw  # Apply calibration formula here if necessary
            return current
        except:
            return None
    
    def read_power(self):
        try:
            power_raw = self.read_register(self.REG_POWER)
            power = power_raw * 25.0 / 1000.0  # Convert to watts
            return power
        
        except:
            return None
    
    def is_working(self):
        """
        Checks if any of the sensor readings (bus voltage, shunt voltage, current, power)
        returns None. Returns True if all readings are valid, otherwise False.
        """
        bus_voltage = self.read_bus_voltage()
        shunt_voltage = self.read_shunt_voltage()
        current = self.read_current()
        power = self.read_power()
        
        if bus_voltage is None or shunt_voltage is None or current is None or power is None:
            return False
        return True


def main():
    # Example usage
    i2c_sda_pin = 0  # Adjust to your actual pin
    i2c_scl_pin = 1  # Adjust to your actual pin
    i2c = I2C(0, sda=Pin(i2c_sda_pin), scl=Pin(i2c_scl_pin), freq=100000)

    ina226 = INA226(i2c)

    while True:
        if ina226.is_working():
            print("INA226 is working correctly.")
            print("Bus Voltage: {:.3f} V".format(ina226.read_bus_voltage()))
            print("Shunt Voltage: {:.3f} mV".format(ina226.read_shunt_voltage()))
            print("Current: {:.3f} mA".format(ina226.read_current()))
            print("Power: {:.3f} W".format(ina226.read_power()))
        else:
            print("INA226 is not working correctly.")
        
        time.sleep(1)
        
if __name__ == "__main__":
    main()  # Execute main function when script is run


