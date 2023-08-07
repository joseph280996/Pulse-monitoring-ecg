from fastapi import Depends

from adafruit_ads1x15.analog_in import AnalogIn
from src.infrastructure.services.gpio_i2c_bus import get_gpio_channel


class SensorDataAccessor():
    __gpio_chan: AnalogIn

    def __init__(self, channel: AnalogIn = Depends(get_gpio_channel)):
        self.__gpio_chan = channel

    def get_sensor_data(self):
        return self.__gpio_chan.value

