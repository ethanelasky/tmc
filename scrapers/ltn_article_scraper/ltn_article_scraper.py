"""
Scrapes articles from Liberty Times News' online newspaper. See the
docstring of scrape_text_from_page for more info. 

Usage: python ltn_article_scraper.py [path_to_urls] [output_file_name]

Ex: python ltn_article_scraper.py ltn_2013_links.json 
                                    ltn_2013_article_contents.csv
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

    df = pd.DataFrame(columns=['link', 'title', 'section1',
                                    'section2', 'time', 'article text'])

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        for i in range(len(urls)):
            url = urls[i]
            await page.goto(url)

            sections = await page.locator('css=div.breadcrumbs.boxTitle.boxText > a').all_inner_texts()

            title = await page.locator('css=h1').inner_text()

            time = await page.locator('css=span.time').inner_text()

            paragraphs = await page.locator("css=div.text.boxTitle.boxText > "
                                      + "p:not(.appE1121)"
                                      + ":not(.before_ir)").all_inner_texts()
            article_text = '\n'.join(paragraphs)

            # print(url, sections, title, time, article_text) #debugging
            df.loc[len(df.index)] = [url, title, sections[0], sections[1], time, article_text]

            await asyncio.sleep(delay)

            if i % 100 == 0 or i == len(urls) - 1:
                df.to_csv(path_or_buf=sys.argv[2], mode='w')
                print(f"Saved {len(df.index)} articles to file.")
                df = pd.DataFrame(columns=['link', 'title', 'section1',
                                    'section2', 'time', 'article text'])

        await browser.close()
    

# The delay in seconds between requests
request_delay = 3.0 

urls = pd.read_json(sys.argv[1])['link'].values

asyncio.run(scrape_text_from_page(urls, request_delay))