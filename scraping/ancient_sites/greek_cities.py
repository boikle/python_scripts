import requests
from bs4 import BeautifulSoup


def getSourceContent(source_url):
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
    requested_data = requests.get(source_url)
    src = requested_data.content

    return src

def main():
    """
    Main entry to scrapping script
    """

    data_source_url = "https://en.wikipedia.org/wiki/List_of_ancient_Greek_cities"
    src_content = getSourceContent(data_source_url)

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
            print("{}, {}".format(city_name, city_coords))


def get_city_coords(city_url):
   coords = None
   city_source = getSourceContent(city_url)
   soup = BeautifulSoup(city_source, 'lxml')
   geodec = soup.find('span', class_='geo-dec')

   if geodec and geodec.text:
        coords = geodec.text

   return coords

if __name__ == '__main__':
    main()
