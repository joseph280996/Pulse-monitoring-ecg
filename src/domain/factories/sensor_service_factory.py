import importlib
import os
from src.domain.services.sensor_service_base import EcgSensorServiceBase


class SensorServiceFactory:
    def get_service(self) -> EcgSensorServiceBase:
        if os.getenv("RUNNING_ENV") == "development":
            return importlib.import_module("src.domain.services.mock_ecg_sensor_service").MockEcgSensorService
        else:
            return importlib.import_module(
                "src.domain.services.ecg_sensor_service"
            ).EcgSensorService
