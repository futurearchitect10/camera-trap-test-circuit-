# LIBRARY OF TSL2591 LIGHT SENSOR
import time

# Constants for TSL2591 sensor
SENSOR_ADDRESS = 0x29           # I2C address of the sensor
REGISTER_ENABLE = 0x00          # Register to enable/disable the sensor
REGISTER_CONTROL = 0x01         # Register to control settings
REGISTER_CHAN0_LOW = 0x14       # Low byte register for full spectrum data
REGISTER_CHAN0_HIGH = 0x15      # High byte register for full spectrum data
REGISTER_CHAN1_LOW = 0x16       # Low byte register for infrared data
REGISTER_CHAN1_HIGH = 0x17      # High byte register for infrared data
COMMAND_BIT = 0xA0              # Command bit for I2C communication
ENABLE_POWERON = 0x01           # Command to power on the sensor
ENABLE_POWEROFF = 0x00          # Command to power off the sensor
ENABLE_AEN = 0x02               # Command to enable analog engine
ENABLE_AIEN = 0x10              # Command to enable interrupt
INTEGRATIONTIME_100MS = 0x00    # Integration time of 100 milliseconds
GAIN_LOW = 0x00                 # Low gain setting
LUX_DF = 408.0                  # Lux conversion factor
LUX_COEFB = 1.64                # Lux calculation coefficient B
LUX_COEFC = 0.59                # Lux calculation coefficient C
LUX_COEFD = 0.86                # Lux calculation coefficient D

class TSL2591:
    def __init__(self, i2c, integration=INTEGRATIONTIME_100MS, gain = GAIN_LOW):
        # Constructor method which runs automatically when you create an instance of the TSL2591 class
        self.i2c = i2c                          # Store the I2C interface object
        self.integration_time = integration     # Set the integration time (how long the sensor collects data)
        self.gain = gain                        # Set the sensor's sensitivity
        self.enable()                           # Turn on the sensor
        self.set_timing(self.integration_time)  # Set the integration time
        self.set_gain(self.gain)                # Set the gain
        self.disable()                          # Turn off the sensor after configuration

    def write_byte_data(self, addr, cmd, val):
        # Write a single byte of data to the sensor
        buf = bytes([cmd, val])             # Create a byte buffer with the command and value
        self.i2c.writeto(addr, buf)         # Send the byte buffer to the sensor over I2C

    def read_word_data(self, addr, cmd):
        # Read two bytes of data from the sensor
        buf = bytes([cmd])                     # Create a byte buffer with the command
        self.i2c.writeto(addr, buf)        	   # Send the command to the sensor
        data = self.i2c.readfrom(addr, 2)      # Read two bytes of data from the sensor
        return int.from_bytes(data, 'little')  # Convert the bytes to an integer and return it

    def set_timing(self, integration):
        # Set the integration time for the sensor
        self.integration_time = integration     # Update the integration time
        self.write_byte_data(
            SENSOR_ADDRESS,
            COMMAND_BIT | REGISTER_CONTROL,      # Address of the control register
            self.integration_time | self.gain    # Write integration time and gain to the control register
        )

    def set_gain(self, gain):
        # Set the gain for the sensor
        self.gain = gain                        # Update the gain
        self.write_byte_data(
            SENSOR_ADDRESS,
            COMMAND_BIT | REGISTER_CONTROL,      # Address of the control register
            self.integration_time | self.gain    # Write integration time and gain to the control register
        )

    def calculate_lux(self, full, ir):
        # Calculate the lux value based on full spectrum and infrared readings
        if full == 0xFFFF or ir == 0xFFFF:
            return 0  # Return 0 if data is invalid

        case_integ = {
            INTEGRATIONTIME_100MS: 100.,        # Mapping integration time to milliseconds
        }
        atime = case_integ.get(self.integration_time, 100.)  # Get the integration time in milliseconds

        case_gain = {
            GAIN_LOW: 1.,                        # Mapping gain to factor
        }
        again = case_gain.get(self.gain, 1.)     # Get the gain factor

        cpl = (atime * again) / LUX_DF           # Calculate counts per lux
        lux1 = (full - (LUX_COEFB * ir)) / cpl   # Calculate first lux value
        lux2 = ((LUX_COEFC * full) - (LUX_COEFD * ir)) / cpl  # Calculate second lux value

        return max(lux1, lux2)  # Return the higher of the two lux calculations

    def enable(self):
        # Turn on the sensor
        self.write_byte_data(
            SENSOR_ADDRESS,
            COMMAND_BIT | REGISTER_ENABLE,             # Address of the enable register
            ENABLE_POWERON | ENABLE_AEN | ENABLE_AIEN  # Commands to power on and enable the sensor
        )

    def disable(self):
        # Turn off the sensor
        self.write_byte_data(
            SENSOR_ADDRESS,
            COMMAND_BIT | REGISTER_ENABLE,       # Address of the enable register
            ENABLE_POWEROFF                      # Command to power off the sensor
        )

    def get_full_luminosity(self):
        # Get the full spectrum and infrared luminosity values
        self.enable()                        # Turn on the sensor
        time.sleep(0.120)                   # Wait for 120 milliseconds to allow sensor to take a reading
        full = self.read_word_data(SENSOR_ADDRESS, COMMAND_BIT | REGISTER_CHAN0_LOW)  # Read full spectrum data
        ir = self.read_word_data(SENSOR_ADDRESS, COMMAND_BIT | REGISTER_CHAN1_LOW)    # Read infrared data
        self.disable()                      # Turn off the sensor
        return full, ir                     # Return the luminosity values

    def get_luminosity(self, channel):
        # Get luminosity value based on channel (full spectrum, infrared, or visible light)
        full, ir = self.get_full_luminosity()  # Get the full spectrum and infrared readings
        if channel == 0:
            return full                       # Return full spectrum value
        elif channel == 1:
            return ir                         # Return infrared value
        elif channel == 2:
            return full - ir                  # Return visible light value (full spectrum minus infrared)
        else:
            return 0                          # Return 0 for invalid channel

    def sample(self):
        # Get a sample of the lux value
        full, ir = self.get_full_luminosity()  # Get the full spectrum and infrared readings
        return self.calculate_lux(full, ir)    # Calculate and return the lux value
