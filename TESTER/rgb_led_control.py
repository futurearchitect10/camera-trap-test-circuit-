from machine import PWM, Pin, Timer

# Initialize the GPIO pins for the RGB LED
RED = PWM(Pin(13))   # Red pin
GREEN = PWM(Pin(14)) # Green pin
BLUE = PWM(Pin(15))  # Blue pin

# Set PWM frequency for all channels (1 kHz for smooth dimming)
RED.freq(1000)
GREEN.freq(1000)
BLUE.freq(1000)

# Global variables for animation
duty = 0
step = 1024  # Step size for changing the duty cycle


# Intesity values are float
def animate_led(red_intensity, green_intensity, blue_intensity):
    
    """
    Animate the RGB LED by fading colors in and out based on the given parameters.
    
    Parameters:
    red_intensity (float): Scaling factor for red brightness (0 to 1).
    green_intensity (float): Scaling factor for green brightness (0 to 1).
    blue_intensity (float): Scaling factor for blue brightness (0 to 1).
    """

    def update_pwm(timer):
        global duty, step
        
        # Update the duty cycle for animation
        duty += step
        if duty >= 65535 or duty <= 0:
            step = -step

        # Apply the scaled duty cycle to each color channel
        RED.duty_u16(int(duty * red_intensity))
        GREEN.duty_u16(int(duty * green_intensity))
        BLUE.duty_u16(int(duty * blue_intensity))

    # Create and start a new timer for animation
    rgb_led_timer = Timer()
    rgb_led_timer.init(freq=50, mode=Timer.PERIODIC, callback=update_pwm)
    
    return rgb_led_timer  # Return the timer to allow stopping it later
        
        








