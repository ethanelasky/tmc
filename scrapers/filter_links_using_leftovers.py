import pandas as pd
import re 
import sys

def extract_timestamp(url):
    """
    Extracts timestamp from the given URL.
    """
    match = re.search(r'/(\d+)-', url)
    return match.group(1) if match else None

def find_unscraped_urls(filename):
    """
    Identifies unscraped URLs by comparing a main links CSV against a leftovers CSV.
    Outputs a CSV file containing unscraped URLs.
    """
    links_df = pd.read_parquet(filename + ".parquet")
    leftovers_df = pd.read_csv(filename + "leftovers.csv", header=None, names=['url'])

    # Assuming the first column in links_df contains URLs, adjust as necessary
    links_df['timestamp'] = links_df.iloc[:, 0].apply(extract_timestamp)
    leftovers_df['timestamp'] = leftovers_df['url'].apply(extract_timestamp)

    # Identify unique timestamps in the links CSV
    unique_timestamps_links = set(links_df['timestamp'])

    # Identify timestamps not yet scraped (present in leftovers)
    timestamps_not_scraped = set(leftovers_df['timestamp'])

    # Filter the links_df to find URLs with timestamps that are not yet scraped
    unscraped_urls = links_df[links_df['timestamp'].isin(timestamps_not_scraped)]

    unscraped_urls.drop_duplicates(subset=['timestamp'])
    
    # Save the unscraped URLs to a CSV file
    unscraped_urls.to_parquet(filename + "leftovers.parquet")

# Example usage
find_unscraped_urls(sys.argv[1])