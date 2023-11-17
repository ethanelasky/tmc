The pipeline follows two general steps, regardless of scraper. First, we collect links to all articles from within the given timeframe. Then, we collect article content and metadata from each of these links.

Files (scripts, sample outputs) for each step of the process are provided in the relevant subfolder.

At a later date, I will open-source all article links collected as part of my project. Unfortunately, releasing all article texts in a similar fashion falls outside the scope of fair use, otherwise I would do this as well.

# Process by website

## Liberty Times News (自由時報)
Links: Scraped [search.ltn.com.tw](search.ltn.com.tw) using ‘的' search query and looping through each page/day (pagination capped at 20 items). [ltn_2013_links.json][ltn_link_scraper/ltn_2013_links.json] is an example entry.
Articles: Scraped links using Playwright. [ltn_sample_article_entry.csv](ltn_article_scraper/ltn_sample_article_entry.csv)) is an example entry scraped from [this](https://news.ltn.com.tw/news/politics/breakingnews/4492811) LTN article using my Python script.

## China Times (中國時報)
Links: Scraped the website's [sitemap](chinatimes.com/sitemaps/sitemap_article_all_index_amp_0.xml) with Playwright.
Articles: 

## United Daily News (聯合報)
Links: 
Articles:
