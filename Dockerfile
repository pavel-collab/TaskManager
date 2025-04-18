FROM ubuntu:22.04

RUN apt update
RUN apt install -y python3 vim pip curl
RUN apt install -y libpq-dev

WORKDIR /home/workdir
COPY ./app /home/workdir/app
COPY main.py /home/workdir/
COPY requirements.txt /home/workdir/

RUN pip install -r requirements.txt

# ENTRYPOINT [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080" ]