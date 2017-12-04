# -*- coding: utf-8 -*-
#author = "王栎汉 2017年11月21日"
import scrapy
from scrapy.http import Request
from  urllib import parse
from scrapy.loader import ItemLoader
import re
from ArticleSpider.items import JobBoleArticleItem,ArticleItemLoader
from ArticleSpider.utils.common import get_md5
import datetime



class JobboleSpider(scrapy.Spider):
    #spider 类
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        #1.获取文章列表页中的文章 url，交给 scrapy 下载并解析
        #2.获取下一页的 url，并交给 scrapy 下载，下载完成后交给 parse
        post_nodes = response.css("#archive div.floated-thumb .post-thumb a")
        for post_node in post_nodes:#单个页面中循环处理
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image_url":parse.urljoin(response.url,image_url) }, callback=self.parse_detail) #meta 将数据打包传到 response 中


        next_urls = response.css(".next.page-numbers ::attr(href)").extract_first("")#两个 class 并行，取消中间空格
        # next_urls = response.css(".next.page-numbers a::attr(href)")
        if(next_urls):#查找下一页
            yield Request(url=parse.urljoin(response.url,next_urls),callback=self.parse)



    def parse_detail(self,response): #处理每篇文章页面中内容
        print("开始")
        article_item = JobBoleArticleItem()
        #xpath 抓取方式
        # title = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract()[0]
        # create_date = response.xpath('//*[@id="post-110287"]/div[2]/p/text()').extract()[0].strip().replace("·","").strip()

        # front_image_url = response.meta.get("front_image_url","")
        # title = response.css(".entry-header h1::text").extract_first() #标题
        # create_date = response.css("p.entry-meta-hide-on-mobile::text").extract_first().strip().replace("·","").strip()#创建日期
        # praise_nums = response.css(".vote-post-up h10::text").extract_first()#点赞数
        # fav_nums = response.css(".bookmark-btn::text").extract_first()#收藏
        # match_re = re.match(".*?(\d+).*",fav_nums)
        # if(match_re):
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        # comment_nums = response.css("a[href='#article-comment'] span::text").extract_first()#评论
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if (match_re):
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0

        # content = response.css("div.entry").extract_first()#文章内容
        # tag_list = response.css("p.entry-meta-hide-on-mobile a::text").extract()#所属类别
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)
        #
        # article_item["title"] = title
        # article_item["url"] = response.url
        # article_item["url_object_id"] = get_md5(response.url)
        # try:
        #     create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # article_item["create_date"] = create_date
        # article_item["front_image_url"] = [front_image_url]
        # article_item["praise_nums"] = praise_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["tags"] = tags
        # article_item["content"] = content


        # 通过 item loader 容器加载 item
        front_image_url = response.meta.get("front_image_url", "")
        item_loader = ArticleItemLoader(item = JobBoleArticleItem(), response = response)
        item_loader.add_css("title", ".entry-header h1::text" )
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url) )
        item_loader.add_css("create_date", "p.entry-meta-hide-on-mobile::text")
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", "a[href='#article-comment'] span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", "div.entry")
        article_item = item_loader.load_item()
        yield article_item # 会将数据传递到 pipelines 中

        pass
