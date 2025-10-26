import json

import scrapy
from itemadapter import ItemAdapter
from mongoengine import DoesNotExist
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field
from mongoengine.errors import NotUniqueError

from models import Author, Quote

class DataPipeline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if "fullname" in adapter.keys():
            self.authors.append(dict(adapter))
        if "quote" in adapter.keys():
            self.quotes.append(dict(adapter))

    def close_spider(self, spider):
        with open("quotes.json", "w", encoding="utf-8") as fd:
            json.dump(self.quotes, fd, ensure_ascii=False, indent=2)
        with open("authors.json", "w", encoding="utf-8") as fd:
            json.dump(self.authors, fd, ensure_ascii=False, indent=2)

class QuoteItem(Item):
    quote = Field()
    author = Field()
    tags = Field()


class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class QuotesSpider(scrapy.Spider):
    name = "get_quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]
    custom_settings = {"ITEM_PIPELINES" : {DataPipeline: 300}}

    def parse(self, response, **kwargs):
        for q in response.xpath("/html//div[@class='quote']"):
            quote = q.xpath(".//span[@class='text']/text()").get().strip()
            author = q.xpath(".//span/small[@class='author']/text()").get().strip()
            tags = q.xpath(".//div[@class='tags']/a/text()").extract()
            # TODO: clear tags
            yield QuoteItem(quote=quote, author=author, tags=tags)
            yield response.follow(url=self.start_urls[0] + q.xpath("span/a/@href").get(), callback=self.parse_author)

        next_link = response.xpath("/html//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)
    @classmethod
    def parse_author(cls, response, **kwargs):
        content = response.xpath("/html//div[@class='author-details']")
        fullname = content.xpath("h3[@class='author-title']/text()").get().strip()
        born_date = content.xpath("p/span[@class='author-born-date']/text()").get().strip()
        born_location = content.xpath("p/span[@class='author-born-location']/text()").get().strip()
        description = content.xpath("div[@class='author-description']/text()").get().strip()
        yield AuthorItem(fullname=fullname, born_date=born_date, born_location=born_location, description=description)



if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
    with open('authors.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author(fullname=el.get('fullname'), born_date=el.get('born_date'),
                                born_location=el.get('born_location'), description=el.get('description'))
                author.save()
            except NotUniqueError as err:
                print("Author already exists")

    with open('quotes.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author.objects.get(fullname=el.get('author'))
            except DoesNotExist:
                sep_names = el.get('author').split(' ')
                last_name = '-'.join(sep_names[1:3])
                fullname = f"{sep_names[0]} {last_name}"
                author = Author.objects.get(fullname=fullname)
            quote = Quote(quote=el.get('quote'), tags=el.get('tags'), author=author)
            quote.save()
