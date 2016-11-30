# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class ReviewPipeline(object):
	def open_spider(self, spider):
		self.file = open('yelp_scrapy/data/data.jl', 'w')

	def close_spider(self, spider):
		self.file.close()

	def process_item(self, item, spider):
		line = json.dumps([
			item['user'],
			item['rating'],
			item['business'],
			item['review']
		]) + "\n"
		self.file.write(line)
		return item
