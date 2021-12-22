FROM python:3

ENV PYTHONUBUFFERED 1

WORKDIR /app

ADD . /app

COPY ./req.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app 

