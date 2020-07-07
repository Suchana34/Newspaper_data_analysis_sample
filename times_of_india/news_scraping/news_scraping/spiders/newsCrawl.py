# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from news_scraping.items import NewsScrapingItem

class NewscrawlSpider(Spider):
    name = 'newsCrawl'
    start_urls = ['https://timesofindia.indiatimes.com/']
    allowed_domain = ['timesofindia.indiatimes.com']
    paths = ['.top-story a','.list_article span' , '.cvs_wdt a' , '.list9 a' , '.list8 a']
    tags = ['.IXtDK a', '.trending_block_inner a', '.slideshowbox a']
    headings = 'h1'
    author = '.byline a'
    content = ['.Normal', '._1_Akb.clearfix', '.content']
    
    def parse(self, response):
        print("you are in 1")
        
        for path in self.paths:
            for url in response.css(path).css("::attr(href)").extract():
                if url is not None:
                    req = Request(url="https://timesofindia.indiatimes.com/" + url , callback= self.parse_article)
                    yield req
        

    def parse_article(self,response):
        print("you are in 2")
        
        l = ItemLoader(item = NewsScrapingItem(), response=response)
        
        for tag in self.tags:
            for word in response.css(tag).css('::text').extract():
                if word is not None:
                    l.add_value('tags', word)
    
        for heading in response.css(self.headings).css('::text').extract():
            if(heading is not None):
                l.add_value('heading', heading)
    
        #for image in response.css(self.imagelink).css('::attr(src)').extract():
        #    if(image is not None):
        #        l.add_value('imaginelink', image)

        
        author = response.css(self.author).css('::text').extract_first()
        l.add_value('author', author)
        
        for i in self.content:
            for text in response.css(i).css('::text').extract():
                l.add_value('content', text)

        yield l.load_item()



