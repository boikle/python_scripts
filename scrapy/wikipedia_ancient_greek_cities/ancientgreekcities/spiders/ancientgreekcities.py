import scrapy

class QuotesSpider(scrapy.Spider):
    # Name of the spider
    name = "ancientgreekcities"

    # URL to scrape
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_ancient_Greek_cities'
    ]

    def parse_city(self, response):
        # Extract the city name, lat, long
        for quote in response.css('table.infobox.geography.vcard'):
            yield {
                'name': quote.css('div.fn.org::text').get(),
                'latitude': quote.css('span.latitude::text').get(),
                'longitude': quote.css('span.longitude::text').get(),
            }

    def parse(self, response):
        # follow links to ancient city pages
        for href in response.css('table.wikitable tr td:nth-child(1) a::attr(href)'):
            yield response.follow(href, self.parse_city)

