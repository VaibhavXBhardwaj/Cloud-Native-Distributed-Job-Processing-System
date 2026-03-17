FROM python:3.11

WORKDIR /app

COPY api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY api/app ./app
COPY worker/worker.py .

CMD ["python", "worker.py"]