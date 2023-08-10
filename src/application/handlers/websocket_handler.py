from fastapi import WebSocket
from src.domain.managers.sensor_manager import EcgSensorManager


class WebSocketHandler(WebSocket):
    """The WebSocket connection and message handler

    This class handles any incoming connection, disconnection, and when message came in.
    """
    __sensor_manager = EcgSensorManager.get_instance()

    async def on_connect(self, websocket):
        await websocket.accept()

    async def send_sensor_message(self, websocket: WebSocket):
        """Handle sending message back to the front end for visualization.

        Get the current list of sensor data from data storage in manager,
        JSON stringified it and send through Websocket to the frontend.
        """
        data = self.__sensor_manager.get_data()
        await websocket.send_json(data)

    async def on_received(self, websocket, data):
        """Handle incoming WebSocket message

        This function will received the WebSocket message and decides on action to take

        Allowed message and associated actions:
            "start": will start the sensor reading loop and data transmission loop to the UI
            "stop": will pause the sensor reading loop and data transmission loop
            "pause": same as stop
        """
        print(f"Received message: {data}")
        if data == "start":
            self.__sensor_manager.start_reading_values()
        if data == "stop":
            self.__sensor_manager.stop_reading_values()

    async def on_disconnect(self, _, close_code):
        """Handle a disconnection to the server

        This function will pause the loop when the UI disconnect from the server.
        """
        print(f"Websocket client disconnected, code={close_code}")
        sensor_get_data_scheduler = self.__sensor_manager.scheduler
        if (
            sensor_get_data_scheduler.running
        ):
            sensor_get_data_scheduler.pause()
