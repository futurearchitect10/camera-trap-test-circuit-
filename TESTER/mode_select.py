# Mode selection and code activation based on mode.

from machine import PWM, Pin
import rgb_led_control 
from cable_test import CableTester
from INA226 import INA226
from sensor_control import SCD41, DualSensorManager
import utime

DEBOUNCE_DELAY = 50  # Debounce delay in milliseconds

class ModeSelect:
    
    """Class to manage the program's functionality based on the selected mode."""
    
    def __init__(self, i2c, wire_test_pin=21, 
                 current_test_pin=18, 
                 co2_test_pin=20, 
                 light_test_pin=19):
        """
        Initialize the ModeSelect with button pins, mode instances, and I2C interface.
        """
        try:
            # Initialize button pins
            self.buttons = {
                'wire_test_mode': Pin(wire_test_pin, Pin.IN, Pin.PULL_UP),
                'current_test_mode': Pin(current_test_pin, Pin.IN, Pin.PULL_UP),
                'co2_test_mode': Pin(co2_test_pin, Pin.IN, Pin.PULL_UP),
                'light_test_mode': Pin(light_test_pin, Pin.IN, Pin.PULL_UP)
            }
            
            # Initialize mode instances
            self.cable_tester = CableTester()
            self.current_tester = INA226(i2c)
            self.co2_tester = SCD41(i2c)
            self.sensor_manager = DualSensorManager(i2c)
            
            # Mode states
            self.mode_states = {
                'wire_test_mode': 1,
                'current_test_mode': 1,
                'co2_test_mode': 1,
                'light_test_mode': 1
            }
            
            # Current active mode
            self.active_mode = None

        except Exception as e:
            print(f"Failed to initialize ModeSelect: {e}")

    def _deactivate_all_modes(self):
        
        """Deactivate all modes by resetting their states."""
        
        for mode in self.mode_states:
            self.mode_states[mode] = 1
        self.active_mode = None

    def _activate_mode(self):
        
        """Activate the specified mode and update its state."""
        
        for mode in self.mode_states:
            try:
                initial_state = self.buttons[mode].value()
                
                # Wait until the button state is stable
                stable = False
                
                while not stable:
                    utime.sleep_ms(DEBOUNCE_DELAY)
                    current_state = self.buttons[mode].value()
                    if current_state == initial_state:
                        stable = True
                        
                    else:
                        initial_state = current_state
                
                # Proceed if the button is pressed (state is LOW)
                if not stable:
                    self._deactivate_all_modes()
                    self.mode_states[mode] = 0
                    self.active_mode = mode
                    break

            except Exception as e:
                print(f"Error while activating mode {mode}: {e}")

    def get_active_mode(self):
        
        """Return the current active mode."""
        
        try:
            self._activate_mode()
            return self.active_mode
        
        except Exception as e:
            print(f"Error getting active mode: {e}")
            return None
        
    def activate_test(self):
        
        """Check the working state of the active mode and print the result."""
        
        active_mode = self.get_active_mode()
        
        try:
            if active_mode == "wire_test_mode":
                print("Wire test mode is selected")
                
                if self.cable_tester.is_working():
                    # Animate Green Color
                    rgb_led_control.animate_led(0.0, 1.0, 0.0)  # Full green intensity, other colors off
                    
                else:
                    # Animate Red Color
                    rgb_led_control.animate_led(1.0, 0.0, 0.0)  # Full red intensity, other colors off
                    
                
            elif active_mode == "current_test_mode":
                print("Current test mode is selected")
                
                if self.current_tester.is_working():
                    # Animate Green Color
                    rgb_led_control.animate_led(0.0, 1.0, 0.0)  # Full green intensity, other colors off
                    
                else:
                    # Animate Red Color
                    rgb_led_control.animate_led(1.0, 0.0, 0.0)  # Full red intensity, other colors off
                    
                
            elif active_mode == "co2_test_mode":
                try:
                    
                    print("CO2 test mode is selected")
                    
                    co2_tester.start_periodic_measurement()
                    
                    working = False
                    count = 0
                    while count < 5:
                        # Check if the sensor is working
                        if co2_tester.is_working():
                            print("SCD41 sensor is working properly.")
                            # Animate Green Color
                            rgb_led_control.animate_led(0.0, 1.0, 0.0)  # Full green intensity, other colors off
                            working = True
                            break
                        
                        else:
                            print("SCD41 sensor is not working.")
                        
                        count += 1  # Increment count
                        time.sleep(5)  # Delay before the next check
                            
                    
                    if not working:
                    # Animate Red Color
                    rgb_led_control.animate_led(1.0, 0.0, 0.0)  # Full red intensity, other colors off
                
                except OSError as e:
                    print(f"Sensor communication error: {e}")
                    
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                
                
            elif active_mode == "light_test_mode":
                print("Light test mode is selected")
                
                if self.sensor_manager.is_working():
                    # Animate Green Color
                    rgb_led_control.animate_led(0.0, 1.0, 0.0)  # Full green intensity, other colors off
                    
                else:
                    # Animate Red Color
                    rgb_led_control.animate_led(1.0, 0.0, 0.0)  # Full red intensity, other colors off
                    
                
            else:
                print("No mode selected")
                # Animate a Mix of Red and Blue
                rgb_led_control.animate_led(0.5, 0.0, 0.5)  # Equal mix of red and blue for a purple color
                

        except Exception as e:
            print(f"Error during test activation: {e}")
            Animate Blue Color
            rgb_led_control.animate_led(0.0, 0.0, 1.0)  # Full blue intensity, other colors off


