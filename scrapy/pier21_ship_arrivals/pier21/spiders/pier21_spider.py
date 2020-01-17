import scrapy

class Pier21Spider(scrapy.Spider):
    """Scrapy spider for scraping Pier 21 ship arrival data"""
    name = 'pier21'

    start_urls = ['https://pier21.ca/research/immigration-records/ship-arrival-search']

    def process_string(self, parsedstr):
        """Strip all extra white space and newline characters from parsed content"""
        return " ".join(parsedstr.split())

    def parse(self, response):
        """Parse content for ship arrival data"""
        for row in response.css('table tbody tr'):
            shipping_company = row.css('td.views-field-field-shipping-company::text').get()
            ship = row.css('td.views-field-field-ship::text').get()
            ports = row.css('td.views-field-field-ports-of-call::text').get()
            passengers = row.css('td.views-field-field-passengers::text').get()
            year = row.css('td.views-field-field-year::text').get()
            month = row.css('td.views-field-field-month::text').get()
            day = row.css('td.views-field-field-day::text').get()

            yield {
                'shipping_company': self.process_string(shipping_company),
                'ship': self.process_string(ship),
                'ports': self.process_string(ports),
                'passengers': self.process_string(passengers),
                'year': self.process_string(year),
                'month': self.process_string(month),
                'day': self.process_string(day)
            }

        # Follow pagination links
        for href in response.css('li.pager-next a::attr(href)'):
            yield response.follow(href, self.parse)
