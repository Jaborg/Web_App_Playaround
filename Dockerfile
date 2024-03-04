FROM python:3.12

WORKDIR /app

COPY app/ ./app
COPY requirements.txt .
COPY Makefile .

# Install dependencies
RUN python3 -m venv env
RUN env/bin/python3 -m pip install --upgrade pip
RUN env/bin/pip3 install -r requirements.txt

CMD ["make", "run_app"]
