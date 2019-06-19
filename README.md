# scrapyProject
Scrapping the news website BBC.com using Scrapy framework & newspaper.

1. Crawls BBC.com for articles.
2. Collects Author,Date, Article, Headlines.
3. REST for querying basic operations.
4. Unittests

To run MongoDb in Docker.
sudo docker run --name bbcmongo -d -p 27017:27017 -v ~/data:/data/db mongo

To rerun.
sudo  docker rm bbcmongo
