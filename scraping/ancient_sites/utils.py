import csv
import os


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
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)