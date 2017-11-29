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

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,value in results:
            image_file_path = value["path"]
        item['front_image_path'] = image_file_path
        return item

class JsonWithEncodingPipeline(object):
    # 自定义 json 文件的导出
    def __init__(self):
        self.file = codecs.open('article.json','w',encoding='utf-8')


    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self, spider):
        self.file.close()

class JsonExporterPipleline(object):
    # 调用 scrapy 提供的 json export 导出 json 文件
    def __init__(self):
        self.file = open('articleexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, enconding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item = item)
        return item


class MysqlPipleline(object):
    #数据库连接写入
    def __init__(self):
        self.conn = MySQLdb.connect('172.21.15.14','root','123456','article_spider',charset = 'utf8mb4',use_unicode=True)
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):
        # print("+++++++++++++++++" + item['title'] + "+++++++++++++++")
        insert_sql = """
          INSERT INTO jobbole_article(title, url, url_object_id, create_date, fav_nums) 
          VALUES (%s, %s, %s, %s, %s)
          """
        # t = item["title"]
        # u = item["url"]
        # o = item["url_object_id"]
        self.cursor.execute(insert_sql, (str(item["title"]).encode("utf-8"), item["url"], item["url_object_id"], item["create_date"], item["fav_nums"]) )
        # self.cursor.execute(insert_sql,("111", "www", "222", "2017/11/29", "0"))
        self.conn.commit()

