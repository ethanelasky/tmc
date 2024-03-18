import numpy as np
import pandas as pd 
import sys

def split_dataset(filename):


    if filename[-3:] == ('txt'):
        df = pd.read_csv(filename, names=["link", 'page'])
        dfs = np.array_split(df, 6)
        for i in range(len(dfs)):
            dfs[i].to_parquet(sys.argv[1][:-4] + "_" + str(i) + ".parquet")

    if filename[-7:] == ('parquet'):
        df = pd.read_parquet(filename)

        dfs = np.array_split(df, 6)
        for i in range(len(dfs)):
            dfs[i].to_parquet(filename[:-8] + "_" + str(i) + ".parquet")
        # chunk_ranges = list(range(0, len(df.index), (len(df.index) - 1)//5))
        # chunk_ranges.append(len(df.index))
        # print(chunk_ranges)
        # for i in range(len(chunk_ranges) - 1):
        #     df.iloc[chunk_ranges[i]:chunk_ranges[i+1], :].to_parquet(sys.argv[1][:-8] + "_" + str(i) + ".parquet")

split_dataset(sys.argv[1])