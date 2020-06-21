# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from news_scraping.items import NewsScrapingItem

class NewscrawlSpider(Spider):
    name = 'newsCrawl'
    start_urls = ['https://www.anandabazar.com/']
    paths = ['#abp-homepage-top-section', 'body > main > section.abp-homepage-more-stories', 'body > main > section.abp-homepage-editors-choice > div > div > div',
    'body > main > section.abp-homepage-editors-choice > section.abp-homepage-editors-choice > div > div > div', 'body > main > section.abp-homepage-editors-choice > section.abp-homepage-editorial > div > div > div',
    'body > main > section.abp-homepage-editors-choice > section.abp-homepage-kolkata > div > div > div', 'body > main > section.abp-homepage-editors-choice > section:nth-child(9)',
    'body > main > section.abp-homepage-editors-choice > section.abp-homepage-country', 'body > main > section.abp-homepage-editors-choice > section.abp-homepage-international',
    'body > main > section.abp-homepage-editors-choice > section.abp-homepage-sports', 'body > main > section.abp-homepage-editors-choice > section.abp-homepage-lifestyle',
    'body > main > section.abp-homepage-editors-choice > section.abp-homepage-science']

    tags = '#abp-homepage-top-section .px-0 a'
    headings = 'h1'
    publish_date = '#abp-homepage-top-section > div > div > div > div.col-md-9.col-xs-12.abp-storypage-main-left-container > div:nth-child(3) > div > div.pr-0.abp-storypage-article-right-wrap > div:nth-child(4) > div.col-12.d-flex.abp-storypage-author-mob > ul.story-date > li:nth-child(3)'
    top_image = '#abp-storypage-img-section .img-fluid'
    
    def parse(self, response):
        print("you are in 1")
        
        for path in self.paths:
            for url in response.css(path).css("::attr(href)").extract():
                if url is not None:
                    print(url + " 1") 
                    req = Request(url="https://www.anandabazar.com" + url , callback= self.parse_article)  
                    yield req

    def parse_article(self,response):
        print("you are in 2")
        
        l = ItemLoader(item = NewsScrapingItem(), response=response)
        
        for tag in response.css(self.tags).css('::text').extract():
            tag = tag.strip()
            if(len(tag) > 0):
                l.add_value('tags', tag)
    
        for heading in response.css(self.headings).css('::text').extract():
            heading = heading.strip()
            if(len(heading) > 0):
                l.add_value('heading', heading)
    
        for date in response.css(self.publish_date).css('::text').extract():
            date = date.strip()
            if(len(date) > 0):
                l.add_value('publish_date', date)
    
            
        for image in response.css(self.top_image).css('::attr(src)').extract():
            if(image is not None):
                l.add_value('imagelink', "https:" + image)
        
        yield l.load_item()


