FROM python:3.11-slim

WORKDIR /worker

COPY . .

RUN pip install redis psycopg2-binary

CMD ["python", "worker.py"]