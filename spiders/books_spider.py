import scrapy
from ..items import ScrapePracticeItem

class BooksSpider(scrapy.Spider):
	name = "books"
	start_urls = [
		'http://books.toscrape.com/'
	]

	def parse(self, response):

		for book in response.css('li .product_pod'):
			items = ScrapePracticeItem()

			title = book.css('h3 a::text').get()
			price = book.css('.product_price p::text').get()
			rating = str(book.xpath('.//p[contains(@class, "star-rating")]/@class').re(r'star-rating(.*)$'))

			items['price'] = price 
			items['rating'] = rating

			subpage = book.css('h3 a::attr(href)').get()
			subpage = response.urljoin(subpage)

			request = scrapy.Request(subpage, callback=self.scrapeTitle)
			request.meta['items'] = items

			yield request

		next_page = response.css('.next a::attr(href)').get()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback = self.parse)


	
	def scrapeTitle(self, response):
		items = response.meta['items']
		items['title'] = response.css('h1::text').get()
		yield items