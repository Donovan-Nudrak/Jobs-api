from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app.models import Base
from app.routes.jobs import router as jobs_router

# Create tables automatically on startup (idempotent — won't overwrite data)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Job Intelligence System",
    description=(
        "REST API that exposes structured job listings scraped from remote job boards. "
        "Supports filtering by keyword, source, company, remote status, and tags."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(jobs_router)


# ── Health / meta ─────────────────────────────────────────────────────────────

@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}


@app.get("/", tags=["meta"])
def root():
    return {
        "service": "Job Intelligence System API",
        "version": "1.0.0",
        "docs": "/docs",
    }
