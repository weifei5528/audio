# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from audio.items import AudioItem, Book, Mp3, BevaBook, BevaBooks
from scrapy.pipelines.images import ImagesPipeline
from scrapy.http.request import Request
from audio.util import Util
from scrapy.pipelines.files import FilesPipeline
from audio.database import Mysql
import time
#import eyed3


class AudioPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, AudioItem):
            #print(item)
            pass
        if isinstance(item, Book):
            print(item)
            pass
        if isinstance(item, Mp3):
            print(item)
            pass
        if isinstance(item, BevaBook):
            print(item)
        if isinstance(item, BevaBooks):
            type_name = item['type_name']
            mysql = Mysql()
            res = mysql.select("select * from dp_categories where name = %s", type_name)
            now_time = int(time.time())
            if len(res) == 0:

                count = mysql.insert("insert into dp_categories (name,create_time,update_time) values (%s, %s, %s)",
                                     (type_name, now_time, now_time))
                res = mysql.select("select * from dp_categories where name = %s", type_name)
                #print(count)
            book = mysql.select("select * from dp_books where name = %s and cat_id = %s", (item['name'], res[0]['id']))
            if len(book) == 0:
                mysql.insert("insert into dp_books (name, cat_id, create_time,update_time, author, publish, `from`"
                             ", description) values (%s, %s, %s, %s, %s, %s, %s, %s)",
                             (item['name'], res[0]['id'], now_time, now_time, '未知', '未知', '贝瓦', item['short_desc']))
        return item


class MyImagepipeline(ImagesPipeline):
    def get_media_requests(self, item, info):

        if item.get('image_urls') is not None:
            for index in range(len(item['image_urls'])):
                path = Util.replace_special_str(item['dir_path'])
                yield Request(item['image_urls'][index], meta={'item': item, 'path': path})

    def file_path(self, request, response=None, info=None):
        path = request.meta['path']
        path = Util.replace_special_str(path)
        image_guid = request.url.split('/')[-1]
        filename = u'img/{0}/{1}'.format(path, image_guid)
        return filename

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            pass
        return item


class MyFilepipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        if item.get('file_urls') is not None:
            for index in range(len(item['file_urls'])):
                path = Util.replace_special_str(item['dir_path'])
                yield Request(item['file_urls'][index], meta={'item': item, 'path': path})

    def file_path(self, request, response=None, info=None):
        path = request.meta['path']
        path = Util.replace_special_str(path)
        image_guid = request.url.split('/')[-1]
        filename = u'img/{0}/{1}'.format(path, image_guid)
        return filename

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        if not image_path:
            pass
        return item
