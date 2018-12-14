# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AudioItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    dir_path = scrapy.Field()
    description = scrapy.Field()
    image_urls = scrapy.Field()


class Book(scrapy.Item):
    name = scrapy.Field()
    description = scrapy.Field()
    dir_path = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()


class Mp3(scrapy.Item):
    name = scrapy.Field()
    file_urls = scrapy.Field()
    dir_path = scrapy.Field()
    original_path = scrapy.Field()
    files = scrapy.Field()


