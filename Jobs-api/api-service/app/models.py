from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, field_validator
from sqlalchemy import ARRAY, Boolean, Column, DateTime, Integer, String, Text, func
from app.database import Base


# ── ORM model ────────────────────────────────────────────────────────────────

class Job(Base):
    __tablename__ = "jobs"

    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String(255), nullable=False)
    company    = Column(String(255), nullable=False)
    location   = Column(String(255))
    url        = Column(Text, unique=True, nullable=False)
    source     = Column(String(100), nullable=False, default="unknown")
    is_remote  = Column(Boolean, nullable=False, default=False)
    tags       = Column(ARRAY(String))
    salary     = Column(String(255))
    posted_at  = Column(DateTime(timezone=True))
    scraped_at = Column(DateTime(timezone=True), server_default=func.now())


# ── Pydantic schemas ──────────────────────────────────────────────────────────

class JobOut(BaseModel):
    id:        int
    title:     str
    company:   str
    location:  Optional[str]
    url:       str
    source:    str
    is_remote: bool
    tags:      Optional[list[str]]
    salary:    Optional[str]
    posted_at: Optional[datetime]
    scraped_at: datetime

    model_config = {"from_attributes": True}


class JobsResponse(BaseModel):
    total:  int
    page:   int
    limit:  int
    items:  list[JobOut]
