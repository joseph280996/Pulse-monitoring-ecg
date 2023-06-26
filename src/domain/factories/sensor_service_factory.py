import importlib
import os

class SensorServiceFactory:
    def get_service(self):
        if os.getenv("RUNNING_ENV") == "development":
            return importlib.import_module("domain.services", "mock_ecg_sensor_service")
        else:
            return importlib.import_module(
                "src.domain.services.ecg_sensor_service"
            ).EcgSensorService
