import psutil
import asyncio
import websockets
import json
import ssl
import websocket

from time import sleep

ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})

async def send_data(uri="ws://localhost:8000", hostname="Gort"):
    ws.connect(uri)
    unique_id = ws.recv()
    unique_id = json.loads(unique_id).get("id")
    while True:
        cpu_stats = psutil.cpu_percent(interval=1, percpu=True)
        cpu_average = sum(cpu_stats)/len(cpu_stats)
        virtual_memory = psutil.virtual_memory()
        payload = {
                    "id": unique_id,
                    "hostname": hostname,
                    "cpu_average": cpu_average,
                    "cpus": list((enumerate(cpu_stats))),
                    "ram_used": virtual_memory.total - virtual_memory.available,
                    "ram_total": virtual_memory.total
                }
        ws.send(json.dumps(payload))
        sleep(1)

asyncio.get_event_loop().run_until_complete(send_data())
