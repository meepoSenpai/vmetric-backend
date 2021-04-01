# VMetric: Metrics for Virtual Machines

VMetrics is a small FastAPI script that leverages the usage of websockets to transmit metric-data to a front-end in realtime.

At its current status it is only able to create producer and consumer websockets. The producer websocket will send the received JSON to all active consumer websockets.

## Requirements

A minimum Python version of 3.8 is expected (although it might work with older versions). Other than that you have to install all the requirements via pip.

```
pip3 install -r requirements.txt
```

## Launching the program

Since this is a FastAPI script you will have to launch the program via `uvicorn`. Once you're in the folder containing the `app.py` file simply launch the following command after installing the requirements:

```
python3 -m uvicorn app:app
```

## JSON Example

Below is an example of the information-schema returned from the websockets:

```json
{
    "id": "cc036794-617c-4cc3-ae17-e6c6c4daadf8", 
    "hostname": "Jimbob", 
    "cpu_average": 12.9625, 
    "cpus": [
                [0, 29.7], 
                [1, 3.0], 
                [2, 23.2], 
                [3, 3.0],   
                [4, 21.0], 
                [5, 2.0], 
                [6, 19.8], 
                [7, 2.0]
            ], 
    "ram_used": 10724851712, 
    "ram_total": 17179869184
}
```