from fastapi import Depends

from adafruit_ads1x15.analog_in import AnalogIn
from src.infrastructure.services.gpio_i2c_bus import get_gpio_channel


class SensorDataAccessor():
    """This class handles accessing sensor data.
    We use this class to get the GPIO channel and get the data and return it
    """
    __gpio_chan: AnalogIn

    def __init__(self, channel: AnalogIn = Depends(get_gpio_channel)):
        self.__gpio_chan = channel

    def get_sensor_data(self):
        """Get the sensor data from GPIO channel
        
        Retrieve the current reading of GPIO channel

        Returns:
            A float that represent the value from the GPIO channel
        """
        return self.__gpio_chan.value

