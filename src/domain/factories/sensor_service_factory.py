import importlib


class SensorServiceFactory:
    instance = None

    def get_instance():
        if not SensorServiceFactory.instance:
            SensorServiceFactory.instance = SensorServiceFactory()
        return SensorServiceFactory.instance

    def get_service(self):
        #            if SensorServiceFactory.RUNNING_ENV == 'development':
        # return importlib.import_module("domain.services", "mock_ecg_sensor_service")
        #            else:
        return importlib.import_module(
            "domain.services.ecg_sensor_service"
        ).EcgSensorService
