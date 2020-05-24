## Guidelines for running the file - 

### 1. Open the folder and in terminal -> pip install -r requirements.txt

### 2. (Optional)Inside news_scraping folder, in settings.py file, uncomment USER_AGENT (line number 19)
### Google search -> my user agent and paste the user-agent in that USER_AGENT variable (User agent is used for smooth crawling and avoid getting blocked)

### 3. I have used MongoDB to store the data, thus run MongoDB on localhost and port - 27017 (default settings)

### 4. At the base folder directory crawlerservice/ in terminal, do the following steps to run the spider ->
#### a. cd news_scraping
#### b. scrapy crawl newsCrawl

### 5. Allow sometime for the spider to scrap the websites for all the links (about 5-6 mins)
