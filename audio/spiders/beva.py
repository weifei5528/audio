# -*- coding: utf-8 -*-
import scrapy
from audio.items import beva

class BevaSpider(scrapy.Spider):
    name = 'beva'
    allowed_domains = ['beva.com']
    my_host = "http://story.beva.com"
    start_urls = ['http://story.beva.com/99/']

    def parse(self, response):
        list_tag = response.css(".slist > ul > li")
        for tag in list_tag:
            item = beva()
            item['name'] = tag.css("span.sll2 > a::text").extract_first()
            item['type_name'] = tag.css("span.wrc > a::text").extract_first()
            item['short_desc'] = tag.css("span::text").extract_first()
            url = tag.css("span.sll2 > a::attr(href)").extract_first()
            print(url)
            #yield scrapy.Request(url, callback=self.getDetail, meta={'item':item})
        page = response.css("#pagination")
        next_page = page.xpath("./a[contains(text(),'下一页')]/@href").extract_first()
        if next_page:
            yield scrapy.Request(self.my_host+next_page, callback=self.parse)


    def getDetail(self, response):
        item = response.meta['meta']
        item['image_urls'] = []
        img = response.xpath("//div[@class,'stimg']/a/img/@src").extract_first()
        item['image_urls'].append(img)
        item['description'] = response.xpath("//div[@class,'stinfo']/p/@text").extract_first()






