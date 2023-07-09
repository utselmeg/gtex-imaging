import glob
import os
import pandas as pd
import numpy as np

# list to save results
results = []

# get all txt files
files = glob.glob("*.txt")

# for each file
for file in files:
    # load data in chunks
    chunks = pd.read_csv(file, sep="\t", chunksize=1000)
    
    # dictionary to count range frequency
    ranges = {}
    
    for chunk in chunks:
        # select nucleus related columns
        nucleus_columns = chunk.columns[chunk.columns.str.startswith('Nucleus')]
        nucleus_data = chunk[nucleus_columns]
        
        # calculate ranges and their frequency
        for column in nucleus_data.columns:
            # round to the nearest 10 to define range
            rounded_values = np.round(nucleus_data[column]/10)*10
            value_counts = rounded_values.value_counts()
            for range_start, count in value_counts.items():
                range_str = f'{int(range_start)}-{int(range_start+10)}'
                if range_str not in ranges:
                    ranges[range_str] = count
                else:
                    ranges[range_str] += count

    # get most frequent range
    most_frequent_range = max(ranges, key=ranges.get)
    most_frequent_count = ranges[most_frequent_range]

    # append result
    results.append([os.path.splitext(file)[0], most_frequent_range, most_frequent_count])

# create dataframe
df = pd.DataFrame(results, columns=['Image Name', 'Most_Frequent_Range', 'Count'])

# save to csv
df.to_csv('results.csv', index=False)
