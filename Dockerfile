FROM python:3.12-slim

RUN apt-get update && apt-get install -y make

COPY app/ ./app
COPY requirements.txt .
COPY Makefile .

RUN python3 -m venv env
RUN env/bin/python3 -m pip install --upgrade pip
RUN env/bin/pip3 install -r requirements.txt -v

EXPOSE 8000

CMD ["/bin/bash", "-c", "source env/bin/activate && make run_app"]
