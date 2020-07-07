# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
from news_scraping.items import NewsScrapingItem

class NewscrawlSpider(Spider):
    name = 'newsCrawl'
    start_urls = ['https://www.deccanchronicle.com/']
    allowed_domain = ['www.deccanchronicle.com']
    paths = [
    '#topStory > div.col-lg-4.col-md-4.col-sm-6.col-xs-12.feedCol.noPadding a',
    '#topStory > div.col-lg-8.col-md-8.col-sm-12.noPadding > div a',
    '#topStory > div.col-lg-4.col-md-4.col-sm-6.col-xs-12.feedCol.noPadding-xs a',
    '#fullBody > div.container.inBody > div.col-sm-12.noPadding.startBlock.SouthHome > div > div.col-sm-12.secColorHolder.secColorTab a',
    '#fullBody > div.container.inBody > div.col-sm-12.col-xs-12.noPadding.entBlock.imgShadow.startBlock.EntertainmentHome a',
    '.col-sm-12.secColorHolder a']
    summary = '.strap span'
    topic = '.color a'
    headings = '.mb-2'
    imagelink = '.coverimg'
    tags = '.articleTags a'
    date = '#fullBody > div.container.inBody > div.col-sm-8.noPadding > div.articlecontent > div > div.attribution > div > div.col-sm-5.col-xs-12.noPadding.noMargin'
    content = '#storyBody p'
    def parse(self, response):
        print("you are in 1")
        
        for path in self.paths:
            for url in response.css(path).css("::attr(href)").extract():
                if url is not None:
                    print(url)
                    req = Request(url= "https://www.deccanchronicle.com/" + url , callback= self.parse_article)
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



