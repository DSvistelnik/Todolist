FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY todolist/ .
CMD gunicorn -b 0.0.0.0:8000

