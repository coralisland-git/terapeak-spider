# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TerapeakItem(scrapy.Item):
	# define the fields for your item here like:
	title = scrapy.Field()
	sold = scrapy.Field()
	format = scrapy.Field()
	start_price = scrapy.Field()
	end_price = scrapy.Field()
	total_bid = scrapy.Field()
	offered = scrapy.Field()
	end_date = scrapy.Field()
	url = scrapy.Field()
