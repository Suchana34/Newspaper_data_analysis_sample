# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from news_scraping.items import NewsScrapingItem

class NewscrawlSpider(Spider):
    name = 'newsCrawl'
    start_urls = ['https://www.telegraphindia.com/']
    allowed_domain = ['www.telegraphindia.com']
    paths = ['.ellipsis_data_2']
    summary = '.fs-20.noto-regular'
    topic = '.muted-link+ .muted-link .text-breadcrumbs'
    headings = '.mb-2'
    imagelink = '.pb-4 .pt-2 img'
    tags = '.px-4'
    date = '.col .noto-regular span:nth-child(1)'
    content = 'p'
    def parse(self, response):
        print("you are in 1")
        
        for path in self.paths:
            for url in response.css(path).css("::attr(href)").extract():
                if url is not None:
                    print(url)
                    req = Request(url= "https://www.telegraphindia.com/" + url , callback= self.parse_article)
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
        
        text = response.css(self.summary).css('::text').extract_first()
        l.add_value('summary', text)

        date_published = response.css(self.date).css('::text').extract_first()
        l.add_value('date_published', date_published)

        for content in response.css(self.content).css('::text').extract():
            l.add_value('content', content[:5000])

        for tag in response.css(self.tags).css('::text').extract():
            if(tag is not None):
                l.add_value('tags', tag)

        yield l.load_item()



