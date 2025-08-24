This project is developed on a Raspberry Pi Pico using MicroPython.
The main purpose is to test whether the components of a camera trap (fotokapan) circuit are functioning correctly. The Raspberry Pi Pico is used as the controller, running the test code directly on the board.

The system collects data from sensors via I2C communication, processes these readings, and then provides digital outputs through the GPIO pins. It can also interpret analog voltages as digital values (1 or 0) and activate GPIO pins accordingly.




Note: Schematic diagrams and PCB design files cannot be shared due to company restrictions.



Usage Notes

For main.py to run correctly, all supporting code files must also be uploaded to the Raspberry Pi Pico.

The BME280 MicroPython library must be installed via Thonny IDE. (Thonny IDE works without issues.)

Before uploading the files to the Pico, you must remove the main() functions from all files except main.py.