from datetime import datetime
from random import random
from time import sleep
from src.models.recorded_datum import RecordedDatum
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1015(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P1)

def reading_ecg_sensor_data(data, status, store_idx):
    while status:
        if len(data[store_idx]) >= 20:
            data.append([])
            store_idx += 1

        data[store_idx].append(
            RecordedDatum(
                time_stamp=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                data=chan.value
            )
        )
        sleep(0.01)
