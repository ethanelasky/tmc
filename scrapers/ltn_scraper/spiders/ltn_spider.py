import scrapy
from datetime import timedelta, date
import re
from pathlib import Path

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2013, 1, 1)
end_date = date(2013, 1, 1) ## Change to corpus end date later
dates = []
for day in daterange(start_date, end_date):
    dates.append(day.strftime("%Y%m%d"))

class LtnSpiderSpider(scrapy.Spider):
    name = "ltn_spider"
    allowed_domains = ["ltn.com.tw"]
    start_urls = ["""https://search.ltn.com.tw/list?
              keyword=的&start_time={day}&end_time={day}
              &sort=date&type=all&page=10""" for day in dates] ## Change to 1 after testing is done

    def parse(self, response):
        page = response.url.split("page=")[-1]
        date = re.match("start_time=([0-9]{8})", response.url)

        links = response.css("a.http::text").getall()

        for i in range(len(links)):
            yield {"date": date, "page": page, "link": links[i]}

        next_page = response.css("a.p_next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        

        



