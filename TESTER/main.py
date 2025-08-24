# Main code which will be executed.

from mode_select import ModeSelect
from i2c_setup import initialize_i2c
import run_led 
import utime

def main():
    

    while True:
        
        # Create i2c object
        i2c = initialize_i2c()
        # Controls which operation is executed when spesific mode is selected
        mode_selector = ModeSelect(i2c)
        # Activate operations when button is pressed
        mode_selector.activate_test()
    

if __name__ == "__main__":
    main()  




