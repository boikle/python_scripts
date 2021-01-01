import requests
from bs4 import BeautifulSoup
import utils


def get_city_coords(city_url):
    """
    Get city coordinates string from wikipedia page
    """
    coords = None
    city_source = utils.get_source_content(city_url)
    if city_source:
        soup = BeautifulSoup(city_source, 'lxml')
        geodec = soup.find('span', class_='geo-dec')

        if geodec and geodec.text:
            coords = geodec.text

    return coords


def parse_lat(coords):
    """
    Parse lat/long string to retrieve latitude number in decimal degree format

    Example: 40.2°N 35.5°E  returns 40.2
    """
    lat = None

    if coords.find("°N") != -1:
        lat_index = coords.index("°N")
        lat = float(coords[:lat_index])
    elif coords.find("°S") != -1:
        lat_index = coords.index("°S")
        lat = float(coords[:lat_index]) * -1

    return lat


def parse_long(coords):
    """
    Parse lat/long string to retrieve longitude number in decimal degree format
    
    Example: 40.2°N 35.5°E  returns 35.5
    """
    long = None
    coords = coords.split()

    if len(coords) == 2:
        coords = coords[1]
        if coords.find("°E") != -1:
            long_index = coords.index("°E")
            long = float(coords[:long_index])
        elif coords.find("°W") != -1:
            long_index = coords.index("°W")
            long = float(coords[:long_index]) * -1

    return long


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
        city_coords = get_city_coords(city_url)
        if city_coords:
            print("{}, {}, {}".format(city_name, parse_lat(city_coords), parse_long(city_coords)))
            rows.append([city_name, parse_lat(city_coords), parse_long(city_coords)])

    # Export scraped data
    utils.export_data('greek_cities.csv', fields, rows)


if __name__ == '__main__':
    main()
