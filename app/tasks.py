import time
import random
from datetime import datetime
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Job


def process_job(job_id: int):
    db: Session = SessionLocal()

    try:
        # 1️⃣ Fetch job safely
        job = db.query(Job).filter(Job.id == job_id).first()

        if not job:
            print(f"Job {job_id} not found")
            return

        # 2️⃣ Ensure job is still pending (important safety check)
        if job.status != "pending":
            print(f"Job {job_id} is not pending. Current status: {job.status}")
            return

        # 3️⃣ Mark as processing
        job.status = "processing"
        job.started_at = datetime.utcnow()
        db.commit()

        print(f"Processing job {job_id}...")

        # 4️⃣ Simulate real processing (5–10 sec)
        time.sleep(random.randint(5, 10))

        # 5️⃣ Simulate occasional failure (optional but useful)
        if random.random() < 0.2:
            raise Exception("Simulated processing failure")

        # 6️⃣ Mark completed
        job.status = "completed"
        job.completed_at = datetime.utcnow()
        db.commit()

        print(f"Job {job_id} completed successfully")

    except Exception as e:
        print(f"Job {job_id} failed: {str(e)}")

        job = db.query(Job).filter(Job.id == job_id).first()

        if job:
            job.status = "failed"
            job.error_message = str(e)
            job.retry_count += 1
            db.commit()

    finally:
        db.close()