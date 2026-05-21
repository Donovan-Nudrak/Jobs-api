import logging
import os

import psycopg2
from psycopg2.extras import execute_values

logger = logging.getLogger(__name__)

_INSERT_SQL = """
INSERT INTO jobs (title, company, location, url, source, is_remote, tags, salary, posted_at)
VALUES %s
ON CONFLICT (url) DO UPDATE SET
    title      = EXCLUDED.title,
    company    = EXCLUDED.company,
    location   = EXCLUDED.location,
    is_remote  = EXCLUDED.is_remote,
    tags       = EXCLUDED.tags,
    salary     = EXCLUDED.salary,
    posted_at  = EXCLUDED.posted_at,
    scraped_at = NOW();
"""


class PostgresPipeline:
    """Bulk-insert Scrapy items into PostgreSQL using psycopg2."""

    BATCH_SIZE = 50  # flush every N items

    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            port=int(os.getenv("DB_PORT", 5432)),
            dbname=os.getenv("DB_NAME", "jobsdb"),
            user=os.getenv("DB_USER", "jobuser"),
            password=os.getenv("DB_PASS", "jobpass"),
        )
        self.cursor = self.conn.cursor()
        self._buffer: list[tuple] = []
        logger.info("PostgresPipeline: connected to database")

    def close_spider(self, spider):
        self._flush()
        self.cursor.close()
        self.conn.close()
        logger.info("PostgresPipeline: connection closed")

    def process_item(self, item, spider):
        self._buffer.append(self._to_tuple(item))
        if len(self._buffer) >= self.BATCH_SIZE:
            self._flush()
        return item

    # ------------------------------------------------------------------

    def _flush(self):
        if not self._buffer:
            return
        try:
            execute_values(self.cursor, _INSERT_SQL, self._buffer)
            self.conn.commit()
            logger.info("PostgresPipeline: flushed %d items", len(self._buffer))
        except Exception as exc:
            self.conn.rollback()
            logger.error("PostgresPipeline: flush failed — %s", exc)
        finally:
            self._buffer.clear()

    @staticmethod
    def _to_tuple(item) -> tuple:
        return (
            item.get("title", ""),
            item.get("company", ""),
            item.get("location", ""),
            item.get("url", ""),
            item.get("source", "unknown"),
            bool(item.get("is_remote", False)),
            item.get("tags") or [],
            item.get("salary") or None,
            item.get("posted_at") or None,
        )
