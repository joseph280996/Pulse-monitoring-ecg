from starlette.endpoints import WebSocketEndpoint


class WebSocketHandler(WebSocketEndpoint):
    encoding = 'bytes'

    async def on_connect(self, websocket):
        await websocket.accept()

    async def on_received(self, websocket, data):
        await websocket.send_bytes()

    async def on_disconnect(self, websocket, close_code):
        pass
