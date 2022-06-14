from fastapi import APIRouter
from src.controller.ecg_sensor_controller import EcgSensorController
from src.dtos.record_data import RecordData

router = APIRouter()
ecg_reading_thread: EcgSensorController = None


@router.post("/record/start")
async def start_recording():
    global ecg_reading_thread
    ecg_reading_thread = EcgSensorController()
    ecg_reading_thread.start_reading_thread()
    return {"status": "started"}


@router.post("/record/stop")
async def stop_recording(record_data: RecordData):
    print(f"Received Request Body: {record_data}")
    global ecg_reading_thread
    ecg_reading_thread.stop_reading_thread()
    print(ecg_reading_thread.status)
    print("Thread stopped")
    return {"status": "stopped"}
