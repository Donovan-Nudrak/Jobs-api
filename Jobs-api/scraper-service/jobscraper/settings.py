BOT_NAME = "jobscraper"

SPIDER_MODULES = ["jobscraper.spiders"]
NEWSPIDER_MODULE = "jobscraper.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Polite crawling
DOWNLOAD_DELAY = 1
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Enable our pipeline
ITEM_PIPELINES = {
    "jobscraper.pipelines.PostgresPipeline": 300,
}

# Logging
LOG_LEVEL = "INFO"

# Feed export encoding
FEED_EXPORT_ENCODING = "utf-8"

# Disable cookies (not needed)
COOKIES_ENABLED = False

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
