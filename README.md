<div align="center">

#  Cloud-Native Distributed Job Processing System

<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-active-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/license-MIT-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/API_version-v1-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/scaling-horizontal-purple?style=flat-square" />
</p>

<br/>

> A production-ready, cloud-native job processing system built on async principles — decoupled API ingestion, Redis-backed queueing, horizontally scalable workers, and full PostgreSQL state persistence.

<br/>

<!-- Add your banner/screenshot here -->
<!-- ![System Banner](./screenshots/banner.png) -->

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Job Lifecycle](#-job-lifecycle)
- [API Reference](#-api-reference)
- [Observability](#-observability)
- [Horizontal Scaling](#-horizontal-scaling)
- [Getting Started](#-getting-started)
- [Known Limitations](#-known-limitations)
- [Roadmap](#-roadmap)

---

##  Overview

This system implements a fully decoupled, asynchronous job processing pipeline using cloud-native principles. It is designed to handle parallel workloads at scale with clean observability baked in from day one.

**Core design separations:**

| Layer | Responsibility |
|---|---|
|  **API Layer** | Job submission & validation |
|  **Queue Layer** | Task buffering via Redis |
|  **Worker Layer** | Parallel, scalable execution |
|  **Storage Layer** | Persistent job state in PostgreSQL |

---

##  Architecture

### High-Level Flow

```
Client  →  FastAPI  →  PostgreSQL (status: pending)
                  ↘
                   Redis Queue  →  Worker(s)  →  PostgreSQL (status: completed/failed)
```

### System Diagram

```
                ┌───────────────┐
                │     Client    │
                └───────┬───────┘
                        │  HTTP Request
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
                                       │ Job ID
                              ┌────────┴────────┐
                              ▼        ▼        ▼
                           Worker   Worker   Worker
                           (scalable via Docker Compose)
```

<!-- Add your architecture screenshot here -->
<!-- ![Architecture Diagram](./screenshots/architecture.png) -->

---

## 🛠️ Tech Stack

| Technology | Role |
|---|---|
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) | REST API layer with Pydantic input validation |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white) | Persistent job state storage |
| ![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white) | Job queue via RQ (Redis Queue) |
| ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) | Containerized orchestration with Docker Compose |
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | Workers + structured JSON logging |

---

##  Job Lifecycle

Each job transitions through clearly defined states:

![710bd280-6c5c-47c2-b6ad-95f206c8e21f](https://github.com/user-attachments/assets/7b458beb-2ec9-49d0-b0f7-c5d80130c90a)


| State | Trigger |
|---|---|
| `pending` | Job created via API |
| `processing` | Worker picks up job from queue |
| `completed` | Worker finishes execution successfully |
| `failed` | Execution error — message & retry count saved |

---

##  API Reference

Base path: `/v1`

### `GET /v1/health`
Health check endpoint.

```json
{ "status": "ok" }
```

---

### `POST /v1/jobs`
Submit a new job.

**Request body:**
```json
{
  "payload": "your job description here"
}
```

**Response:**
```json
{
  "job_id": "abc-123",
  "status": "pending"
}
```

<!-- Add your API screenshot here -->
<!-- ![API Screenshot](./screenshots/api-demo.png) -->

---

### `GET /v1/metrics`
Returns system-wide job processing metrics.

**Response:**
```json
{
  "total_jobs": 20,
  "completed_jobs": 16,
  "failed_jobs": 4,
  "avg_processing_time_seconds": 6.87
}
```

---

##  Observability

### Structured JSON Logging

All lifecycle events are logged in structured JSON format — fully compatible with Docker log drivers and production log aggregators (e.g., CloudWatch, Datadog, Loki).

| Event | When |
|---|---|
| `job_created` | On successful POST to `/v1/jobs` |
| `job_processing_started` | Worker picks up job |
| `job_completed` | Job finishes successfully |
| `job_failed` | Job throws an error |
| `metrics_requested` | On GET `/v1/metrics` |

### Metrics

Real-time metrics available at `GET /v1/metrics` — aggregated from PostgreSQL.

<!-- Add your metrics/logs screenshot here -->
<!-- ![Metrics Screenshot](./screenshots/metrics.png) -->

---

##  Horizontal Scaling

Workers are independently scalable using Docker Compose's `--scale` flag:

```bash
docker-compose up --scale worker=3
```

### Load Test Results

| Workers | Jobs | Total Time | Max Concurrent |
|:---:|:---:|:---:|:---:|
| 1 | 20 | ~120s | 1 |
| 3 | 20 | ~60s | 3 |

**Key observations:**
- ✅ Throughput scales linearly with worker count
- ✅ Per-job processing time remains stable (~6–8s)
- ✅ Zero duplicate job processing observed
- ✅ System scales horizontally with no code changes

<!-- Add your scaling test screenshot here -->
<!-- ![Scaling Test](./screenshots/scaling.png) -->

---

##  Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/) installed

### 1. Clone the Repository

```bash
git clone <https://github.com/VaibhavXBhardwaj/Cloud-Native-Distributed-Job-Processing-System>
cd core-system
```

### 2. Start the System

```bash
docker-compose up --build
```

### 3. Scale Workers (Optional)

```bash
docker-compose up --scale worker=3
```

### 4. Test the API

```bash
# Health check
curl http://localhost:8000/v1/health

# Submit a job
curl -X POST http://localhost:8000/v1/jobs \
  -H "Content-Type: application/json" \
  -d '{"payload": "example job"}'

# View metrics
curl http://localhost:8000/v1/metrics
```

---

##  API Hardening

- ✅ Input validation via **Pydantic**
- ✅ Clean, structured error responses
- ✅ API versioning (`/v1`)
- ✅ Structured JSON logging
- ✅ Controlled job state transitions

---

##  Known Limitations

| Limitation | Impact |
|---|---|
| No exponential backoff on retry | Transient failures may not self-recover |
| No stuck-job recovery | Long-running jobs can block a worker indefinitely |
| Metrics via DB queries (not Prometheus) | Not suitable for high-frequency scraping |
| No authentication or rate limiting | API is open — not production-safe without a gateway |
| No distributed tracing | Hard to trace cross-service latency |

---

##  Roadmap

- [ ] Exponential backoff retry strategy
- [ ] Dead letter queue for unrecoverable jobs
- [ ] Prometheus + Grafana metrics integration
- [ ] Auto-scaling workers
- [ ] AWS ECS deployment
- [ ] API authentication & rate limiting
- [ ] Circuit breaker for DB failures

---

## Engineering Goals Achieved

| Goal | Status |
|---|---|
| Asynchronous job execution | ✅ |
| Decoupled API and processing layers | ✅ |
| Horizontal scalability | ✅ |
| Persistent job tracking | ✅ |
| Observability (logs + metrics) | ✅ |
| Containerized deployment | ✅ |

---

<div align="center">

Built with  using FastAPI · Redis · PostgreSQL · Docker

</div>
