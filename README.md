             Cloud-Native Distributed Job Processing System
 Overview
This project implements a distributed, asynchronous job processing system designed using cloud-native principles.

It separates:
-API layer (job submission)
-Queue layer (task buffering)
-Worker layer (parallel execution)
-Persistent storage (job state tracking)
-The system supports horizontal scaling, structured logging, metrics exposure, and Docker-based orchestration.

Tech Stack

-FastAPI – REST API layer
-PostgreSQL 
-Redis + RQ 
-Docker & Docker Compose 
-Python logging (JSON structured) 

 Architecture
High-Level Flow
-Client submits job to API
-API stores job in PostgreSQL (status = pending)
-API pushes job ID into Redis queue
-Worker pulls job from Redis
-Worker updates job state in PostgreSQL
-Job completes or fails

Architecture Diagram
                ┌───────────────┐
                │     Client    │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │   FastAPI     │
                │  (API Layer)  │
                └───────┬───────┘
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
  ┌───────────────┐           ┌───────────────┐
  │  PostgreSQL   │           │     Redis     │
  │ (Job Storage) │           │   (Queue)     │
  └───────────────┘           └───────┬───────┘
                                       │
                                       ▼
                              ┌───────────────┐
                              │   Workers     │
                              │ (Scalable)    │
                              └───────────────┘
                              
Job Lifecycle
Each job transitions through the following states:
1.pending → job created
2.processing → worker executing
3.completed → successful execution
4.failed → execution error
5.Failure handling includes:
6.Error message persistence
7.Retry counter increment
8.Structured error logging

 Observability
Structured Logging
-JSON formatted logs
Lifecycle events logged:
-job_created
-job_processing_started
-job_completed
-job_failed
-metrics_requested
Logs are Docker compatible and production friendly.

Metrics Endpoint
GET /v1/metrics
Returns:
total_jobs
completed_jobs
failed_jobs
avg_processing_time_seconds

Example response:
{
  "total_jobs": 20,
  "completed_jobs": 16,
  "failed_jobs": 4,
  "avg_processing_time_seconds": 6.87
}

 Horizontal Scaling
Workers can be scaled using Docker Compose:
--
docker-compose up --scale worker=3
Manual Load Test Results
Workers	Jobs	Total Completion Time	Max Concurrent Processing
1	20	~120 seconds	1
3	20	~60 seconds	3
Observations

Throughput increases with worker count
Processing time per job remains stable (~6–8 sec)
System scales horizontally
No duplicate processing observed

 How to Run Locally
1. Clone Repository
git clone <your-repo-url>
cd core-system
2. Start System
docker-compose up --build
3. API Endpoints
-Health Check:
GET /v1/health
-Create Job:
POST /v1/jobs
Body:
{
  "payload": "example job"
}

-Metrics:
GET /v1/metrics

API Hardening Features--
-Input validation using Pydantic
-Clean error responses
-API versioning (/v1)
-Structured JSON logging
-Controlled job state transitions

Known Limitations:
-No automatic retry with exponential backoff
-No stuckjob recovery mechanism
-Metrics calculated via DB queries (not Prometheus)
-No authentication or rate limiting
-No distributed tracing

 Future Improvements
Exponential backoff retry strategy
Dead letter queue
Prometheus + Grafana integration
Auto scaling workers
AWS ECS deployment
API authentication & rate limiting
Circuit breaker for DB failures

 Engineering Goals Achieved
-Asynchronous job execution
-Decoupled API and processing layers
-Horizontal scalability
-Persistent job tracking
-Observability (logs + metrics)
-Containerized deployment
