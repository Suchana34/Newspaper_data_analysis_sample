# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
import newspaper
from newspaper import Article
from news_scraping.items import NewsScrapingItem

class NewscrawlSpider(Spider):
    name = 'newsCrawl'
    start_urls = ['https://hindustantimes.com/']
    allowed_domain = ['hindustantimes.com']
    paths = ['.more-latest-news .headingfour a' , '.clearfix .para-txt a' , '.random-heading a' , '.new-assembly-elections a' , '.wclink2' , '.bigstory-mid-h3 a' , '.subhead4 a']
    subheadings = ['figcaption' , '#miwInL23P7y8wYxwF1WiDL_story h2']
    headings = 'h1'
    
    def parse(self, response):
        print("you are in 1")
        
        for path in self.paths:
            for url in response.css(path).css("::attr(href)").extract():
                if url is not None:
                    yield Request(url="https://www.hindustantimes.com/" + url , callback= self.parse_article)
        

    def parse_article(self,response):
        print("you are in 2")
        
        l = ItemLoader(item = NewsScrapingItem(), response=response)
        
        for subheading in self.subheadings:
            for word in response.css(subheading).css('::text').extract():
                if word is not None:
                    l.add_value('subheadings', word)
    
        for heading in response.css(self.headings).css('::text').extract():
            if(heading is not None):
                l.add_value('heading', heading)
    


        yield l.load_item()



