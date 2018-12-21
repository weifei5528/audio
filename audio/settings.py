# -*- coding: utf-8 -*-

# Scrapy settings for audio project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
BOT_NAME = 'audio'

SPIDER_MODULES = ['audio.spiders']
NEWSPIDER_MODULE = 'audio.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'audio (+http://www.yourdomain.com)'
DOWNLOAD_TIMEOUT = 20

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
LOG_FILE = "mySpider.log"
LOG_LEVEL = "INFO"
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = True

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
#    'audio.middlewares.AudioSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
    #'audio.middlewares.AudioDownloaderMiddleware': 543,
    #'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}
MEDIA_ALLOW_REDIRECTS = True
# user agent 列表
USER_AGENT_LIST = [
    'MSIE (MSIE 6.0; X11; Linux; i686) Opera 7.23',
    'Opera/9.20 (Macintosh; Intel Mac OS X; U; en)',
    'Opera/9.0 (Macintosh; PPC Mac OS X; U; en)',
    'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
    'Mozilla/4.76 [en_jp] (X11; U; SunOS 5.8 sun4u)',
    'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0',
    'Mozilla/4.77 [en] (X11; I; IRIX;64 6.5 IP30)',
    'Mozilla/4.8 [en] (X11; U; SunOS; 5.7 sun4u)'
]
# 随机生成user agent
USER_AGENT = random.choice(USER_AGENT_LIST)

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'audio.pipelines.AudioPipeline': 300,
    'scrapy.pipelines.images.ImagesPipeline': 10,
    'scrapy.pipelines.files.FilesPipeline': 15,
    # 'audio.pipelines.MyImagepipeline': 10,
   # 'audio.pipelines.MyFilepipeline': 20
}
IMAGES_STORE = r'D:\work\python\public\uploads\images\beva'

FILES_STORE = r'D:\work\python\public\uploads\mp3\beva'

# 图像管道避免下载最近已经下载的图片。使用 FILES_EXPIRES (或 IMAGES_EXPIRES) 设置可以调整失效期限，
# 可以用天数来指定
IMAGES_EXPIRES = 30
FILES_EXPIRES = 120
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
