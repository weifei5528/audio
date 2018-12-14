# -*- coding: utf-8 -*-
import scrapy
from audio.items import AudioItem, Book, Mp3


class YoubanSpider(scrapy.Spider):
    name = 'youban'
    allowed_domains = ['youban.com']
    start_urls = ['http://www.youban.com/mp3/']

    def parse(self, response):
        li_tags = response.css("div.Mp3HotwarpMain > ul > li")
        for tag in li_tags:
            url = tag.css("a::attr(href)").extract_first()
            yield scrapy.Request(url, callback=self.get_book)



    def get_book(self, response):
        item = AudioItem()
        item_tags = response.css("div.TypeNameinfo")
        item['name'] = item_tags.css("div.TypeNameText > h3::text").extract_first()
        item['description'] = item_tags.css("div.TypeNameText > p::text").extract_first()
        item['image_urls'] = []
        item_img = item_tags.css("div.TypeNameImg > img::attr(src)").extract_first()
        # 添加item的图片
        item['image_urls'].append(item_img)
        item['dir_path'] = str(item['name']+"/")
        li_tags = response.css("div.Mp3ALLgequMain > ul > li")
        for tag in li_tags:
            url = tag.css('p > a::attr(href)').extract_first()
            if type(url) is not None:
                yield scrapy.Request(url, callback=self.get_book_detail, meta={'path': item['dir_path']})
        yield item
        #return item

    """
    获取图书的详细信息
    """
    def get_book_detail(self, response):
        path = response.meta['path']
        book = Book()
        book['image_urls'] = []
        book_tags = response.css("div.TypeNameinfo")
        book['name'] = book_tags.css("div.TypeNameText > h3::text").extract_first()
        book['dir_path'] = path + str(book['name']) + "/"
        image = book_tags.css("div.TypeNameImg > img::attr(src)").extract_first()
        book['image_urls'].append(image)
        listen_tags = response.css("#topicListern >ul >li")
        for tag in listen_tags:
            url = tag.css("span>a::attr(href)").extract_first()
            yield scrapy.Request(url, callback=self.get_download_page, meta={'path': book['dir_path']})
        #
        yield book
        return book
    """
    获取音频文件的详细信息
    """
    def get_download_page(self, response):
        path = response.meta['path']
        mp3 = Mp3()
        mp3['name'] = response.css("div.Mp3showInfobox > h1::text").extract_first()
        mp3['dir_path'] = path+str(mp3['name'])+"/"
        url = response.css("div.DownBtnbox >a.downbtnboxicon::attr(href)").extract_first()
        if type(url) is not None:
            yield scrapy.Request(url, callback=self.get_mp3_info, meta={'mp3': mp3})
            yield mp3

        #return mp3
    """
    获取音频文件的下载地址
    """
    def get_mp3_info(self, response):
        mp3 = response.meta['mp3']
        mp3['file_urls'] = []
        url = response.css("div.downloadboxlist > p>a::attr(href)").extract_first()
        if '.mp3' in url:
            mp3['original_path'] = url
            mp3['file_urls'].append(url)
            return mp3


