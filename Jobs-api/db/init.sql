-- Job Intelligence System — Initial Schema
CREATE TABLE IF NOT EXISTS jobs (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(255)    NOT NULL,
    company     VARCHAR(255)    NOT NULL,
    location    VARCHAR(255),
    url         TEXT            UNIQUE NOT NULL,
    source      VARCHAR(100)    NOT NULL DEFAULT 'unknown',
    is_remote   BOOLEAN         NOT NULL DEFAULT FALSE,
    tags        TEXT[],
    salary      VARCHAR(255),
    posted_at   TIMESTAMP,
    scraped_at  TIMESTAMP       NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_jobs_company   ON jobs (company);
CREATE INDEX IF NOT EXISTS idx_jobs_source    ON jobs (source);
CREATE INDEX IF NOT EXISTS idx_jobs_is_remote ON jobs (is_remote);
CREATE INDEX IF NOT EXISTS idx_jobs_scraped   ON jobs (scraped_at DESC);
