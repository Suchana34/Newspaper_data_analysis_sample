import feedparser as fp
from newspaper import Article
import newspaper
from time import mktime
from datetime import datetime
import json

content = Article('http://prayukti.net/pso-rite-review-discount-code-is-it-worth-buying/')
print("Downloading articles from")
newsPaper = {
    "articles": []
}
article = {}
article['link'] = content.url

try:
    content.download()
    content.parse()
except Exception as e:
    print(e)
    print("continuing...")

article['title'] = content.title
article['text'] = content.text
newsPaper['articles'].append(article)
print("Downloaded")
try:
    with open('scraped_articles.json', 'w') as outfile:
        json.dump(newsPaper, outfile)
except Exception as e: print(e)


