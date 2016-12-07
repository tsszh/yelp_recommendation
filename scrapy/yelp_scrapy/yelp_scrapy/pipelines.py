# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class ReviewPipeline(object):
	def open_spider(self, spider):
		self.files = {}

	def close_spider(self, spider):
		for file in self.files:
			self.files[file].close()

	def process_item(self, item, spider):
		if not item['filepath'] in self.files:
			self.files[ item['filepath'] ] = \
				open('yelp_scrapy/data/%s.reviews.jl'%item['filepath'], 'a')
		line = json.dumps([
			item['userId'],
			item['userName'],
			item['rating'],
			item['business'],
			item['review']
		]) + "\n"
		self.files[ item['filepath'] ].write(line)
		return item
