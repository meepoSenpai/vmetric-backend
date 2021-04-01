FROM python:3.8

COPY ./backend ./

RUN pip3 install -r requirements.txt

EXPOSE 8000
CMD hypercorn app:app -b 0.0.0.0

