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