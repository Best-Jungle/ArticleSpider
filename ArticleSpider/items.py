# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field() #Item里面只有 Filed 一种类型
    create_date = scrapy.Field() #创建日期
    url = scrapy.Field() #url
    url_object_id = scrapy.Field() #md5 url
    front_image_url = scrapy.Field() #图像 url
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()  #点赞数
    comment_nums = scrapy.Field() #评论数
    fav_nums = scrapy.Field() #收藏数
    tags = scrapy.Field() #标签
    content = scrapy.Field() #文章内容
