import pandas as pd 
import sys

def split_dataset(filename):


    if sys.argv[1][-3:] == ('txt'):
        df = pd.read_csv(filename, names=["link", 'page'])
        chunk_ranges = range(0, len(df.index), 100000) 
        for i in range(len(chunk_ranges) - 1):
            df.iloc[chunk_ranges[i]:chunk_ranges[i+1], :].to_csv(sys.argv[1][:-4] + "_" + str(i) + ".csv")

split_dataset(sys.argv[1])