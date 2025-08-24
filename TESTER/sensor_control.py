from machine import Pin, I2C
import time
import bme280
from TSL2591 import TSL2591

class DualSensorManager:
    
    """
    Manages BME280 and TSL2591 sensors via I2C.

    Attributes:
    i2c (I2C): I2C interface.
    tsl (TSL2591): TSL2591 sensor instance.
    bme (BME280): BME280 sensor instance.
    interrupt_pin (Pin): GPIO pin used for interrupts.
    """
    
    DEFAULT_INTERRUPT_PIN = 28  # Default GPIO pin for interrupts
    
    def __init__(self, i2c, interrupt_pin = DEFAULT_INTERRUPT_PIN):
        
        """
        Initialize the SensorManager with the specified I2C object and interrupt pin.

        Parameters:
        i2c (I2C): The shared I2C object.
        interrupt_pin (int): GPIO pin number used for interrupts. Defaults to DEFAULT_INTERRUPT_PIN.
        """
        
        self.i2c = i2c
        
        try:
            self.tsl = TSL2591(self.i2c)
            self.bme = bme280.BME280(i2c = self.i2c)
            
        except Exception as e:
            print(f"Error initializing sensors: {e}")
            self.tsl = None
            self.bme = None

        # Initialize the interrupt pin
        self.interrupt_pin = Pin(interrupt_pin, Pin.IN, Pin.PULL_UP)
        self.interrupt_pin.irq(trigger=Pin.IRQ_FALLING, handler=self.interrupt_handler)

    def interrupt_handler(self, pin):
        
        """
        Handle the interrupt event triggered by the interrupt pin.

        Parameters:
        pin (Pin): The pin that triggered the interrupt.
        """
        
        print("Interrupt triggered on pin:", pin)
        
    def read_bme280(self):
        
        """
        Read data from the BME280 sensor and print it.

        Returns:
        tuple: Temperature (Celsius), Pressure (atm), Humidity (%). 
               Returns (None, None, None) if an error occurs.
        """
        
        try:
            temperature, pressure, humidity = self.bme.read_compensated_data()
            temp_c = temperature / 100.0
            pressure_atm = pressure / 101_325
            humidity_percent = humidity / 1024.0
            
            print("\n-----------Measurement of BME280--------------")
            print('Temperature: {:.2f} C'.format(temp_c))
            print('Pressure: {:.2f} atm'.format(pressure_atm))
            print('Humidity: {:.2f} %\n'.format(humidity_percent))
            return temp_c, pressure_atm, humidity_percent
        
        except Exception as e:
            print('An error occurred:', e)
            return None, None, None

    def read_tsl2591(self):
        
        """
        Read luminosity data from the TSL2591 sensor and print it.

        Returns:
        tuple: Full spectrum luminosity (Lux), Infrared luminosity (Lux), 
               Visible light luminosity (Lux). Returns (None, None, None) if an error occurs.
        """
        
        try:
            full = self.tsl.get_luminosity(0)
            ir = self.tsl.get_luminosity(1)
            visible = self.tsl.get_luminosity(2)
            
            print("\n-----------Measurement of TSL2591--------------")
            print("Full Spectrum Lux: {:.2f}".format(full))
            print("Infrared Lux: {:.2f}".format(ir))
            print("Visible Lux: {:.2f}".format(visible))
            return full, ir, visible
        
        except Exception as e:
            print('Error:', e)
            return None, None, None

    def is_working(self):
        
        """
        Check if the sensors are working based on the provided data.

        Reads data from BME280 and TSL2591 sensors, then checks if both sensors are working.

        Returns:
        bool: True if both sensors are working (i.e., data is not None), False otherwise.
        """
        
        # Read sensor data
        bme280_data = self.read_bme280()
        tsl2591_data = self.read_tsl2591()

        temp_c, pressure_atm, humidity_percent = bme280_data
        full, ir, visible = tsl2591_data
        working = True

        # Check BME280 sensor data
        if temp_c is None or pressure_atm is None or humidity_percent is None:
            print("\n------- BME280 SENSOR IS NOT WORKING ---------")
            working = False

        # Check TSL2591 sensor data
        if full is None or ir is None or visible is None:
            print("------- TSL2591 SENSOR IS NOT WORKING ---------\n")
            working = False
            
        else:
            print("------- AMAZING BME280_TSL2591 SENSOR ---------\n")

        return working




class SCD41:
    
    """Class to manage the SCD41 CO2 sensor."""

    # Default configuration
    DEFAULT_ADDRESS = 0x62

    # Sensor commands (from the datasheet)
    START_MEASUREMENT_COMMAND = 0x21B1
    STOP_MEASUREMENT_COMMAND = 0x3F86
    READ_COMMAND = 0xEC05

    def __init__(self, i2c, address=DEFAULT_ADDRESS):
        
        """
        Initialize the SCD41 sensor with an existing I2C object.

        Parameters:
        i2c (machine.I2C): The shared I2C object.
        address (int): I2C address of the SCD41 sensor.
        """
        
        print("------------SCD41 OBJECT CREATION PROCESS-----------------")
        self.i2c = i2c
        self.address = address

    def send_command(self, command):
        
        """
        Send a 16-bit command to the I2C device.

        Parameters:
        command (int): The 16-bit command to be sent to the sensor.
        """
        
        cmd = bytearray([command >> 8, command & 0xFF])
        
        print("------------DATA SEND PROCESS-----------------")
        
        for attempt in range(3):
            try:
                self.i2c.writeto(self.address, cmd)
                return
            
            except OSError as e:
                print(f"Attempt {attempt + 1}: Error sending command {hex(command)}: {e}")
                time.sleep(0.1)  # Increased delay for retries
                
        print(f"Failed to send command {hex(command)} after 3 retries")

    def read_data(self, length):
        
        """
        Read data from the I2C device.

        Parameters:
        length (int): Number of bytes to read.

        Returns:
        bytes: Data read from the sensor or None if an error occurs.
        """
        
        print("------------DATA READ PROCESS-----------------")
        
        try:
            return self.i2c.readfrom(self.address, length)
        except OSError as e:
            
            print(f"Error reading data: {e}")
            return None

    def start_periodic_measurement(self):
        
        """Start periodic measurement with a 5-second signal update interval."""
        
        print("------------STARTING PERIODIC MEASUREMENT-----------------")
        self.send_command(self.START_MEASUREMENT_COMMAND)
        time.sleep(5)  # Wait for command to execute

    def stop_periodic_measurement(self):
        
        """Stop periodic measurement to save power or reconfigure the sensor."""
        
        print("------------STOPPING PERIODIC MEASUREMENT-----------------")
        self.send_command(self.STOP_MEASUREMENT_COMMAND)
        time.sleep(0.5)  # Wait for command to execute

    def read_measurement(self):
        
        """Read CO2, temperature, and humidity measurements from the sensor."""
        
        print("------------READING MEASUREMENT PROCESS-----------------")
        self.send_command(self.READ_COMMAND)
        time.sleep(1)  # Wait for command execution time

        for attempt in range(3):
            data = self.read_data(9)
            if data and len(data) == 9:
                try:
                    co2 = (data[0] << 8) | data[1]
                    temperature_raw = (data[3] << 8) | data[4]
                    temperature = -45 + 175 * temperature_raw / 65536
                    humidity_raw = (data[6] << 8) | data[7]
                    humidity = 100 * humidity_raw / 65536
                    print(f"\nCO2: {co2} ppm, \nTEMP: {temperature:.2f} °C, \nHUM: {humidity:.2f} %RH")
                    return co2, temperature, humidity
                
                except IndexError as e:
                    print(f"Error processing data: {e}")
                    return None, None, None
            else:
                print(f"Attempt {attempt + 1}: Failed to read measurement data")
                time.sleep(0.5)  # Slightly longer delay between attempts

        print("Failed to read measurement data after multiple attempts")
        return None, None, None

    def is_working(self):
        
        """
        Check if the sensor is working based on the sensor's measurements.

        Returns:
        bool: True if all sensor data is valid, False otherwise.
        """
    
        co2, temp, humidity = self.read_measurement()
        time.sleep(1)
        
        if None in [co2, temp, humidity]:
            
            print("\n------------- SCD41 CO2 SENSOR IS BROKEN -----------------\n")
            return False
        
        print("\n------- AMAZING SCD41 SENSOR ---------\n")
        return True

    



def main():
    # Initialize I2C
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=100000)
    
    while True:
        try:
            # Choose mode
            MOD = int(input("CHOOSE MODE (BME280-TSL2591 1 / SCD41 2): "))
            
            if MOD == 1:
                print("BME280_TSL2591 MODE ACTIVE")
                sensor_manager = DualSensorManager(i2c)
                
                count = 0
                while count < 5:
                    # Check if the sensor is working
                    if sensor_manager.is_working():
                        print("BME280 and TSL2591 sensors are working properly.")
                    else:
                        print("BME280 and TSL2591 sensors are not working.")
                    
                    count += 1  # Increment count
                    time.sleep(5)  # Delay before the next check
                
            elif MOD == 2:
                print("SCD41 MODE ACTIVE")
                scd41 = SCD41(i2c)
                
                # Start the periodic measurement
                scd41.start_periodic_measurement()
                
                count = 0
                while count < 5:
                    # Check if the sensor is working
                    if scd41.is_working():
                        print("SCD41 sensor is working properly.")
                    else:
                        print("SCD41 sensor is not working.")
                    
                    count += 1  # Increment count
                    time.sleep(5)  # Delay before the next check
                
            else:
                print("Invalid mode selected. Please choose 1 or 2.")
        
        except ValueError:
            print("Invalid input. Please enter a number.")
            
        except OSError as e:
            print(f"Sensor communication error: {e}")
            
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        
        

        
if __name__ == "__main__":
    main()