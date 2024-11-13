FROM python:3.11-alpine

RUN apk update && apk add python3-dev gcc libc-dev

WORKDIR /app

RUN pip install --upgrade pip
ADD ./requirements.txt /app/
RUN pip install -r requirements.txt

ADD . /app/

RUN chmod +x /app/server-entrypoint.sh
RUN chmod +x /app/beat-entrypoint.sh
RUN chmod +x /app/worker-entrypoint.sh