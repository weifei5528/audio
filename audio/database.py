import pymysql
from configparser import ConfigParser


class Mysql(object):
    def __init__(self):
        con = ConfigParser()
        con.read('audio/db.cfg', 'UTF-8')
        sections = con.sections()
        mysql_section = sections[0]
        self.host = con.get(mysql_section, 'host')
        self.user = con.get(mysql_section, 'user')
        self.password = con.get(mysql_section, 'passwd')
        self.port = con.getint(mysql_section, 'port')
        self.database = con.get(mysql_section, 'db')
        #self.charset = con.get(mysql_section, 'charset', fallback='UTF-8')

        self.cursor_type = pymysql.cursors.DictCursor

    def connect(self):
        try:
            db = pymysql.connect(self.host, self.user, self.password, self.database, self.port)
            return db
        except pymysql.MySQLError as e:
            print("mysql连接错误，错误信息为:" + ' '.join(tuple(e.args)))


    # @param where 数组  里面参数 3 1key 2 比较条件 3 值（可以为 string 或者是数组）
#    def where(self, where):
#        for key, comp, value in where:
#            self.where += key +
    def select(self, sql, param=()):
        try:
            db = self.connect()
            cursor = db.cursor(self.cursor_type)
            cursor.execute(sql, param)
            results = cursor.fetchall()
        except pymysql.MySQLError as e:
            print("查询数据错误，错误信息为:" + ' '.join(tuple(e.args)))
        finally:
            cursor.close()
            db.close()
        return results

    def insert(self, sql, param=()):
        try:
            db = self.connect()
            cursor = db.cursor(self.cursor_type)
            count = cursor.execute(sql, param)
            db.commit()
            return count
        except pymysql.MySQLError as e:
            db.rollback()
            print("插入数据错误，错误信息为:" + ' '.join(tuple(e.args)))
        finally:
            cursor.close()
            db.close()

    def select_one(self, sql, param=()):
        try:
            db = self.connect()
            cursor = db.cursor(self.cursor_type)
            cursor.execute(sql, param)
            results = cursor.fetchone()
        except pymysql.MySQLError as e:
            print("查询数据错误，错误信息为:" + ' '.join(tuple(e.args)))
        finally:
            cursor.close()
            db.close()
        return results



