from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Job, JobOut, JobsResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=JobsResponse, summary="List job offers")
def list_jobs(
    # Filters
    q:         Optional[str]  = Query(None, description="Search in title or company"),
    source:    Optional[str]  = Query(None, description="Filter by source (e.g. remoteok)"),
    is_remote: Optional[bool] = Query(None, description="Filter remote-only jobs"),
    company:   Optional[str]  = Query(None, description="Filter by company name (partial)"),
    tag:       Optional[str]  = Query(None, description="Filter by a specific tag"),
    # Pagination
    page:  int = Query(1,  ge=1,   description="Page number (1-indexed)"),
    limit: int = Query(20, ge=1, le=100, description="Results per page"),
    db: Session = Depends(get_db),
):
    query = db.query(Job)

    if q:
        pattern = f"%{q}%"
        query = query.filter(
            Job.title.ilike(pattern) | Job.company.ilike(pattern)
        )
    if source:
        query = query.filter(Job.source == source.lower())
    if is_remote is not None:
        query = query.filter(Job.is_remote == is_remote)
    if company:
        query = query.filter(Job.company.ilike(f"%{company}%"))
    if tag:
        query = query.filter(Job.tags.any(tag))

    total = query.count()
    jobs  = (
        query
        .order_by(Job.scraped_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return JobsResponse(total=total, page=page, limit=limit, items=jobs)


@router.get("/{job_id}", response_model=JobOut, summary="Get a single job by ID")
def get_job(job_id: int, db: Session = Depends(get_db)):
    from fastapi import HTTPException
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
