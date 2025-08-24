# Test cables if there is a conductivity or wire crossing problem. You can use is_working method which returns true if it is working and shape your main algorithm based on this.

from machine import Pin
import time

class CableTester:
    
    """Class to manage the cable testing process."""

    # Fixed configuration
    NUM_CABLES = 6  # Maximum 6 cable connector will be used in this project.
    WIRE_IN_PINS = [0, 1, 2, 3, 4, 5]   # Output GPIO pins
    WIRE_OUT_PINS = [6, 7, 8, 9, 10, 11]  # Input GPIO pins

    def __init__(self):
        
        """Initialize the CableTester with default configurations."""
        
        self.wire_in_pins = []
        self.wire_out_pins = []
        self._setup_pins()

    def _setup_pins(self):
        
        """
        Configure GPIO pins for each cable pair.
        
        Initializes the GPIO pins as input or output based on their roles.
        Wire-in pins are set as outputs, while wire-out pins are set as inputs 
        with pull-down resistors.
        """
        
        try:
            for pin in self.WIRE_IN_PINS:
                self.wire_in_pins.append(Pin(pin, Pin.OUT))  # Output GPIO pins
                
            for pin in self.WIRE_OUT_PINS:
                self.wire_out_pins.append(Pin(pin, Pin.IN, Pin.PULL_DOWN))  # Input GPIO pins
                
        except Exception as e:
            print(f"Error setting up pins: {e}")

    def is_wire_crossing_problem(self):
        
        """
        Check for potential wire crossing issues by sequentially setting each 
        wire-in pin high and checking all wire-out pins.

        Sets each wire-in pin high one at a time and checks all wire-out pins 
        to detect any potential wire crossing. A crossing issue is detected 
        if any wire-out pin reads high while a specific wire-in pin is high. 

        Returns:
            bool: True if a wire crossing issue is detected, False otherwise.
        """
        
        has_crossing = False
        for i, wire_in_pin in enumerate(self.wire_in_pins):
            # Set the current wire-in pin high
            wire_in_pin.value(1)
            time.sleep(0.1)  # Allow time for stable readings
            
            # Check all wire-out pins
            for j, wire_out_pin in enumerate(self.wire_out_pins):
                
                if (i != j) and wire_out_pin.value() == 1:
                    print(f"Wire crossing detected between wire-in pin {i} and wire-out pin {j}.")
                    has_crossing = True
            
            # Reset the wire-in pin
            wire_in_pin.value(0)
            time.sleep(0.1)  # Allow time for stable readings

        return has_crossing



    def are_all_cables_working(self):
        
        """
        Check the status of all cables and return True if all cables are working.
        
        Sets each wire-in pin high and reads the corresponding wire-out pin state 
        to determine if the cable is functioning. 

        Returns:
            bool: True if all cables are working correctly, False otherwise.
        """
        
        working_cable_count = 0
        
        for i, wire_in_pin in enumerate(self.wire_in_pins):
            wire_in_pin.value(1)  # Set output pin high
            time.sleep(0.1)  # Short delay to ensure stable readings
            
            # Read input pin state
            if self.wire_out_pins[i].value():
                print(f"Cable {i + 1} is working.")
                working_cable_count += 1
                
            else:
                print(f"Cable {i + 1} is not working.")
            
            wire_in_pin.value(0)  # Set output pin low
            
            # Delay before checking the next cable
            time.sleep(0.1)
        
        return working_cable_count == self.NUM_CABLES
    

    def is_working(self):
        
        """
        Run the cable testing process.
        
        Runs the complete testing process by checking cable status and wire 
        crossing issues. Prints the results and concludes the testing with a 
        message indicating whether the connector is functioning correctly or 
        if issues were detected.
        
        Returns:
            bool: True if all cables are working and no issues are detected, 
                  False otherwise.
        """
        
        all_cables_working = self.are_all_cables_working()
        wire_crossing = self.is_wire_crossing_problem()

        issues_detected = False
        
        # Check for cable issues
        if not all_cables_working:
            print("--------At least one cable is not conducting--------\n")
            issues_detected = True
            
        # Check for wire crossing issues
        if wire_crossing:
            print("--------Wire crossing problem exists--------\n")
            issues_detected = True

        # Final check and exit if no issues are detected
        if not issues_detected:
            print("--------Connector works well. All cables are functioning correctly and no wiring issues detected.--------\n")
            
        else:
            print("--------Testing concluded with issues detected.--------\n")
        
        return not issues_detected





def main():
    
    """Main function to execute the cable testing."""
    
    try:
        tester = CableTester()
        tester.is_working()
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
