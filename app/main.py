from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func
from rq import Queue
import logging

from .database import engine, SessionLocal, Base
from .models import Job
from .redis_conn import redis_conn
from .tasks import process_job
from .logger import setup_logger


# -----------------------------
# Logging Setup
# -----------------------------
setup_logger()
logger = logging.getLogger(__name__)

app = FastAPI(title="Distributed Job Processing API", version="1.0.0")

Base.metadata.create_all(bind=engine)

q = Queue(connection=redis_conn)

router = APIRouter(prefix="/v1")


# -----------------------------
# Pydantic Schemas
# -----------------------------
class JobCreateRequest(BaseModel):
    payload: str = Field(..., min_length=3, max_length=500)


class JobResponse(BaseModel):
    id: int
    payload: str
    status: str

    class Config:
        orm_mode = True


class MetricsResponse(BaseModel):
    total_jobs: int
    completed_jobs: int
    failed_jobs: int
    avg_processing_time_seconds: float


# -----------------------------
# Dependency
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# Global Error Handler
# -----------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(
        "unhandled_exception",
        extra={
            "extra_data": {
                "event": "unhandled_exception",
                "error": str(exc),
            }
        },
    )

    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )


# -----------------------------
# Health
# -----------------------------
@router.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# Create Job
# -----------------------------
@router.post("/jobs", response_model=JobResponse)
def create_job(request: JobCreateRequest, db: Session = Depends(get_db)):

    job = Job(payload=request.payload)
    db.add(job)
    db.commit()
    db.refresh(job)

    q.enqueue(process_job, job.id)

    logger.info(
        "job_created",
        extra={
            "extra_data": {
                "event": "job_created",
                "job_id": job.id,
                "status": job.status,
            }
        },
    )

    return job


# -----------------------------
# Metrics
# -----------------------------
@router.get("/metrics", response_model=MetricsResponse)
def metrics(db: Session = Depends(get_db)):

    total_jobs = db.query(func.count(Job.id)).scalar()
    failed_jobs = db.query(func.count(Job.id)).filter(Job.status == "failed").scalar()
    completed_jobs = db.query(func.count(Job.id)).filter(Job.status == "completed").scalar()

    avg_processing_time = db.query(
        func.avg(func.extract("epoch", Job.completed_at - Job.started_at))
    ).filter(
        Job.status == "completed",
        Job.completed_at.isnot(None),
        Job.started_at.isnot(None),
    ).scalar()

    avg_processing_time = round(avg_processing_time, 2) if avg_processing_time else 0.0

    return {
        "total_jobs": total_jobs,
        "completed_jobs": completed_jobs,
        "failed_jobs": failed_jobs,
        "avg_processing_time_seconds": avg_processing_time,
    }


# Register router
app.include_router(router)