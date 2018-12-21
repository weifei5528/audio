# -*- coding: utf-8 -*-
import scrapy
from audio.items import BevaBooks, BevaBook
import re
import json

class BevaSpider(scrapy.Spider):
    name = 'beva'
    allowed_domains = ['beva.com']
    my_host = "http://story.beva.com"
    start_urls = ['http://story.beva.com/99/']
    login_url = "http://account.beva.com/newAccount/register?returnUrl=http%3A%2F%2Fstory.beva.com%2F&source=2"
    login_data = {
        'beva_username': 'weifei528@qq.com',
        'beva_password': 'weifei851213',
        'source': '2',
        'beva_rememberMe': "on"
    }
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Referer": "http://story.beva.com"
    }

    def start_requests(self):
        return [scrapy.Request(url="http://account.beva.com/newAccount/register?returnUrl=http%3A%2F%2Fstory.beva.com%2F"
                                   "&source=2", meta={'cookiejar': 1},
                               callback=self.login_html)]

    def login_html(self, response):
        #cookie1 = response.headers.getlist('Set-Cookie')
        #print("cookie1的值为:", cookie1)
        return [scrapy.FormRequest.from_response(response,
                                                 url='http://account.beva.com/newAccount/ajaxLogin',  # 真实post地址
                                                 meta={'cookie': response.meta['cookiejar']},
                                                 formdata=self.login_data,
                                                 callback=self.login,
                                                 headers=self.headers,
                                                 method="POST",
                                                 dont_filter=True)]

    def login(self, response):
        print(response.request)
        cookie2 = response.request.headers.getlist('cookiejar')
        print('登录时携带请求的Cookies：', cookie2)
        jieg = response.body  # 登录后可以查看一下登录响应信息

        print('登录响应结果：', json.loads(jieg))
        yield self.make_requests_from_url(self.start_urls[0])

    def parse(self, response):
        print(response.request.headers)
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









