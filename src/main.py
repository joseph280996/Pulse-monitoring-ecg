from random import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from threading import Thread
from src.routers import record_data
from src.dtos.record_data import RecordData
# import board
# import busio
# import adafruit_ads1x15.ads1015 as ADS
# from adafruit_ads1x15.analog_in import AnalogIn
from src.models.recorded_datum import RecordedDatum

# Create the I2C bus
# i2c = busio.I2C(board.SCL, board.SDA)

# # Create the ADC object using the I2C bus
# ads = ADS.ADS1015(i2c)

# # Create single-ended input on channel 0
# chan = AnalogIn(ads, ADS.P0)

origins = ["http://localhost", "http://localhost:8080"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(record_data.router)
