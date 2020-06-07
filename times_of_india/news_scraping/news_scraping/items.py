# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsScrapingItem(scrapy.Item):
    # define the fields for your item here like:
    heading = scrapy.Field()
    #text = scrapy.Field()
    tags = scrapy.Field()
    #imagelink = scrapy.Field()
    author = scrapy.Field()
    #info = scrapy.Field()