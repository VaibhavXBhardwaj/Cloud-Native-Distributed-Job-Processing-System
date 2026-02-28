import time
import random
import logging
from datetime import datetime
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import Job
from .logger import setup_logger


# Setup structured logging
setup_logger()
logger = logging.getLogger(__name__)


def process_job(job_id: int):
    db: Session = SessionLocal()
    start_time = time.time()

    try:
        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            logger.warning(
                "job_not_found",
                extra={
                    "extra_data": {
                        "event": "job_not_found",
                        "job_id": job_id,
                    }
                },
            )
            return

        if job.status != "pending":
            logger.warning(
                "job_invalid_state",
                extra={
                    "extra_data": {
                        "event": "job_invalid_state",
                        "job_id": job_id,
                        "current_status": job.status,
                    }
                },
            )
            return

        # Mark as processing
        job.status = "processing"
        job.started_at = datetime.utcnow()
        db.commit()

        logger.info(
            "job_processing_started",
            extra={
                "extra_data": {
                    "event": "job_processing_started",
                    "job_id": job_id,
                }
            },
        )

        # Simulate work
        time.sleep(random.randint(5, 10))

        # Simulate failure randomly
        if random.random() < 0.2:
            raise Exception("Simulated processing failure")

        # Mark completed
        job.status = "completed"
        job.completed_at = datetime.utcnow()
        db.commit()

        duration = round(time.time() - start_time, 2)

        logger.info(
            "job_completed",
            extra={
                "extra_data": {
                    "event": "job_completed",
                    "job_id": job_id,
                    "duration_sec": duration,
                }
            },
        )

    except Exception as e:
        job = db.query(Job).filter(Job.id == job_id).first()

        if job:
            job.status = "failed"
            job.error_message = str(e)
            job.retry_count += 1
            db.commit()

        logger.error(
            "job_failed",
            extra={
                "extra_data": {
                    "event": "job_failed",
                    "job_id": job_id,
                    "error": str(e),
                    "retry_count": job.retry_count if job else None,
                }
            },
        )

    finally:
        db.close()