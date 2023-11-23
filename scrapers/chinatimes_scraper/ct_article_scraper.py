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

async def scrape_text_from_page(urls, delay=5.0):
    """ 
    Scrapes article contents from webpages given a list of URLs. The
    contents of each article consists of its link, title, section, subsection,
    date and time of publication, and the text of the article. 

    After collecting 100 articles or upon reaching the end of the list of
    urls, append the dataframe to a CSV file of links. Then clear the DataFrame
    to avoid storing too much information in memory.
    
    Inputs: 
    - A list of URLs (as strings)
    - delay: minimum time between requests (to avoid IP bans / overthrottling)

    Outputs:
    - A CSV file containing article contents named as specified in command
        line arguments
    """

    assert len(sys.argv) == 3

    df = pd.DataFrame(columns=['link', 'title', 'sections', 'time', 'article text', 'author'])

    path_to_extension = "./uBlock"
    user_data_dir = "/tmp/test-user-data-dir"

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,
        args=[
            "--headless=new",
            f"--disable-extensions-except={path_to_extension}",
            f"--load-extension={path_to_extension}",
        ],
        )

        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',


        page = await browser.new_page()
        page.set_default_navigation_timeout(60000)
        context = browser.new_context(user_agent=ua)

        for i in range(len(urls)):
            url = urls[i]
            print(url)
            while True:
                try:
                    await page.goto(url)      
                except:
                    await asyncio.sleep(delay)
                    continue
                break

            source = await page.locator('div.source').all_inner_texts()
            author = await page.locator('div.author').all_inner_texts()
            title = await page.locator('css=.article-title').inner_text()
            time = await page.locator("css=time").get_attribute("datetime")
            paragraphs = await page.locator("css=div.article-body > p").all_inner_texts()
            article_text = '\n'.join(paragraphs)

            # print(url, sections, title, time, article_text) #debugging
            df.loc[len(df.index)] = [url, title, source, time, article_text, author]

            await asyncio.sleep(delay)

            if i % 100 == 0 or i == len(urls) - 1:
                df.to_csv(path_or_buf=sys.argv[2], mode='w')
                print(f"Saved {len(df.index)} articles to file.")
                df = pd.DataFrame(columns=['link', 'title', 'sections', 'time', 'article text', 'author'])

        await browser.close()
    

# The delay in seconds between requests
request_delay = 3.0 

urls = pd.read_csv(sys.argv[1])['link']

asyncio.run(scrape_text_from_page(urls, request_delay))