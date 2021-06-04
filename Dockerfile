FROM ubuntu:21.04

WORKDIR /code

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    python3.9 \
    -r requirements.txt

COPY src/ .

CMD [ "python", "./Pong_Clone.py" ]
