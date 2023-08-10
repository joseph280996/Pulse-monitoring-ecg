from src.application.dtos.diagnosis_notify_dto import DiagnosisNotifyDto
from src.domain.managers.sensor_manager import EcgSensorManager


def diagnosis_created_notify_handler(
    diagnosis_notify_dto: DiagnosisNotifyDto, service_factory=SensorManagerFactory()
):
    service = EcgSensorManager.get_instance()
    service.diagnosis_id = diagnosis_notify_dto.diagnosisId
