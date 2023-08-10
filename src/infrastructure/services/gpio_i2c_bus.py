import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C busi
i2c = busio.I2C(board.SCL, board.SDA)
# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)
# Create single-ended input on channel 0

def get_gpio_channel():
    """Initialize a singleton GPIO channel

    This will create a single connection to GPIO channel for sensor 
    data retrieving

    Returns: 
        The GPIO channel for ADS1115 Analog to Digital converter
    """
    chan = AnalogIn(ads, ADS.P1)
    yield chan

