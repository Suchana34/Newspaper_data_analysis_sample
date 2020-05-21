#desription: this program scrapes and summarises news articles

import nltk
from newspaper import Article

# get the article by its link
url = 'https://www.hindustantimes.com/world-news/finally-china-gives-in-agrees-to-probe-covid-19-origin-who-response/story-gb3ZadVm3HrKnnCDiClaLP.html'
article = Article(url)

# do some nlp
article.download()
article.parse()
nltk.download('punkt')
article.nlp()

#get the authors of the article
print('author :', article.authors)

#get the published date
print('publish_date :', article.publish_date)

# get the top image
print('top-image-url :' , article.top_image)

#get the articles text
print('article-text :', article.text)

#get a summary of the article
print('summary :', article.summary)
