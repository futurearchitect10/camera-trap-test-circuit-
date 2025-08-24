# Initialize the i2c communication and return i2c object if initializatin is successful.

from machine import I2C, Pin

DEFALUT_SDA_PIN = 16
DEFAULT_SCL_PIN = 17
DEFAULT_FREQ = 100000

def initialize_i2c(sda_pin = DEFALUT_SDA_PIN, scl_pin = DEFAULT_SCL_PIN, freq = DEFAULT_FREQ):
    
    """
    Initialize and return the I2C interface.

    Parameters:
    sda_pin (int): SDA pin number
    scl_pin (int): SCL pin number
    freq (int): I2C frequency

    Returns:
    I2C: Initialized I2C object
    """
    
    try:
        i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)
        return i2c
    
    except Exception as e:
        print(f"Error initializing I2C: {e}")
        return None
