"""
Drop rows with empty specified cells
"""
import pandas as pd
input_file = "input.csv"
output_file = "output.csv"
fields = ['latitude', 'longitude']

# Create a Pandas data frame
df = pd.read_csv(input_file, index_col=0, encoding='utf-8')

# Loop through fields that need to be not null
for field in fields:
    df = df[~df[field].isnull()]

# Output results
df.to_csv(output_file)
