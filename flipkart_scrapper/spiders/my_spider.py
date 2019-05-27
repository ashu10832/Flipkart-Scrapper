import scrapy


class MySpider(scrapy.Spider):

	name = 'my_spider'

	def start_requests(self):

		urls = ["https://www.flipkart.com/search?q=%s" % self.category
		]

		for url in urls:
			request =  scrapy.Request(url = url,callback = self.parse)
			request.meta['page'] = 1
			yield request

	def parse(self,response):


		mobiles = response.css("div._1UoZlX")

		for mobile in mobiles:

			title = mobile.css("div._3wU53n::text").get()
			price = mobile.css("div._1vC4OE::text").get()
			rating = mobile.css("div.hGSR34::text").get()
			price = price[1:]

			yield {
				"title":title,
				"price":price,
				"rating":rating,
			}

		page_num = response.meta['page']
		if(page_num<=9):

			next_page_selector = response.css("a._3fVaIS")
			if len(next_page_selector) == 1:
				next_page_id = next_page_selector[0].css("a::attr(href)").get()
			else:
				next_page_id = next_page_selector[1].css("a::attr(href)").get()
			if(next_page_id is not None):
				next_page = response.urljoin(next_page_id)
				request =  scrapy.Request(url = next_page,callback = self.parse)
				request.meta['page'] = page_num+1
				yield request

		




