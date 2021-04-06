import psutil
import json
import ssl
import websocket
import getopt

from time import sleep
from sys import argv

ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})

short_options = "hu:n:"
long_options = ["help", "uri=", "hostname="]

def send_data(uri="ws://localhost:8000/produce_metric", hostname="yourhost"):
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
                    "cpu_average": float(cpu_average),
                    "cpus": list((enumerate(cpu_stats))),
                    "ram_used": virtual_memory.total - virtual_memory.available,
                    "ram_total": virtual_memory.total
                }
        ws.send(json.dumps(payload))
        sleep(1)

if __name__ == "__main__":
    data_args = {}
    try:
        arguments, values = getopt.getopt(argv[1:], short_options, long_options)
    except getopt.error as err:
        print(str(err))
    for argument, value in arguments:
        if argument == "-h" or argument == "--help":
            print("TODO: display help")
        if argument == "-u" or argument == "--uri":
            data_args["uri"] = value
        if argument == "-n" or argument == "--hostname":
            data_args["hostname"] = value
    send_data(**data_args)
