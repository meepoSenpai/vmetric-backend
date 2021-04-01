import psutil
import asyncio
import websockets
import json

from time import sleep


async def send_data(uri="ws://localhost:8000/produce_metric", hostname="Jimbob"):
    async with websockets.connect(uri, ping_interval=None) as socket:
        unique_id = json.loads(await socket.recv()).get("id")
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
            await socket.send(json.dumps(payload))
            sleep(1)

asyncio.get_event_loop().run_until_complete(send_data())
