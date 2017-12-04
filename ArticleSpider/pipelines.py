# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs
import json
import sys
from scrapy.exporters import JsonItemExporter
import MySQLdb
from twisted.enterprise import adbapi
import MySQLdb.cursors
import datetime


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if("front_image_url" in item):
            for ok,value in results:
                image_file_path = value["path"]
            item['front_image_path'] = image_file_path
        return item

class ComplexEncoder(json.JSONEncoder):
    #扩招 json 的功能
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class JsonWithEncodingPipeline(object):
    # 自定义 json 文件的导出
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding='utf-8')


    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False, cls=ComplexEncoder) + "\n"
        self.file.write(lines)
        return item


    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipleline(object):
    # 调用 scrapy 提供的 json export 导出 json 文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding = "utf-8" ,ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipleline(object):
    #数据库连接写入 同步
    def __init__(self):
        self.conn = MySQLdb.connect('172.21.15.14','root','123456','article_spider',charset = 'utf8',use_unicode=True)
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        # print("+++++++++++++++++" + item['title'] + "+++++++++++++++")
        insert_sql = """
          INSERT INTO jobbole_article(title, url, url_object_id, create_date, fav_nums) 
          VALUES (%s, %s, %s, %s, %s)
          """
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["url_object_id"], item["create_date"], item["fav_nums"]))
        # self.cursor.execute(insert_sql, (str(item["title"]).encode("utf-8"), item["url"], item["url_object_id"], item["create_date"], item["fav_nums"]) )
        self.conn.commit()

class MysqlTwistedPipline(object):
    #异步化 mysql
    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        #使用 twisted 将 mysql 插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常


    def handle_error(self, failure, item, spider):
        #处理异步插入的异常  错误处理函数
        print(failure)

    def do_insert(self, cursor, item):
        #执行具体插入
        insert_sql = """
                  INSERT INTO jobbole_article(title, create_date, url, url_object_id, front_image_url,front_image_path,
                   praise_nums,comment_nums, fav_nums, tags, content) 
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )
                  """
        cursor.execute(insert_sql,(item["title"],item["create_date"], item["url"],item["url_object_id"],
                                   item["front_image_url"][0], item["front_image_path"], item["praise_nums"],
                                   item["comment_nums"], item["fav_nums"],item["tags"],item["content"]))



    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
        host=settings["MYSQL_HOST"],
        db = settings["MYSQL_DBNAME"],
        user = settings["MYSQL_USER"],
        passwd = settings["MYSQL_PASSWORD"],
        charset = 'utf8',
        cursorclass = MySQLdb.cursors.DictCursor,
        use_unicode = True
        )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)


