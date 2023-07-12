"""
Convert the output of the QuPath script 'Export cell and nucleus measurements' to a CSV file.
"""
import glob
import pandas as pd
from IPython.display import display

nucleus_columns = [
    "Nucleus: Area", "Nucleus: Perimeter", "Nucleus: Circularity",
    "Nucleus: Max caliper", "Nucleus: Min caliper", "Nucleus: Eccentricity",
    "Nucleus: Hematoxylin OD mean", "Nucleus: Hematoxylin OD sum",
    "Nucleus: Hematoxylin OD std dev", "Nucleus: Hematoxylin OD max",
    "Nucleus: Hematoxylin OD min", "Nucleus: Hematoxylin OD range",
    "Nucleus: Eosin OD mean", "Nucleus: Eosin OD sum", "Nucleus: Eosin OD std dev",
    "Nucleus: Eosin OD max", "Nucleus: Eosin OD min", "Nucleus: Eosin OD range",
    "Cell: Area", "Cell: Perimeter", "Cell: Circularity", "Cell: Max caliper",
    "Cell: Min caliper", "Cell: Eccentricity", "Cell: Hematoxylin OD mean",
    "Cell: Hematoxylin OD std dev", "Cell: Hematoxylin OD max", "Cell: Hematoxylin OD min",
    "Cell: Eosin OD mean", "Cell: Eosin OD std dev", "Cell: Eosin OD max", "Cell: Eosin OD min",
    "Cytoplasm: Hematoxylin OD mean", "Cytoplasm: Hematoxylin OD std dev", 
    "Cytoplasm: Hematoxylin OD max", "Cytoplasm: Hematoxylin OD min", "Cytoplasm: Eosin OD mean", 
    "Cytoplasm: Eosin OD std dev", "Cytoplasm: Eosin OD max", "Cytoplasm: Eosin OD min", 
    "Nucleus/Cell area ratio"
    ]

results = []

files = glob.glob("*.txt")

results = []

for file in files:
    df = pd.read_csv(file, sep="\t")

    for column in nucleus_columns:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in file: {file}")

    column_edges = []
    for column in nucleus_columns:
        bins = pd.cut(df[column], bins=16)
        bin_counts = bins.value_counts().sort_index()

        max_count_bin = bin_counts.idxmax()

        left_edge = max_count_bin.left
        right_edge = max_count_bin.right

        column_edges.extend([left_edge, right_edge])

    results.append([df["Image"].iloc[0]] + column_edges)

df = pd.DataFrame(results, columns=['Image'] +
                  [f for sublist in [(f'{col} Left Edge',
                                      f'{col} Right Edge') 
                                     for col in nucleus_columns] for f in sublist])

display(df)

df.to_csv('results.csv', index=False)

df = pd.read_csv('results.csv')

display(df)
