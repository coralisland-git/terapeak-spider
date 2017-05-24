# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TerapeakPipeline(object):
	def open_spider(self, spider):
		# open csv file
		self.fp = open("data.csv", "wb")

		# write header in csv file
		self.fp.write('"Item Title","Sold","Format","Start Price","End Price","Total Bids","Item Offered","End Date","Item Url"\n')

	def close_spider(self, spider):
		self.fp.close()

	def process_item(self, item, spider):
		line = '"%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' % \
					(self.filter(item['title']), item['sold'], item['format'],\
					str(item['start_price']), str(item['end_price']), str(item['total_bid']), str(item['offered']),item['end_date'], item['url'])

		# encode data string with utf8 and save it into file
		self.fp.write(line.encode("utf8"))

		return item

	def filter(self, raw_str):

		res = raw_str.replace(",", " ")
		res = res.replace("\"", " ")

		return res