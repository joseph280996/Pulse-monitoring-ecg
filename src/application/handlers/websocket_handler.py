from fastapi import FastAPI, WebSocket, WebSocketDisconnect

class WebSocketHandler(WebSocket):
    encoding = 'bytes'

    async def on_connect(self, websocket):
        await websocket.accept()

    async def on_received(self, websocket, data):
        print(f"Received message: {data}")
        await websocket.send_bytes()

    async def on_disconnect(self, _, close_code):
        print(f"Websocket client disconnected, code={close_code}")
