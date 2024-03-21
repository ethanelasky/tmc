import os
import pandas as pd
import sys

def write_to_html(row):
    with open(os.path.join(csv_name[:-4], str(row.name)) + ".html", 'w') as f:
        f.write(row['html'])

csv_name = sys.argv[1]
reader = pd.read_csv(csv_name, chunksize=100)
if not os.path.exists(csv_name[:-4]):
    os.mkdir(csv_name[:-4])

i = 0
for chunk in reader:
    chunk.apply(write_to_html, axis=1)
    print("Wrote chunk", i)
    i += 1
