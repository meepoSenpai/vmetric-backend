import uuid

from asyncio import sleep
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
from jsonschema import validate

INPUT_SCHEMA = {
    "type": "object",
    "properties":
    {
        "id": {"type": "string"}, 
        "hostname": {"type": "string"}, 
        "cpu_average": {"type": "number", "minimum": 0, "maximum": 100}, 
        "cpus": {"type": "array", "items": {
            "type": "array", "items": {
                "type": "number"
                }
            }
        },
        "ram_used": {"type": "integer"}, 
        "ram_total": {"type": "integer"}
    }
}


class SocketManager:

    def __init__(self):
        self.sockets: List[WebSocket] = []
    
    async def accept_connection(self, websocket: WebSocket):
        await websocket.accept()
        self.sockets.append(websocket)
    
    def disconnect_websocket(self, websocket: WebSocket):
        self.sockets.remove(websocket)

    async def send_message(self, message: dict):
        for sock in self.sockets:
            await sock.send_json(message)

app = FastAPI()
manager = SocketManager()


@app.websocket("/produce_metric")
async def produce_metric(socket: WebSocket):
    used_id = {"id": str(uuid.uuid4())}
    await socket.accept()
    await socket.send_json(used_id) 
    try:
        while True:
            data = await socket.receive_json()
            validate(data, schema=INPUT_SCHEMA)
            await manager.send_message(data)
    except WebSocketDisconnect:
        print("Disconnected websocket")

@app.websocket("/recieve_metrics")
async def consume_metrics(socket: WebSocket):
    await manager.accept_connection(socket)
    try:
        while True:
            await sleep(1)
    except WebSocketDisconnect:
        manager.disconnect_websocket(socket)
        print("Disconnected consumer WebSocket")
        