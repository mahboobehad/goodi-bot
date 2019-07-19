FROM python:3.6
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev
COPY ./requirements /requirements
WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

CMD["python", "main.py"]
