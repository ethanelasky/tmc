import asyncio
from playwright.async_api import async_playwright
import re

async def scrape_urls_from_sitemap(root_links, delay=5.0):

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        for sitemap_url in root_links:

            leaf_links = []

            response = await page.goto(sitemap_url)
            
            content = await page.content()

            all_links = await page.get_by_text(re.compile("https:\/\/udn\.com\/([A-Za-z0-9\/])*", re.IGNORECASE)).all_inner_texts()

            for link in all_links:
                if link is not None:
                    leaf_links.append(link)

            with open('udn_article_links.txt', 'w') as file:
                for leaf in leaf_links:
                    file.write(leaf + '\n')

            # Wait for the specified delay before making the next request
            await asyncio.sleep(delay)

        await browser.close()


    return leaf_links

# The delay in seconds between requests
request_delay = 5.0  # Adjust this value as needed

with open('udn_links_to_sitemaps.txt') as f:
    root_links = f.read().split("\n")

# Run the scraping function with the delay
urls = asyncio.run(scrape_urls_from_sitemap(root_links, request_delay))

# The URLs have been saved to '/mnt/data/urls.txt'
print(f"Saved {len(urls)} URLs to file.")