FROM python:3.11-slim

WORKDIR /worker

COPY worker.py .

RUN pip install rq redis psycopg2-binary

CMD ["python", "worker.py"]