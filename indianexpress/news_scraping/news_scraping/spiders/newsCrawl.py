# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
import newspaper
from newspaper import Article
from news_scraping.items import NewsScrapingItem

class NewscrawlSpider(Spider):
    name = 'newsCrawl'
    start_urls = ['https://indianexpress.com/']
    allowed_domain = ['indianexpress.com']
    paths = ['.ie-first-story a', '.top-news a' , 'h1','.stories a', '.other-article a','.small-story a', '.heading a']
    synopsis = '.synopsis'
    headings = 'h1'
    tags = '.storytags a'
    
    def parse(self, response):
        print("you are in 1")
        
        for path in self.paths:
            for url in response.css(path).css("::attr(href)").extract():
                if url:
                    yield Request(url=url , callback= self.parse_article)
        

    def parse_article(self,response):
        print("you are in 2")
        
        l = ItemLoader(item = NewsScrapingItem(), response=response)
        
        for text in response.css(self.synopsis).css('::text').extract():
            if(text is not None):
                l.add_value('synopsis', text)
    
        for heading in response.css(self.headings).css('::text').extract():
            if(heading is not None):
                l.add_value('heading', heading)    
        for tag in response.css(self.tags).css('::text').extract():
            if(tag is not None):
                l.add_value('tags', tag)

        yield l.load_item()



