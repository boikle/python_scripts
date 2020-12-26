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
    data_source_url = "https://en.wikipedia.org/wiki/Category:Roman_towns_and_cities_by_country"
    source_content = getSourceContent(data_source_url)



if __name__ == '__main__':
    main()
