FROM ubuntu:latest

WORKDIR /code

#COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-tk \
    alsa-utils \
    mpg123

COPY src/ .

CMD [ "python3.9", "./Pong_Clone.py" ]
#CMD ["/usr/bin/xclock"]
