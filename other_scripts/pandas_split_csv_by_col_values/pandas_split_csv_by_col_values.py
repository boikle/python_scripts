"""
Simple data processing script to break up a csv into multiple csv files based
on a specified column to split data on.
"""
import os
import pandas as pd

input_file = "input/input.csv"
split_col = "foobar"

# Check if input file exists
if os.path.isfile(input_file):
    input_file_basename = os.path.basename(input_file)[:-4]
else:
    raise Exception("Can't find specified input file")

# Check if output directory exists, and if it doesn't add it
if not os.path.isdir('./output'):
    os.mkdir('output')

# Create a Pandas data frame
df = pd.read_csv(input_file, index_col=None, encoding='utf-8')
unique_col_values = df[split_col].unique()

# Loop through unique column values to produce split csv files
for unique_value in unique_col_values:
    output_rows = df.loc[df[split_col] == unique_value]

    # Output split results
    output_rows.to_csv('output/{}_{}_{}.csv'.format(
        str(input_file_basename),
        str(split_col),
        str(unique_value)),
        index=False)
