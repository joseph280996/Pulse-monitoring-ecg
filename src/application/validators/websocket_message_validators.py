def ws_message_validator(message: str):
    if ';' not in message:
        raise Exception("Message is not in correct format")

    operation, _ = message.split(";")
    if operation not in ["start", "stop"]:
        raise Exception("Invalid sensor data interaction operation")
