# -*- coding: utf-8 -*-

# Scrapy settings for CrawlBot project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'CrawlBot'

SPIDER_MODULES = ['CrawlBot.spiders']
NEWSPIDER_MODULE = 'CrawlBot.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'CrawlBot (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'CrawlBot.middlewares.IndiabixSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'CrawlBot.middlewares.IndiabixDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'CrawlBot.pipelines.IndiabixPipeline': 500,
    'CrawlBot.pipelines.SendCSVFilePipeline': 400,
    'CrawlBot.pipelines.CsvExporterPipeline': 300,
    'CrawlBot.pipelines.CleanDataPipeline': 200


}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# STATS_CLASS = 'scraper.stats.MyStatsCollector'

#Export as CSV Feed
FEED_EXPORTERS = {
    'csv': 'CrawlBot.custom_csv_class.MyProjectCsvItemExporter',
}
FIELDS_TO_EXPORT = [
    "question_text", "answer_1", "answer_2", "answer_3", "answer_type", "right_answer", "question_type", "difficulty_level", "binary_file_path",
    "category"
]
CSV_DELIMITER = ";"

URL_TO_SEND = 'http://10.177.7.134:9000/file/upload'

# Command to run csv scrapy crawl IndiaBixArrangeSpider -o test.csv -a filename=test.csv -t csv -a CSV_DELIMITER=";"

#FEED_FORMAT = "csv"
#FEED_URI = "IndiaBixSingle.csv"
#FEED_EXPORT_FIELDS = ["question_text", "answer_1", "answer_2", "answer_3", "answer_type", "right_answer", "question_type", "difficulty_level", "binary_file_path"]

# LOG_LEVEL = 'DEBUG'






# from scrapy.settings.default_settings import DOWNLOADER_MIDDLEWARES
#
# DOWNLOADER_MIDDLEWARES.update({
#     'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
#     'scrapy_rotated_proxy.downloadmiddlewares.proxy.RotatedProxyMiddleware': 750,
# })
# ROTATED_PROXY_ENABLED = True
# PROXY_STORAGE = 'scrapy_rotated_proxy.extensions.file_storage.FileProxyStorage'
# # When set PROXY_FILE_PATH='', scrapy-rotated-proxy
# # will use proxy in Spider Settings default.
# PROXY_FILE_PATH = ''
# HTTP_PROXIES = [
#     'http://proxy0:8888',
#     'http://user:pass@proxy1:8888',
#     'https://user:pass@proxy1:8888',
# ]
# HTTPS_PROXIES = [
#     'http://proxy0:8888',
#     'http://user:pass@proxy1:8888',
#     'https://user:pass@proxy1:8888',
# ]


#
# DOWNLOADER_MIDDLEWARES.update({
#     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
#     'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
# })