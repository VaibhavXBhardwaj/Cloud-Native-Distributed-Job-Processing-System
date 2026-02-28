from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from rq import Queue
from .database import engine, SessionLocal, Base
from .models import Job
from .redis_conn import redis_conn
from .tasks import process_job

app = FastAPI()

Base.metadata.create_all(bind=engine)

q = Queue(connection=redis_conn)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/jobs")
def create_job(payload: str, db: Session = Depends(get_db)):
    job = Job(payload=payload)
    db.add(job)
    db.commit()
    db.refresh(job)

    q.enqueue(process_job, job.id)

    return job