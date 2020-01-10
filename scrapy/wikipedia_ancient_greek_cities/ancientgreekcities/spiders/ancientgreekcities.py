import scrapy

class QuotesSpider(scrapy.Spider):
    # Name of the spider
    name = "ancientgreekcities"

    # URL to scrape
    start_urls = [
        'https://en.wikipedia.org/wiki/List_of_ancient_Greek_cities'
    ]

    def parse_coords(self, response):
        # Extract the latitude and Longitude
        for quote in response.css('table span.geo'):
            yield {
                'latitude': quote.css('span.latitude::text').get(),
                'longitude': quote.css('span.longitude::text').get()
            }


    def parse_city(self, response):
        # Extract the city name
        for table in response.css('table.infobox.geography.vcard'):
            yield {
                'name': table.css('div.fn.org::text').get()
            }

        for href in response.css('span#coordinates span a::attr(href)'):
            yield response.follow(href, self.parse_coords)

    def parse(self, response):
        # follow links to ancient city pages
        for href in response.css('table.wikitable tr td:nth-child(1) a::attr(href)'):
            yield response.follow(href, self.parse_city)

