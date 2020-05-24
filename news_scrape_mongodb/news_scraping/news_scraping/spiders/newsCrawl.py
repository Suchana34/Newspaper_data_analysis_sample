# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy.loader import ItemLoader
import newspaper
from newspaper import Article
from news_scraping.items import NewsScrapingItem

class NewscrawlSpider(Spider):
    name = 'newsCrawl'
    start_urls = ['https://en.wikipedia.org/wiki/List_of_newspapers_in_India']
    
    def parse(self, response):
        # go to each newspaper link in the table
        #print("you are in 1")
        for url in response.css("i a").css("::attr('href')").extract():

            yield Request(url='https://en.wikipedia.org/'+url , callback= self.parse_article)
    
    def parse_article(self,response):
        #print("you are in 3")
        ext_url = response.css(".url .text").css("::attr('href')").extract_first()
        if(ext_url is not None):
            
            l = ItemLoader(item = NewsScrapingItem(), response=response)
            url = ext_url
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()

            title = article.title
            text = article.text
            keywords = article.keywords

            l.add_value('title', title)
            l.add_value('link', url)
            l.add_value('text', text)
            l.add_value('keywords', keywords)


            yield l.load_item()



