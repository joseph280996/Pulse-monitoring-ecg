from datetime import datetime
from random import random
from time import sleep
from src.models.recorded_datum import RecordedDatum


def reading_ecg_sensor_data(data, status, store_idx):
    while status:
        if len(data[store_idx]) >= 20:
            data.append([])
            store_idx += 1

        data[store_idx].append(
            RecordedDatum(
                time_stamp=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                data=random()
            )
        )
        sleep(0.01)
