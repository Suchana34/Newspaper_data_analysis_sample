# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from news_scraping.items import NewsScrapingItem

class NewscrawlSpider(Spider):
    name = 'newsCrawl'
    start_urls = ['https://www.thestatesman.com/']
    allowed_domain = ['www.thestatesman.com']
    paths = ['.note-worthy-inner li a', '.soprts-right h4', '.entertainment-left-inner p', '.opinionSlider h2 a' ,'.aroundtheword li a','.storybx-summary a', '#featured-card a' ]
    summary = '.post-excerpt p'
    topic = 'span span span a'
    headings = '.heading'
    imagelink = '#loading_layer > div:nth-child(8) > div > div > div.col.col-md-9.col-sm-12 > div.row.featured-image > div > img'
    tags = '.tag a'
    date_author = '.col-xs-12 p'
    content = '#loading_layer > div:nth-child(8) > div > div > div.col.col-md-9.col-sm-12 > div.row.post-content > div p'
    def parse(self, response):
        print("you are in 1")
        
        for path in self.paths:
            for url in response.css(path).css("::attr(href)").extract():
                if url is not None:
                    print(url)
                    req = Request(url=url , callback= self.parse_article)
                    yield req

        

    def parse_article(self,response):
        print("you are in 2")
        
        l = ItemLoader(item = NewsScrapingItem(), response=response)

        
        topic = response.css(self.topic).css('::text').extract_first()
        l.add_value('topic', topic)
        
        for heading in response.css(self.headings).css('::text').extract():
            tag = heading.strip()
            if(len(tag) > 0):
                l.add_value('heading', tag)
                
        #heading can also be done in extract.first()

        for image in response.css(self.imagelink).css('::attr(src)').extract():
            if(image is not None):
                l.add_value('imagelink', image)
        
        text = response.css(self.summary).css('::text').extract_first()
        l.add_value('summary', text)

        date_published = response.css(self.date_author).css('::text').extract_first()
        l.add_value('date_author', date_published.strip())

        for content in response.css(self.content).css('::text').extract():
            l.add_value('content', content[:5000])

        for tag in response.css(self.tags).css('::text').extract():
            if(tag is not None):
                l.add_value('tags', tag)

        yield l.load_item()



