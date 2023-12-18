"""
Scrapes text from articles on the China Times' online newspaper website. 
See the docstring of scrape_text_from_page for more info. 

Usage: python ct_article_scraper.py [path_to_urls] [output_file_name]

Ex: python ct_article_scraper.py ct_2013_links.json 
                                    ct_2013_article_contents.csv
"""

import asyncio
import pandas as pd
from playwright_stealth import stealth_async
from playwright.async_api import async_playwright, BrowserContext
import sys
from scipy import stats

headless = False

async def scrape_html(index_url_pairs, mu=5):
    """ 
    Scrapes article HTML from webpages given a list of URLs.
    
    Inputs: 
    - A list of URLs (as strings)
    - mu: Parameter for the Exponential (mu) process describing delay time (to avoid IP bans / overthrottling)

    Outputs:
    - HTML files that each represent one article. 
    """

    path_to_extension = "./uBlock"
    user_data_dir = "/tmp/test-user-data-dir"
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

    async with async_playwright() as p:

        async def new_context():
            context = await p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            user_agent=ua,
            args=[
                f"--disable-extensions-except={path_to_extension}",
                f"--load-extension={path_to_extension}",
            ],
            )
            return context
        async def new_page(context): 
            page = await context.new_page()
            await stealth_async(page)
            await page.goto("https://bot.sannysoft.com/")
            return page

        context = await new_context()
        page = await new_page(context)

        for i in range(len(index_url_pairs)):
            pair = index_url_pairs[i]
            index = pair[0]
            url = pair[1]
            i = 0
            while True:
                try:
                    await page.goto(url)      
                except:
                    sleep_duration = stats.norm.rvs(mu, 1)
                    await asyncio.sleep(sleep_duration)
                    print("waiting for page to load", sleep_duration)
                    i += 1
                    if i == 10:
                        i = 0
                        await page.close()
                        await context.close()
                        context = await new_context()
                        page = await new_page(context)
                        print("Created new page from context")
                    continue
                break

            contents = await page.content()
            with open(str(index) + ".html", 'w', encoding="utf-8") as f:
                f.write(contents)
                print(f"Wrote {index} to file.")

            sleep_duration = stats.norm.rvs(mu, 1)
            print("between pages, wait time: ", sleep_duration)
            await asyncio.sleep(sleep_duration)

        await context.close()
    

# The mean delay in seconds between requests
mu = 9.0 

if sys.argv[1][:-3] == ".csv":
    df = pd.read_csv(sys.argv[1], index_col=0)
    if len(sys.argv) == 3:
        df = df.loc[int(sys.argv[2]):, :]
    indices = df.index
    links = df['link'].values
    index_url_pairs = list(zip(indices, links))
else:
    df = pd.read_parquet(sys.argv[1])
    if len(sys.argv) == 3:
        df = df.loc[int(sys.argv[2]):, :]
    indices = df.index
    links = df['link'].values
    index_url_pairs = list(zip(indices, links))
print(df)

asyncio.run(scrape_html(index_url_pairs, mu))