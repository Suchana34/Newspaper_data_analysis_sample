# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from news_scraping.items import NewsScrapingItem

class NewscrawlSpider(Spider):
    name = 'newsCrawl'
    start_urls = ['https://www.deccanherald.com/']
    allowed_domain = ['www.deccanherald.com']
    paths = ['.card-cta']
    topic = '.first+ li a'
    headings = '#page-title'
    imagelink = '.caption-processed'
    tags = '#main-wrapper .field-item a'
    date = '.crud-items__lists:nth-child(1)'
    content = '#main-wrapper .even p'
    
    def parse(self, response):
        print("you are in 1")
        
        for path in self.paths:
            for url in response.css(path).css("::attr(href)").extract():
                if url is not None:
                    print(url)
                    req = Request(url= "https://www.deccanherald.com/" + url , callback= self.parse_article)
                    yield req

        

    def parse_article(self,response):
        print("you are in 2")
        
        l = ItemLoader(item = NewsScrapingItem(), response=response)

        
        topic = response.css(self.topic).css('::text').extract_first()
        l.add_value('topic', topic)
        
        for heading in response.css(self.headings).css('::text').extract():
            if(heading is not None):
                l.add_value('heading', heading)
                

        for image in response.css(self.imagelink).css('::attr(src)').extract():
            if(image is not None):
                l.add_value('imagelink', image)
        

        date_published = response.css(self.date).css('::text').extract_first()
        l.add_value('date_published', date_published)

        for content in response.css(self.content).css('::text').extract():
            l.add_value('content', content[:5000])

        for tag in response.css(self.tags).css('::text').extract():
            if(tag is not None):
                l.add_value('tags', tag)

        yield l.load_item()



