import scrapy
import json

from terapeak.items import TerapeakItem

from time import time
import datetime

class TerapeakSpider(scrapy.Spider):
	name = "terapeak"
	
	def __init__(self):
		self.total_number = 3000;
		
	# make a request for login
	def start_requests(self):
		data = '{"username": "bllee@miis.edu", "password": "dD4CO0OWnO1h"}'
		header = {
			"accept": "application/json",
			"Accept-Encoding": "gzip, deflate, br",
			"content-type": "application/json",
			"Host": "sell.terapeak.com",
			"Origin": "https://sell.terapeak.com",
			"Referer": "https://sell.terapeak.com/login/",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
			
		request = scrapy.Request("https://sell.terapeak.com/services/tokens",
						method = "POST",
						body = data,
						headers = header,
						callback=self.get_token, dont_filter=True)

		return [request]

	# get credential token and make request for getting products
	def get_token(self, response):
		credential = json.loads(response.body)
		
		if credential['success'] == True:
			token = credential['token']
			current_time = time() * 1000
			date_string = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d')
			
			url = "https://sell.terapeak.com/services/ebay/legacy/productresearch/itemresearch?token=%s&ulbrtabid=632085c9-3c1b-4561-948f-65fd9219dff6&ulpagename=eBayProductResearch&" % token
			
			header = {
				"Accept": "application/json, text/javascript, */*; q=0.01",
				"Accept-Encoding": "gzip, deflate, br",
				"Content-Type": "application/json",
				"Cookie": 'optimizelyEndUserId=oeu1471650850862r0.5160012859792553; tp_x8=61.2169599617418002-0e71143pt%2FXNFcYzkjaWQM830fID61rLH9tqpnlZTJviChg52VE7ywdSK4OBeAubsURPxomG%3D; tp_c7=1fMOTnC7D0M1OeIPEiQ5cikSJ9isLJYPuanSHY6FDrvju%2FA6glLDqFwo0vul0WNumjQsKYzQQbZzk1C%2BjkhzUQy%2FlTDe4aJKX69FgigSARPkhLtIwbLDrmDvUt6WRRWNou%2Bo5qv27v9QxrtwRtQMYlvcmNB4R7lBsIf%2FCzZyqgZZI2JLdPk1ZqHtzBbrniBH8cm7pCzEzL0nz0dfC3y6USXAYBsgugMwqPWwL5fHRUkWtc69%2B%2FXdVb4K5d8Z%2BvB6wPy3zet3ZzqZ9EkReW3W%2F5ZOwcFvBFlxQK5F5ve7QEz1nfFvzxvU4GnpKfX2E5nKwOVAZvmE%2FVNL3Aixq26ibZ3I2QUDPnPXPw%2FJWybErZ%2FoSTyVdqhJ%2BCs6ATBCSWXlGvESlDN%2BNXMQGoZs0YVNlXQCOhmxGq6STbX%2FjhZ1HFI%3D1d79509b742c20ffa3bf68999aa90f7097bf462f; lastUrl=https://sell.terapeak.com/; __utmt=1; token=' + str(token) + '; tokenExpiry=1503190445983; ki_t=1471650855829%3B1471650855829%3B1471654542699%3B1%3B24; ki_r=; optimizelySegments=%7B%22229813889%22%3A%22gc%22%2C%22229833781%22%3A%22referral%22%2C%22229852304%22%3A%22false%22%7D; optimizelyBuckets=%7B%223138480291%22%3A%223143150124%22%2C%223386134531%22%3A%223408741298%22%2C%226456040624%22%3A%226450293330%22%7D; userRole=PHOENIX_PROFESSIONAL; __utma=195498537.251309087.1471650851.1471650851.1471650851.1; __utmb=195498537.35.10.1471650851; __utmc=195498537; __utmz=195498537.1471650851.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); currency=USD; tpebayCurrencyId=1; i18next=en-US; optimizelyPendingLogEvents=%5B%5D; totango.heartbeat.last_module=__system; totango.heartbeat.last_ts=' + str(current_time) + '; localeHeader=en-US,en',
				"Host": "sell.terapeak.com",
				"Origin": "https://sell.terapeak.com",
				"Referer": "https://sell.terapeak.com/?page=eBayProductResearch",
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
				"X-Requested-With": "XMLHttpRequest"
			}
			
			data = '{ \
				"currency": "1", \
				"date": "' + date_string + '", \
				"date_range": 7, \
				"id": "0", \
				"limit": 200, \
				"offset":0, \
				"order": "end_price", \
				"orderDir": "desc", \
				"query": "vacuum pump", \
				"siteID": "0" \
			}'
			
			request = scrapy.Request(url,
						method = "POST",
						body = data,
						headers = header,
						callback=self.parse_products, dont_filter=True)
						
			request.meta['offset'] = 0
			request.meta['token'] = token
			request.meta['current_time'] = current_time
						
			yield request
				
	# parse product data with josn format.
	def parse_products(self, response):
		offset = response.meta['offset']
		token = response.meta['token']
		current_time = response.meta['current_time']
		date_string = datetime.datetime.fromtimestamp(current_time/1000).strftime('%Y-%m-%d')
		
		products = json.loads(response.body)
		products = products['productResearch_itemBrowse']
		
		# iterate a product and save it into csv file
		for product in products:
			item = TerapeakItem()
			item['title'] = product['item_title']
			item['sold'] = product['sold']
			item['format'] = product['format']
			item['start_price'] = product['start_price']
			item['end_price'] = product['end_price']
			item['total_bid'] = product['items_sold']
			item['offered'] = product['items_offered']
			item['end_date'] = datetime.datetime.fromtimestamp(product['end_date']/1000 + 24 * 60 * 60).strftime('%Y-%m-%d')
			item['url'] = product['view_item_url']
			
			yield item
		
		# if the number of products reaches to the total number of products that should be scraped, exit the spider
		if offset >= self.total_number:
			return
			
		offset += 200
		url = "https://sell.terapeak.com/services/ebay/legacy/productresearch/itemresearch?token=%s&ulbrtabid=632085c9-3c1b-4561-948f-65fd9219dff6&ulpagename=eBayProductResearch&" % token
			
		header = {
			"Accept": "application/json, text/javascript, */*; q=0.01",
			"Accept-Encoding": "gzip, deflate, br",
			"Content-Type": "application/json",
			"Cookie": 'optimizelyEndUserId=oeu1471650850862r0.5160012859792553; tp_x8=61.2169599617418002-0e71143pt%2FXNFcYzkjaWQM830fID61rLH9tqpnlZTJviChg52VE7ywdSK4OBeAubsURPxomG%3D; tp_c7=1fMOTnC7D0M1OeIPEiQ5cikSJ9isLJYPuanSHY6FDrvju%2FA6glLDqFwo0vul0WNumjQsKYzQQbZzk1C%2BjkhzUQy%2FlTDe4aJKX69FgigSARPkhLtIwbLDrmDvUt6WRRWNou%2Bo5qv27v9QxrtwRtQMYlvcmNB4R7lBsIf%2FCzZyqgZZI2JLdPk1ZqHtzBbrniBH8cm7pCzEzL0nz0dfC3y6USXAYBsgugMwqPWwL5fHRUkWtc69%2B%2FXdVb4K5d8Z%2BvB6wPy3zet3ZzqZ9EkReW3W%2F5ZOwcFvBFlxQK5F5ve7QEz1nfFvzxvU4GnpKfX2E5nKwOVAZvmE%2FVNL3Aixq26ibZ3I2QUDPnPXPw%2FJWybErZ%2FoSTyVdqhJ%2BCs6ATBCSWXlGvESlDN%2BNXMQGoZs0YVNlXQCOhmxGq6STbX%2FjhZ1HFI%3D1d79509b742c20ffa3bf68999aa90f7097bf462f; lastUrl=https://sell.terapeak.com/; __utmt=1; token=' + str(token) + '; tokenExpiry=1503190445983; ki_t=1471650855829%3B1471650855829%3B1471654542699%3B1%3B24; ki_r=; optimizelySegments=%7B%22229813889%22%3A%22gc%22%2C%22229833781%22%3A%22referral%22%2C%22229852304%22%3A%22false%22%7D; optimizelyBuckets=%7B%223138480291%22%3A%223143150124%22%2C%223386134531%22%3A%223408741298%22%2C%226456040624%22%3A%226450293330%22%7D; userRole=PHOENIX_PROFESSIONAL; __utma=195498537.251309087.1471650851.1471650851.1471650851.1; __utmb=195498537.35.10.1471650851; __utmc=195498537; __utmz=195498537.1471650851.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); currency=USD; tpebayCurrencyId=1; i18next=en-US; optimizelyPendingLogEvents=%5B%5D; totango.heartbeat.last_module=__system; totango.heartbeat.last_ts=' + str(current_time) + '; localeHeader=en-US,en',
			"Host": "sell.terapeak.com",
			"Origin": "https://sell.terapeak.com",
			"Referer": "https://sell.terapeak.com/?page=eBayProductResearch",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
			"X-Requested-With": "XMLHttpRequest"
		}
		
		data = '{ \
			"currency": "1", \
			"date": "' + date_string + '", \
			"date_range": 7, \
			"id": "0", \
			"limit": 200, \
			"offset":' + str(offset) + ', \
			"order": "end_price", \
			"orderDir": "desc", \
			"query": "vacuum pump", \
			"siteID": "0" \
		}'
		
		request = scrapy.Request(url,
					method = "POST",
					body = data,
					headers = header,
					callback=self.parse_products, dont_filter=True)
					
		request.meta['offset'] = offset
		request.meta['token'] = token		
		request.meta['current_time'] = current_time

		yield request
		
		'''filename = response.url.split("/")[-2] + '.html'
		with open(filename, 'wb') as f:
			f.write(response.body)'''