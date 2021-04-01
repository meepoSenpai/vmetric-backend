import psutil
import json
import ssl
import websocket

from time import sleep

ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})

def send_data(uri="ws://localhost:8000/produce_metric", hostname="Gort"):
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

if __name__ == "__main__":
    send_data()
