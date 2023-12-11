import pandas as pd
import scrapy


class HTMLGetterSpider(scrapy.Spider):
    name = "html_getter"
    allowed_domains = ["ltn.com.tw"]

    start_urls = pd.read_parquet("ltn_links.parquet")['link'].values.tolist()

    def parse(self, response):
        yield {'link': response.url, 'html': response.css("html")[0].get(), 'status': response.status}
