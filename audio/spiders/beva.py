# -*- coding: utf-8 -*-
import scrapy
from audio.items import BevaBooks, BevaBook
import re
class BevaSpider(scrapy.Spider):
    name = 'beva'
    allowed_domains = ['beva.com']
    my_host = "http://story.beva.com"
    start_urls = ['http://story.beva.com/99/']
    login_url = "http://account.beva.com/newAccount/ajaxLogin"
    def parse(self, response):
        list_tag = response.css(".slist > ul > li")
        for tag in list_tag:
            item = BevaBooks()
            item['name'] = tag.css("span.sll2 > a::text").extract_first()
            item['type_name'] = tag.css("span.wrc > a::text").extract_first()
            item['short_desc'] = tag.css("span.sll3::text").extract_first()
            #item['book'] = []
            url = tag.css("span.sll2 > a::attr(href)").extract_first()
            #print(url)
            yield scrapy.Request(self.my_host + url, callback=self.getDetail, meta={'book_name': item['name']})
            yield item
        page = response.css("#pagination")
        next_page = page.xpath("./a[contains(text(),'下一页')]/@href").extract_first()
        if next_page:
            yield scrapy.Request(self.my_host+next_page, callback=self.parse)

    def getDetail(self, response):
        book_name = response.meta['book_name']
        content = response.xpath("//div[@id='stcontent']/p[not(contains(@class,'stcatvc'))]").extract()
        if len(content) > 0:
            book = BevaBook()
            book['book_name'] = book_name
            book['image_urls'] = []
            img = response.xpath("//div[@class='stimg']/a/img/@src").extract_first()
            book['image_urls'].append(img)
            string_content = ''.join(content)
            book['content'] = string_content
            book['file_urls'] = []
            down_url = response.xpath("//form[@id='downLoad']/@action").extract_first()
            if down_url is not None:
                book['file_urls'].append(self.my_host + down_url)
            book['description'] = response.xpath("//div[@class='stinfo']/p/text()").extract_first()
            name = response.xpath("//div[@id='stcontent']/h1/text()").extract_first()

            if name is not None:
                name = re.sub('[\[\]【】]', '', name)
                book['name'] = name
            else:
                book['name'] = book_name
            yield book
            return book
        else:
            book_list = response.xpath("//div[@class='stch']/p[@class='stchtit']")
            for tag in book_list:
                url = tag.xpath("./a/@href").extract_first()
                yield scrapy.Request(self.my_host + url, callback=self.getDetail, meta={'book_name': book_name})









