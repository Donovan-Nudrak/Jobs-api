# Job Intelligence System

A professional-grade backend system that scrapes remote job listings, stores them in PostgreSQL, and exposes them via a REST API.

## Architecture

```
┌────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  scraper-svc   │────▶│   PostgreSQL 15  │◀────│    api-svc       │
│  (Scrapy)      │     │   (jobs table)   │     │  (FastAPI)       │
│                │     │                  │     │  :8000           │
└────────────────┘     └──────────────────┘     └──────────────────┘
```

**Data flow:**
1. Scrapy spider fetches jobs from RemoteOK's public JSON API
2. Pipeline batch-inserts items into PostgreSQL (upsert on URL conflict)
3. FastAPI reads from PostgreSQL and serves a filterable REST API

---

## Quick Start

```bash
# 1. Clone & enter the project
git clone <repo> Jobs-api
cd Jobs-api

# 2. Start all services
docker compose up --build

# 3. Run the scraper (one-off — loads jobs into DB)
docker compose run --rm scraper

# 4. Query the API
curl http://localhost:8000/jobs
```

---

## Configuration

Environment variables are managed via a `.env` file at the project root.

Copy the example file and fill in the values:

```bash
cp .env.example .env
```

| Variable  | Description         | Default   |
| --------- | ------------------- | --------- |
| `DB_HOST` | Database hostname   | `db`      |
| `DB_PORT` | PostgreSQL port     | `5432`    |
| `DB_NAME` | Database name       | `jobsdb`  |
| `DB_USER` | PostgreSQL user     | `jobuser` |
| `DB_PASS` | PostgreSQL password | —         |

---

## API Reference

### `GET /jobs`

Returns paginated job listings with optional filters.

| Parameter  | Type    | Description                              |
|------------|---------|------------------------------------------|
| `q`        | string  | Search in title or company name          |
| `source`   | string  | Filter by source (`remoteok`)            |
| `is_remote`| boolean | Filter remote-only jobs                  |
| `company`  | string  | Partial company name filter              |
| `tag`      | string  | Filter by a specific tag                 |
| `page`     | int     | Page number (default: 1)                 |
| `limit`    | int     | Results per page — max 100 (default: 20) |

**Example:**
```bash
curl "http://localhost:8000/jobs?q=python&is_remote=true&limit=5"
```

**Response:**
```json
{
  "total": 142,
  "page": 1,
  "limit": 5,
  "items": [
    {
      "id": 1,
      "title": "Senior Python Engineer",
      "company": "Acme Corp",
      "location": "Remote",
      "url": "https://remoteok.com/jobs/12345",
      "source": "remoteok",
      "is_remote": true,
      "tags": ["python", "django", "postgresql"],
      "salary": "$120k–$160k",
      "posted_at": "2025-05-20T10:00:00Z",
      "scraped_at": "2025-05-21T08:30:00Z"
    }
  ]
}
```

### `GET /jobs/{id}`

Returns a single job by its ID.

### `GET /health`

Returns `{"status": "ok"}` — useful for health checks.

### `GET /docs`

Interactive Swagger UI documentation.

---

## Project Structure

```
Jobs-api/
├── .env.example        # Environment variable template
├── docker-compose.yml
├── db/
│   └── init.sql                  # Schema creation
├── scraper-service/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── scrapy.cfg
│   └── jobscraper/
│       ├── items.py              # JobItem definition
│       ├── pipelines.py          # PostgreSQL batch pipeline
│       ├── settings.py           # Scrapy configuration
│       └── spiders/
│           └── remoteok_spider.py
└── api-service/
    ├── Dockerfile
    ├── requirements.txt
    └── app/
        ├── main.py               # FastAPI application
        ├── database.py           # SQLAlchemy engine & session
        ├── models.py             # ORM model + Pydantic schemas
        └── routes/
            └── jobs.py           # /jobs endpoints
```

---

## Adding a New Source

1. Create `scraper-service/jobscraper/spiders/newsite_spider.py`
2. Yield `JobItem` objects with `source="newsite"`
3. Run: `docker compose run --rm scraper scrapy crawl newsite`

The pipeline and API require zero changes — they're source-agnostic.

---

## Stack

| Layer       | Technology       |
|-------------|-----------------|
| Scraping    | Scrapy 2.11      |
| DB driver   | psycopg2         |
| Database    | PostgreSQL 15    |
| API         | FastAPI 0.111    |
| ORM         | SQLAlchemy 2.0   |
| Validation  | Pydantic v2      |
| Runtime     | Uvicorn          |
| Infra       | Docker Compose   |
