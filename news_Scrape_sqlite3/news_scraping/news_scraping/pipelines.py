# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class NewsScrapingPipeline:
        
    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("newspaper.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS news_tb""")
        self.curr.execute("""create table news_tb(
            news_title text,
            news_text text,
            news_link text,
            keywords text
        )""")


    def process_item(self, item, spider):
        self.table_data(item)
        return item

    def table_data(self,item):
        words = ""
        for i in item['keywords']:
            words = words + i + ","

        self.curr.execute(""" insert into news_tb values (?,?,?,?)""",
        (
            item['title'][0],
            item['text'][0],
            item['link'][0],
            words
        ))

        self.conn.commit()

