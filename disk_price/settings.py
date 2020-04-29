# -*- coding: utf-8 -*-

# Scrapy settings for disk_price project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'disk_price'

SPIDER_MODULES = ['disk_price.spiders']
NEWSPIDER_MODULE = 'disk_price.spiders'

SPLASH_URL = 'http://localhost:8050'

USER_AGENT = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Opera/8.0 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 534.57.2(KHTML, like Gecko) Version / 5.1.7 Safari / 534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)"',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
]

HTTPPROXY_ENABLED = True
PROXY_MAX_FAILED = 3

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'disk_price (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
DOWNLOAD_TIMEOUT = 10

RETRY_ENABLED = 10
RETRY_TIMES = 5
RETRY_HTTP_CODE = [500, 502, 503, 504, 522, 524, 408]
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16


# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = True

# REDIRECT_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider CutomMiddleware
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    # 'disk_price.middlewares.DiskPriceSpiderMiddleware': 543,
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader CutomMiddleware
# # See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'disk_price.CutomMiddleware.proxy_middleware.ProxyMiddleware': 539,
    'disk_price.middlewares.DiskPriceDownloaderMiddleware': 543,
    'disk_price.CutomMiddleware.useragent.UserAgentMiddleware': 544,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,

}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'disk_price.pipelines.DiskPricePipeline': 300,
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
# FEED_EXPORT_ENCODING = 'GB2312'

CRAWLERA_DOWNLOAD_TIMEOUT = 60
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE ='scrapy_splash.SplashAwareFSCacheStorage'
PROXIES = [
'https://125.110.88.233:9000',
'https://182.34.37.137:9999',
'https://171.13.136.178:9999',
'https://124.200.36.118:40188',
'https://110.189.152.86:52277',
'https://222.95.144.44:3000',
'https://121.33.220.158:808',
'https://118.113.234.101:8118',
'https://121.237.149.109:3000',
'https://61.150.96.27:46111',
'https://125.69.182.41:30228',
'https://60.216.101.46:59351',
'https://49.234.46.87:8888',
'https://121.237.148.201:3000',
'https://110.73.2.96:8123',
'https://222.95.144.129:3000',
'https://121.237.148.241:3000',
'https://222.95.144.119:3000',
'https://222.95.144.195:3000',
'https://121.237.149.88:3000',
'https://121.237.148.192:3000',
'https://121.237.148.183:3000',
'https://121.237.149.56:3000',
'https://121.237.149.163:3000',
'https://121.237.149.118:3000',
'https://117.88.176.228:3000',
'https://121.237.149.73:3000',
'https://222.95.144.92:3000',
'https://182.61.179.157:8888',
'https://117.88.177.20:3000',
'https://121.237.149.102:3000',
'https://117.88.5.105:3000',
'https://117.88.177.94:3000',
'https://115.223.99.148:8010',
'https://117.88.5.25:3000',
'https://117.88.4.211:3000',
'https://117.88.5.160:3000',
'https://117.88.4.99:3000',
'https://117.88.5.116:3000',
'https://202.115.142.147:9200',
'https://117.88.177.177:3000',
'https://122.4.54.133:1081',
'https://110.73.2.116:8123',
'https://117.87.50.89:8118',
'https://117.88.5.154:3000',
'https://117.88.4.61:3000',
'https://121.237.149.101:3000',
'https://117.88.5.208:3000',
'https://117.88.5.220:3000',
'https://117.88.4.113:3000',
'https://117.88.4.162:3000',
'https://27.203.208.195:8060',
'https://114.234.150.59:8060',

]