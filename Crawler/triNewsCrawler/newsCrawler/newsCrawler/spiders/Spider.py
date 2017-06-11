# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from newsCrawler.items import newsCrawlerItem
from scrapy.contrib.linkextractors import LinkExtractor
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

class Spider(CrawlSpider):
    name = "news"
    allowed_domains = ["news.163.com"]
    start_urls = ['http://news.163.com']
    rules = (
            Rule(
                LinkExtractor(allow = r"/17/\d+/\d+/*"),
                callback = "parse_news",
                follow = True
                ),
            )

    def parse_news(self,response):
        item = newsCrawlerItem()
        item['news_thread'] = response.url.strip().split('/')[-1][:-5]
        self.get_title(response,item)
        self.get_source(response,item)
        self.get_url(response,item)
        self.get_news_from(response,item)
        self.get_from_url(response,item)
        self.get_text(response,item)
        return item

    def get_title(self,response,item):
        title = response.xpath("/html/head/title/text()").extract()
        if title:
            item['news_title'] = title[0][:-5]

    def get_source(self,response,item):
        #source = response.xpath("//div[@class = 'ep-time-soure cDGray']/text()").extract()
        #if source:
        item['news_source'] = 'netease'

    def get_news_from(self,response,item):
        news_from = response.xpath("//div[@class = 'ep-time-soure cDGray']/a/text()").extract()
        if news_from:
            item['news_from'] = news_from[0]

    def get_from_url(self,response,item):
        from_url = response.xpath("//div[@class='ep-time-soure cDGray']/a/@href").extract()
        if from_url:
            item['from_url']=from_url[0]

    def get_text(self,response,item):
        news_body = response.xpath("//div[@id='endText']/p/text()").extract()
        if news_body:
            item['news_body'] = news_body

    def get_url(self,response,item):
        news_url = response.url
        if news_url:
            item['news_url'] = news_url


class sinaSpider(CrawlSpider):
    name = 'sinaNews'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn']
    url_pattern = r'(http://(?:\w+\.)*news\.sina\.com\.cn)/.*/(\d{4}-\d{2}-\d{2})/\d{4}(\d{8})\.(?:s)html'
    rules = [
        Rule(
            #LinkExtractor(allow=[url_pattern]),
            #LinkExtractor(allow=r'/[cow](?:/\w{2})/(\d{4}-\d{2}-\d{2})/doc-i*\.(?:s)html'),
            LinkExtractor(allow=r'/(\d{4}-\d{2}-\d{2})/*'),
            callback = 'parse_news',
            #follow = True
            follow = False
            ),
        ]

    def parse_news(self,response):
        item = newsCrawlerItem()
        #http://mil.news.sina.com.cn/2017-06-06/doc-ifyfuzny3608195.shtml
        item['news_thread'] = response.url.strip().split('/')[-1][5:-6]
        print('news_thread:', item['news_thread'])
        item['news_title'] = response.xpath("/html/head/title/text()").extract()
        print('news_title:', item['news_title'])
        item['news_source'] = 'sina'
        print('news_source:', item['news_source'])
        news_from = response.xpath("//span[@data-sudaclick = 'media_name']/a/text()").extract()
        if news_from:
            item['news_from'] = news_from[0]
        else:
            item['news_from'] = 'sina'
        print('news_from:', item['news_from'])
        from_url = response.xpath("//span[@data-sudaclick = 'media_name']/a/@href").extract()
        if from_url:
            item['from_url'] = from_url[0]
        else:
            item['from_url'] = response.url
        print('from_url:', item['from_url'])
        sel = Selector(response)
        item['news_body'] = response.xpath("//div[@id='artibody']/p/text()").extract()
        print('news_body:', item['news_body'])
        item['news_url'] = response.url
        print('news_url:', item['news_url'])
        return item

    def ListCombiner(lst):
        string = ''
        for e in lst:
            string += e
        return string

class tencentSpider(CrawlSpider):
    name = 'tencentNews';




    

