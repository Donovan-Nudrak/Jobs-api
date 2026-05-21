import json
import scrapy
from jobscraper.items import JobItem


class RemoteOKSpider(scrapy.Spider):
    """
    Spider for RemoteOK — fetches jobs from the public JSON API.
    RemoteOK exposes https://remoteok.com/api which returns a JSON array;
    the first element is a metadata disclaimer object, the rest are job objects.
    """

    name = "remoteok"
    allowed_domains = ["remoteok.com"]
    start_urls = ["https://remoteok.com/api"]

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            # RemoteOK requires a User-Agent that is not a known bot string
            "User-Agent": (
                "Mozilla/5.0 (compatible; JobIntelligenceBot/1.0; "
                "+https://github.com/your-org/job-intelligence-system)"
            ),
            "Accept": "application/json",
        },
        # Be polite — one request per second
        "DOWNLOAD_DELAY": 1,
        "AUTOTHROTTLE_ENABLED": True,
    }

    def parse(self, response):
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as exc:
            self.logger.error("Failed to parse JSON from RemoteOK: %s", exc)
            return

        # Skip the first element (legal/disclaimer object)
        jobs = data[1:] if isinstance(data, list) else []
        self.logger.info("RemoteOK returned %d job listings", len(jobs))

        for job in jobs:
            yield self._parse_job(job)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _parse_job(self, job: dict) -> JobItem:
        tags = job.get("tags") or []
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",") if t.strip()]

        location = job.get("location") or ""
        is_remote = bool(
            job.get("remote")
            or "remote" in location.lower()
            or not location
        )

        return JobItem(
            title=self._clean(job.get("position") or job.get("title", "")),
            company=self._clean(job.get("company", "")),
            location=self._clean(location) or "Remote",
            url=self._clean(job.get("url", "")),
            source="remoteok",
            is_remote=is_remote,
            tags=tags,
            salary=self._clean(job.get("salary", "")),
            posted_at=job.get("date"),
        )

    @staticmethod
    def _clean(value: str) -> str:
        return value.strip() if isinstance(value, str) else ""
