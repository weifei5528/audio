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
import os
import hashlib
from scrapy import log
from PIL import Image

IMG_PATH = "uploads/images/beva/"
FILE_PATH = "uploads/mp3/beva/"
STORE_PATH = "D:\work\python\public\\"

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
            """settings = get_project_settings()
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
                    att_info = mysql.select_one("select id from dp_admin_attachment where md5 = `%s`", ())
                    now_time = int(time.time())
                    mysql.insert("insert into dp_chapters (name, img, img_original, book_id, content, description"
                                 ", create_time, update_time, mp3, mp3_original) values "
                                 "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                 (item['name'], TRUE_PATH + item['images'][0]['path'], item['image_urls'][0], info['id']
                                  , item['content'], item['description'], now_time, now_time, file_path,file_original))"""
            self.book_img(item)

            return item
        if isinstance(item, BevaBooks):
            type_name = item['type_name']
            res = mysql.select("select * from dp_categories where name = %s", type_name)
            now_time = int(time.time())
            if len(res) == 0:
                count = mysql.insert("insert into dp_categories (name,create_time,update_time) values (%s, %s, %s)",
                                     (type_name, now_time, now_time))
                res = mysql.select("select * from dp_categories where name = %s", (type_name,))
                #print(count)
            book = mysql.select("select * from dp_books where name = %s and cat_id = %s", (item['name'], res[0]['id']))
            if len(book) == 0:
                mysql.insert("insert into dp_books (name, cat_id, create_time,update_time, author, publish, `from`"
                             ", description) values (%s, %s, %s, %s, %s, %s, %s, %s)",
                             (item['name'], res[0]['id'], now_time, now_time, '未知', '未知', '贝瓦',
                              item['short_desc']))

        return item

    def book_img(self, item):
        mysql = Mysql()
        settings = get_project_settings()
        file_store = settings.get('FILES_STORE')
        file_id = ''
        img_id = ''
        now_time = int(time.time())
        # 解压zip文件
        if len(item['files']) > 0:
            f = zipfile.ZipFile(file_store + "/" + item['files'][0]['path'], 'r')
            self.mk_dir(FILE_PATH + item['files'][0]['checksum'])
            f.extractall(file_store + "/" + item['files'][0]['checksum'])
            for name in f.namelist():
                # 记录存储的相对路径
                file_path = FILE_PATH + item['files'][0]['checksum'] + '/' + name
                # 查询数据库是否有记录 没有插入数据 返回 id
                log.msg(file_path)
                md5 = self.get_file_md5(file_path)
                log.msg(type(md5))
                log.msg(md5)
                file_info = mysql.select_one("select id from dp_admin_attachment where `md5` = %s", (md5,))
                if file_info is None:
                    mysql.insert("insert into dp_admin_attachment (name, module, path, url, mime, ext, size, md5, "
                                 "driver, create_time, update_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                                 , (name, 'book', file_path, item['file_urls'][0], 'audio/mp3', 'mp3',
                                    self.get_file_size(file_path), md5, 'local', now_time, now_time))
                    file_info = mysql.select_one("select id from dp_admin_attachment where md5 = %s", (md5,))

                file_id = file_info['id']
        # 查询图片是否添加
        if len(item['images']) > 0:
            path = IMG_PATH + item['images'][0]['path']
            size = self.get_file_size(path)
            md5 = self.get_file_md5(path)
            format, img_size, mode = self.get_image_info(path)
            image_info = mysql.select_one("select id from dp_admin_attachment where md5 = %s", (md5,))
            if image_info is None:
                mysql.insert("insert into dp_admin_attachment (name, module, path, url, mime, ext, size, md5, "
                             "driver, create_time, update_time, width, height) values (%s, %s, %s, %s, %s, %s, %s, %s,"
                             " %s, %s, %s, %s, %s)"
                             , (self.get_image_name(path), 'book', path, item['image_urls'][0], 'image/' + format,
                                 format, size, md5, 'local', now_time, now_time, img_size[0], img_size[1]))
                image_info = mysql.select_one("select id from dp_admin_attachment where md5 = %s", (md5,))
            img_id = image_info['id']
        # 查询图书是否存在
        info = mysql.select_one("select id from dp_books where name = %s", (item['book_name'],))
        if info is not None:
            chapter_info = mysql.select_one("select * from dp_chapters where name = %s AND book_id = %s",
                                            (item['name'], info['id']))

            if chapter_info is None:
                now_time = int(time.time())
                mysql.insert("insert into dp_chapters (name, img, book_id, content, description"
                             ", create_time, update_time, mp3) values "
                             "(%s, %s, %s, %s, %s, %s, %s, %s)",
                             (item['name'], img_id, info['id'], item['content'], item['description'], now_time,
                              now_time, file_id))

        return item

    # 目录不存在创建目录
    def mk_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    # 获取图片的信息
    def get_image_info(self, filename):
        img = Image.open(STORE_PATH+filename)
        return img.format.lower(), img.size, img.mode

    # 获取文件的名称
    def get_image_name(self,filename):
        return os.path.basename(STORE_PATH+filename)

    # 获取文件的大小
    def get_file_size(self, filename):
        return os.path.getsize(STORE_PATH+filename)

    def get_file_md5(self, filename):  # 产生MD5值
        if not os.path.isfile(STORE_PATH+filename):
            return

        myhash = hashlib.md5()
        f = open(STORE_PATH+filename, 'rb')
        while True:
            b = f.read(1024)
            if not b:
                break
            myhash.update(b)
        f.close()
        return myhash.hexdigest()

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
