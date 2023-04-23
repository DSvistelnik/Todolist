FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["sh", "entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
