# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Review(scrapy.Item):
    user = scrapy.Field()
    rating = scrapy.Field()
    business = scrapy.Field()
    review = scrapy.Field()

class YelpScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
