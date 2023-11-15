import asyncio
from playwright.async_api import async_playwright
import re


async def scrape_urls_from_sitemap(base_url, start_page, end_page, delay=5.0):

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        for i in range(start_page, end_page + 1):
            all_urls = []
            sitemap_url = f"{base_url}_{i}.xml"
            response = await page.goto(sitemap_url)
            
            content = await page.content()

            # Find all 'loc' elements and extract the URL

            all_links = await page.get_by_text(re.compile("https:\/\/www\.chinatimes\.com\/amp\/[^\/]*\/[0-9]*-[0-9]*", re.IGNORECASE)).all_inner_texts()

            for link in all_links:
                if link is not None:
                    all_urls.append(link)

            # Wait for the specified delay before making the next request
            await asyncio.sleep(delay)

            # Save the URLs to a file
            with open('urls.txt', 'a') as file:
                for url in all_urls:
                    file.write(url + ', ' + str(i) + '\n')


        await browser.close()

# Base URL without the page number and extension
base_sitemap_url = 'https://www.chinatimes.com/sitemaps/article_amp_sitemaps/sitemap_article_amp'

# Define the start and end page numbers
start_page = 522
end_page = 976 #976

# The delay in seconds between requests
request_delay = 5.0  # Adjust this value as needed

# Run the scraping function with the delay
urls = asyncio.run(scrape_urls_from_sitemap(base_sitemap_url, start_page, end_page, request_delay))

# The URLs have been saved to '/mnt/data/urls.txt'
print(f"Saved {len(urls)} URLs to file.")