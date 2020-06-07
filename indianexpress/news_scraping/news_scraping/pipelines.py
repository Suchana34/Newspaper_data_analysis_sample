# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class NewsScrapingPipeline:
        
    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['news_paper_data']
        self.collection = db['indianexpress_tb']
    
    def process_item(self, item, spider):
        
        self.collection.insert(dict(item))
        return item

