FROM python:3.8

COPY ./app.py ./app.py
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
CMD hypercorn app:app -b 0.0.0.0:80

