# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import datetime
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import  ItemLoader
import re


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def add_jobbole(value):
    return value + "-jobbole"


def data_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date

def get_nums(values): #获取数字，正则匹配
    match_re = re.match(".*?(\d+).*", values)
    if (match_re):
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def remove_comment_tags(value):
    #去除 tag 中提取的评论
    if("评论" in value):
        return ""
    else:
        return value

def return_value(value):
    return value



class ArticleItemLoader(ItemLoader):
    #自定义 ItemLoader 重载类
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        input_processor = MapCompose(add_jobbole),
    ) #Item里面只有 Filed 一种类型
    create_date = scrapy.Field(
        input_processor = MapCompose(data_convert)#传递函数，对数据进行预处理
    ) #创建日期
    url = scrapy.Field() #url
    url_object_id = scrapy.Field() #md5 url
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    ) #图像 url
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )  #点赞数
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    ) #评论数
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    ) #收藏数
    tags = scrapy.Field(
        input_processor = MapCompose(remove_comment_tags),
        output_processor = Join(",")
    ) #标签
    content = scrapy.Field() #文章内容
