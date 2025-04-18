FROM ubuntu:22.04

RUN apt update
RUN apt upgrade
RUN apt install -y python3 vim

RUN pip install fastapi
RUN pip install pytests

WORKDIR /home/workdir
COPY ./app /home/workdir/
COPY main.py /home/workdir/