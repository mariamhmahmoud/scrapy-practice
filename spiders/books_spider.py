import scrapy

class BooksSpider(scrapy.Spider):
	name = "books"
	start_urls = [
		'http://books.toscrape.com/'
	]

	def parse(self, response):
		for book_info in response.css('li .product_pod'):
			yield {
				'book_title': book_info.css('h3 a::text').get(),
		    	'book_price': book_info.css('.product_price p::text').get(),
		    	'book_rating': book_info.xpath('.//p[contains(@class, "star-rating")]/@class').re(r'star-rating(.*)$')
			}
		next_page = response.css('.next a::attr(href)').get()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback = self.parse)