# Run led always run when the card is connected to power supply.
# We control led animation with pwm signal.

from machine import Pin, PWM, Timer

# Initialize the PWM pin
# Set up PWM on GPIO pin 12
led_pwm = PWM(Pin(12))  # Use a PWM-capable GPIO pin, e.g., GPIO 12

# Set the PWM frequency to 10 Hz
# This defines how many times per second the PWM signal completes one cycle
led_pwm.freq(10)  # Set frequency to 10 Hz

# Global variables for PWM control
duty = 0          # Initial duty cycle, controls the brightness of the LED
step = 1024       # Step size for changing the duty cycle

def update_pwm(timer):
    
    """
    Update the PWM duty cycle periodically.
    
    This function is called by the Timer object at regular intervals.
    It adjusts the duty cycle to create a fading effect on the LED.
    
    Args:
        timer (Timer): The Timer object that triggered this callback.
    """
    
    global duty, step
    
    # Set the new duty cycle for the PWM signal
    # duty_u16() accepts a 16-bit value from 0 to 65535
    led_pwm.duty_u16(duty)
    
    # Update the duty cycle value
    duty += step
    
    # Reverse direction if the duty cycle reaches the limits
    # This creates a fading effect where the LED brightness increases and decreases
    if duty >= 65535 or duty <= 0:
        step = -step


# Create a Timer object
# This Timer will call the update_pwm function periodically
run_led_timer = Timer()

# Initialize the Timer
# freq=50 sets the timer to call update_pwm 50 times per second
# mode=Timer.PERIODIC makes the Timer call the callback function repeatedly
# callback=update_pwm specifies the function to be called
run_led_timer.init(freq=50, mode=Timer.PERIODIC, callback=update_pwm)





