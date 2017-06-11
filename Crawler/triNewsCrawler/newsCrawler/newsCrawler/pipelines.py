# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .store import NewsDB

class NewscrawlerPipeline(object):
    def process_item(self, item, spider):
        #if spider.name != "news":
            #print ("spider.name!=news")
        #    return item
        if item.get("news_thread",None) is None:
            print("item.get(thread)=none")
            return item
        spec = {"news_thread":item["news_thread"]}
        NewsDB.new.update(spec,{"$set":dict(item)}, upsert = True)
	#print("update in mongodb")
        return None
