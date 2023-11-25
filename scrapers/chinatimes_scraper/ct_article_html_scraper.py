"""
Scrapes text from articles on the China Times' online newspaper website. 
See the docstring of scrape_text_from_page for more info. 

Usage: python ct_article_scraper.py [path_to_urls] [output_file_name]

Ex: python ct_article_scraper.py ct_2013_links.json 
                                    ct_2013_article_contents.csv
"""

import asyncio
import pandas as pd
from playwright.async_api import async_playwright
import sys

async def scrape_html(index_url_pairs, delay=5.0):
    """ 
    Scrapes article HTML from webpages given a list of URLs.
    
    Inputs: 
    - A list of URLs (as strings)
    - delay: minimum time between requests (to avoid IP bans / overthrottling)

    Outputs:
    - HTML files that each represent one article. 
    """

    path_to_extension = "./uBlock"
    user_data_dir = "/tmp/test-user-data-dir"
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,
        user_agent=ua,
        args=[
            "--headless=new",
            f"--disable-extensions-except={path_to_extension}",
            f"--load-extension={path_to_extension}",
        ],
        )

        page = await browser.new_page()
        page.set_default_navigation_timeout(60000)

        for i in range(len(index_url_pairs)):
            pair = index_url_pairs[i]
            index = pair[0]
            url = pair[1]
            print(url)
            while True:
                try:
                    await page.goto(url)      
                except:
                    await asyncio.sleep(delay * 3)
                    continue
                break

            title = await page.locator('css=.article-title').inner_text()
            contents = await page.content()
            with open("/output/" + str(index) + ".html", 'w', encoding="utf-8") as f:
                f.write(contents)
                print(f"Wrote {title} to file.")

            await asyncio.sleep(delay)

        await browser.close()
    

# The delay in seconds between requests
request_delay = 3.0 

df = pd.read_csv(sys.argv[1], index_col=0)
indices = df.index
links = df['link'].values
index_url_pairs = list(zip(indices, links))

# with open(sys.argv[1]) as f:
#     urls = f.read().split('\n')
#     urls = list(filter(None, urls))

asyncio.run(scrape_html(index_url_pairs, request_delay))