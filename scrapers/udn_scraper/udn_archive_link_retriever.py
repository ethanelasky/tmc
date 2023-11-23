import pandas as pd
import requests
import time

def scrape_urls_from_sitemap(start_page, delay=5.0):
        
    archive_url = "http://web.archive.org/cdx/search/cdx?url=udn.com*&from=2013&to=2023&filter=statuscode:200&output=json&filter=mimetype:text/html&collapse=original"
    num_pages = int(requests.get(archive_url + "&showNumPages=true").text)

    links = []
    for i in range(start_page, num_pages):
        df = pd.read_json(archive_url + "&page=" + str(i))
        df.to_csv("udn_article_links.csv", mode='a')
        print("Scraped page {i} of {num_pages} of Archive.org's UDN archives.")
        time.sleep(60)

    return i


# The delay in seconds between requests
request_delay = 5.0  # Adjust this value as needed

# Run the scraping function with the delay
num_links = scrape_urls_from_sitemap(0, request_delay)

# The URLs have been saved to '/mnt/data/urls.txt'
print(f"Saved {num_links} URLs to file.")