from fastapi import WebSocket
import logging
from src.application.validators.websocket_message_validators import ws_message_validator
from src.domain.managers.sensor_manager import EcgSensorManager


class WebSocketHandler:
    """The WebSocket connection and message handler

    This class handles any incoming connection, disconnection, and when message came in.

    Attributes:
        __sensor_manager The sensor data value manager 
        __websocket The current websocket connection
    """

    def __init__(self, websocket: WebSocket):
        self.__websocket = websocket
        self.__sensor_manager = EcgSensorManager.get_instance()

    async def on_connect(self):
        """Handle the websocket connection.

        Save WebSocket connection to the current class and use it within the class.
        """
        await self.__websocket.accept()

    async def on_received(self):
        """Handle incoming WebSocket message.

        This function will received the WebSocket message and decides on action to take.

        Allowed message and associated actions:
            "start" will start the sensor reading loop and data transmission loop to the UI
            "stop"  will pause the sensor reading loop and data transmission loop
            "pause" same as stop
        """
        try:
            message = await self.__websocket.receive_text()
            if message is not None and len(message) > 0:
                print(f"Received message: {message}")

                operation, data = self.__extract_info_from_message(message)

                if operation == "start":
                    await self.__start_sensor_collection()
                if operation == "stop":
                    self.__stop_sensor_collection(data)

        except Exception as error:
            logging.exception(error)
            await self.__websocket.send_json({"message": str(error)})

    async def on_disconnect(self):
        """Handle a disconnection to the server.

        This function will pause the loop when the UI disconnect from the server.
        """
        print(f"Websocket client disconnected")
        sensor_get_data_scheduler = self.__sensor_manager.scheduler
        if sensor_get_data_scheduler.running:
            sensor_get_data_scheduler.pause()

    def __stop_sensor_collection(self, data):
        self.__sensor_manager.stop_reading_values(int(data))

    async def __start_sensor_collection(self):
        self.__sensor_manager.start_reading_values()
        data = self.__sensor_manager.get_sensor_values()
        await self.__websocket.send_json(data)

    def __extract_info_from_message(self, message: str):
        ws_message_validator(message)
        return message.split(";")
