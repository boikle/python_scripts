'''
Simple line graph which plots weight change over time.
'''

import matplotlib.pyplot as plt
import pandas as pd

# Load data
df = pd.read_csv('./data.csv', parse_dates=True)

# Create graph with loaded data
df.plot(x='date', y='lbs', kind='line')

# Set the X and Y graph labels
plt.xlabel('Date')
plt.ylabel('Weight (lbs)')

# Add a title for graph
plt.title("Weight Change")

# Show the plot
plt.show()
