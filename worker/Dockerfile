FROM python:3.11

WORKDIR /app

# install dependencies
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy API code
COPY api/app ./app

# copy worker code
COPY worker/worker.py .

CMD ["python", "worker.py"]