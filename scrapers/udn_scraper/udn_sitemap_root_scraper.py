import asyncio
from playwright.async_api import async_playwright
import re

async def scrape_urls_from_sitemap(base_url):
    all_urls = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        sitemap_url = base_url
        response = await page.goto(sitemap_url)
        
        content = await page.content()

        all_links = await page.get_by_text(re.compile("https:\/\/udn\.com\/[^\/]*[^\.]*.xml", re.IGNORECASE)).all_inner_texts()

        for link in all_links:
            if link is not None:
                all_urls.append(link)

        await browser.close()

    # Save the URLs to a file
    with open('udn_links_to_sitemaps.txt', 'w') as file:
        for url in all_urls:
            file.write(url + '\n')

    return all_urls

# Base URL without the page number and extension
base_sitemap_url = 'https://udn.com/sitemapxml/news/mapindex.xml'

# Run the scraping function with the delay
urls = asyncio.run(scrape_urls_from_sitemap(base_sitemap_url))

# The URLs have been saved to '/mnt/data/urls.txt'
print(f"Saved {len(urls)} URLs to file.")