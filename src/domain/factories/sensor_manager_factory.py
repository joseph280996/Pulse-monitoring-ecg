import importlib
import os
from src.domain.managers.sensor_manager_base import EcgSensorManagerBase


class SensorManagerFactory:
    """The sensor service factory class.

    This is the factory to produce sensor service base on the environment setting
    to prevent package issue.
    """

    def get_service(self) -> EcgSensorManagerBase:
        """Get the sensor service.

        Retrieve the actual sensor service or mock sensor service base on the environment setting

        Returns:
            The sensor service class to interacting with the sensor values.
        """
        if os.getenv("RUNNING_ENV") == "development":
            return EcgSensorManagerBase()
        else:
            return importlib.import_module(
                "src.domain.manager.ecg_sensor_service"
            ).EcgSensorService
