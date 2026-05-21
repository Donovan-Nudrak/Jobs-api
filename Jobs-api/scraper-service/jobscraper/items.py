import scrapy


class JobItem(scrapy.Item):
    title     = scrapy.Field()
    company   = scrapy.Field()
    location  = scrapy.Field()
    url       = scrapy.Field()
    source    = scrapy.Field()
    is_remote = scrapy.Field()
    tags      = scrapy.Field()
    salary    = scrapy.Field()
    posted_at = scrapy.Field()
