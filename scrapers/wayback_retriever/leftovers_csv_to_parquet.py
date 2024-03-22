import pandas as pd
import re
import sys

df = pd.read_csv(sys.argv[1], names=["directory_name", "link"])
df['directory_name'] = df['directory_name'].str.extract("(?:/)(\\d+)").astype(int)
df = df.set_index('directory_name').rename_axis(index=None)
new_name = re.search("([A-Za-z0-9_]+)(?:\\.)", sys.argv[1])[0]
df.to_parquet(new_name + "parquet")