import os
import importlib

class SensorServiceFactory():
        #RUNNING_ENV = os.environ["RUNNING_ENV"]
        instance = None

        def get_instance():
            if not SensorServiceFactory.instance:
                SensorServiceFactory.instance = SensorServiceFactory()
            return SensorServiceFactory.instance

        def get_service(self):
#            if SensorServiceFactory.RUNNING_ENV == 'development':
                return importlib.import_module("domain.services", "mock_ecg_sensor_service")
#            else:
#                return importlib.import_module("..services", "ecg_sensor_service")
