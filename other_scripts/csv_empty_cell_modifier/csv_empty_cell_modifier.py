"""
Replace empty cells with replacement string.
"""
import pandas as pd
import csv
input_file = "input.csv"
output_file = "output.csv"
replacement = "foobar"

# Open and read input file
input_csv_file = open(input_file, 'r', encoding='utf8')
input_csv_reader = csv.reader(input_csv_file)

# Open and write to output file
output_csv_file = open(output_file, 'w', encoding='utf8')
output_csv_writer = csv.writer(output_csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

# Loop through csv rows
for row in input_csv_reader:
    # Replace empty cells with replacement string
    for i in range(len(row)):
        if row[i] == '':
            row[i] = replacement

    output_csv_writer.writerow(row)
