from bs4 import BeautifulSoup
import utils


def main():
    """
    Main entry to scrapping script
    """

    rows = []
    fields = ['city_name', 'lat', 'long']
    data_source_url = "https://en.wikipedia.org/wiki/List_of_ancient_Greek_cities"
    src_content = utils.get_source_content(data_source_url)

    soup = BeautifulSoup(src_content, 'lxml')

    # Get list of Greek City Links
    links = soup.select('#mw-content-text table.wikitable tr td:first-child a')

    print(links)
    for link in links:
        host_url = 'https://en.wikipedia.org'
        city_url = host_url + link.attrs['href']
        city_name = link.text
        city_coords = utils.get_city_coords(city_url)
        if city_coords:
            print("{}, {}, {}".format(city_name, utils.parse_lat(city_coords), utils.parse_long(city_coords)))
            rows.append([city_name, utils.parse_lat(city_coords), utils.parse_long(city_coords)])

    # Export scraped data
    utils.export_data('greek_cities.csv', fields, rows)


if __name__ == '__main__':
    main()
