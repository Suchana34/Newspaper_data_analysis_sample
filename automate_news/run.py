import feedparser as fp
from newspaper import Article
import newspaper
from time import mktime
from datetime import datetime
import json

LIMIT = 4


with open('newspapers.json') as data_file:
    news = json.load(data_file)

count = 1

for key,value in news.items():
    if 'rss' in value:
        d = fp.parse(value['rss'])
        print("Downloading articles from ", key)
        newsPaper = {
            "rss" : value['rss'],
            "link" : value['link'],
            "articles": []
        }
        for entry in d.entries:
            if hasattr(entry, 'published'):
                if count>LIMIT:
                    break
                article = {}
                article['link'] = entry.link
                date = entry.published_parsed
                article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()

                try:
                    content = Article(entry.link)
                    content.download()
                    content.parse()
                except Exception as e:
                    print(e)
                    print("continuing...")
                    continue
                article['title'] = content.title
                article['text'] = content.text
                newsPaper['articles'].append(article)
                print(count, "articles downloaded from", key, ", url: ", entry.link)
                count = count + 1
    else:
        print("building site for company", key)
        content = Article(value['link'])
        content.download()
        content.parse()
        newsPaper = {
            "link": value['link'],
            "articles": []
        }
        article = {}
        article['title'] = content.title
        article['link'] = content.url
        article['text'] = content.text
        newsPaper['articles'].append(article)
        print(count, "articles downloaded from", key, ", url: ", content.url)
        count = count + 1

try:
    with open('scraped_articles.json', 'w') as outfile:
        json.dump(newsPaper, outfile)
except Exception as e: print(e)


