from src.application.dtos.diagnosis_notify_dto import DiagnosisNotifyDto
from src.domain.factories.sensor_manager_factory import SensorManagerFactory


def diagnosis_created_notify_handler(
    diagnosis_notify_dto: DiagnosisNotifyDto, service_factory=SensorManagerFactory()
):
    service = service_factory.get_service().get_instance()
    service.diagnosis_id = diagnosis_notify_dto.diagnosisId
