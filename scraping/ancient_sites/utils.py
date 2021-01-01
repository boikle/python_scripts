import csv
import os


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

    with open('output/' + file_name, 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)