import scrapy

class Pier21Spider(scrapy.Spider):
    name = 'pier21'

    start_urls = ['https://pier21.ca/research/immigration-records/ship-arrival-search']

    def parse(self, response):
        # Scrap ship arrival data
        for row in response.css('table tbody tr'):
            yield {
                'shipping_company': row.css('td.views-field-field-shipping-company::text').get(),
                'ship': row.css('td.views-field-field-ship::text').get(),
                'ports': row.css('td.views-field-field-ports-of-call::text').get(),
                'passengers': row.css('td.views-field-field-passengers::text').get(),
                'month': row.css('td.views-field-field-month::text').get(),
                'day': row.css('td.views-field-field-day::text').get(),
                'year': row.css('td.views-field-field-year::text').get()
            }

        # Follow pagination links
        for href in response.css('li.pager-next a::attr(href)'):
            yield response.follow(href, self.parse)
