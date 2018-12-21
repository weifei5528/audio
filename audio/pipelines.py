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
from scrapy.utils.project import get_project_settings
import zipfile
#import eyed3

TRUE_PATH = "uploads/images/beva/"
FILE_PATH = "uploads/mp3/beva/"


class AudioPipeline(object):
    def process_item(self, item, spider):
        mysql = Mysql()
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
            settings = get_project_settings()
            file_store = settings.get('FILES_STORE')
            file_path = ''
            file_original = item['file_urls'][0]
            if len(item['files']) > 0:

                f = zipfile.ZipFile(file_store + "/" + item['files'][0]['path'], 'r')
                for name in f.namelist():
                    file_path = FILE_PATH + name
                    f.extract(name, file_store)

            book_name = item['book_name']
            info = mysql.select_one("select * from dp_books where name = %s", (book_name,))
            if info is not None:
                chapter_info = mysql.select_one("select * from dp_chapters where name = %s AND book_id = %s",
                                                (item['name'], info['id']))
                if chapter_info is None:
                    now_time = int(time.time())
                    mysql.insert("insert into dp_chapters (name, img, img_original, book_id, content, description"
                                 ", create_time, update_time, mp3, mp3_original) values "
                                 "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                 (item['name'], TRUE_PATH + item['images'][0]['path'], item['image_urls'][0], info['id']
                                  , item['content'], item['description'], now_time, now_time, file_path,file_original))

            return item
        if isinstance(item, BevaBooks):
            type_name = item['type_name']
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
                             (item['name'], res[0]['id'], now_time, now_time, '未知', '未知', '贝瓦',
                              item['short_desc']))

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
