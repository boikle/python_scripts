import csv
import os
import requests
from bs4 import BeautifulSoup


def get_source_content(source_url):
    """
    Get the HTML content for the provided source URL

    Attributes:
    ---------------
    source_url: string
        The URL for the website being requested

    Returns:
    ---------------
    src: bytes literal
        A string containing the html content for the provided source
    """
    src = None
    try:
        requested_data = requests.get(source_url, timeout=1000)
        src = requested_data.content
    except requests.exceptions.ConnectionError:
        print("Connection refused")

    return src


def get_founding_date(city_url):
    """
    Get the founding date for city

    Attributes:
    ---------------
    city_url: string
        The URL for the website being requested

    Returns:
    ---------------
    foundation_date: string
        A string containing the founding date of the city
    """
    foundation_date = None
    city_source = get_source_content(city_url)
    if city_source:
        source = BeautifulSoup(city_source, 'lxml')
        vertical_card = source.find('table', class_='vcard')

        if vertical_card:
            # Find Rows in Table
            rows = vertical_card.find_all('tr')
            for row in rows:
                row_header = row.find('th')

                if row_header:
                    if row_header.text and row_header.text == "Founded":
                        row_value = row.find('td')
                        foundation_date = row_value.text
                    else:
                        row_header_link = row_header.find('a')
                        if row_header_link and row_header_link.text and row_header_link.text == "Foundation":
                            row_value = row.find('td')
                            foundation_date = row_value.text

        return foundation_date


def get_city_coords(city_url):
    """
    Get city coordinates string from wikipedia page

    Attributes:
    ---------------
    city_url: string
        The URL for the website being requested

    Returns:
    ---------------
    coords: string
        A string containing the Lat/Long coordinates
    """
    coords = None
    city_source = get_source_content(city_url)
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

    Attributes:
    ---------------
    coords: string
        The lat/long coordinate string

    Returns:
    ---------------
    lat: string
        A string containing the decimal degree latitude number
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

    Attributes:
    ---------------
    coords: string
        The lat/long coordinate string

    Returns:
    ---------------
    long: string
        A string containing the decimal degree latitude number
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


def export_data(file_name, fields, rows):
    """
    Export scrapped data

    Attributes:
    --------------------
    file_name: str
        file name of the exported data
    fields: list
        list of field names
    rows: list
        list of lists containing row values
    """

    # Create output directory if it doesn't exist
    if not os.path.exists('output/'):
        os.mkdir('output')

    # Delete old output file if it exists
    if os.path.exists('output/' + file_name):
        os.remove('output/' + file_name)

    with open('output/' + file_name, 'w') as f:
        write = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        write.writerow(fields)
        write.writerows(rows)
