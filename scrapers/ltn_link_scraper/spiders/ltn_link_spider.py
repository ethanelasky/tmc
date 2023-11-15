import scrapy
from datetime import timedelta, date
import re
from pathlib import Path
import random


class LtnSpiderSpider(scrapy.Spider):
    """
    On the LTN website, start_time is inclusive, while end_time is exclusive."""

    name = "ltn_link_spider"
    allowed_domains = ["ltn.com.tw"]
    def start_requests(self):
        def daterange(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield [start_date + timedelta(n),start_date + timedelta(n+1)]

        start_date = date(2016, 1, 1)
        end_date = date(2023, 7, 1) ## Change to corpus end date later
        dates = []
        for days in daterange(start_date, end_date):
            dates.append([days[0].strftime("%Y%m%d"), days[1].strftime("%Y%m%d")])
        urls = [
            "https://search.ltn.com.tw/list?keyword=的&start_time={}&end_time={}&type=all&sort=date&page=1".format(days[0], days[1]) for days in dates ## Change page to 1 after testing is done
        ]
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8,zh-TW;q=0.5,ja;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            # 'Cookie': 'ltnSessionLast=1698955842513; _ss_pp_id=d5a7add3da5cdad125d1698318289093; fcmToken=0; ltnSession=1698955752660; status=æ\x99´æ\x99\x82å¤\x9aé\x9b²; icon=wi_0002_day.png; temperature=22-24  â\x84\x83; softPush=1; _td=802ee217-587b-43e1-8841-b9ca6a608c73; keyword=%E7%9A%84; date=%E4%B8%8D%E9%99%90%E6%99%82%E9%96%93; type=%E5%85%A8%E9%83%A8; sort=',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            }
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=header)
   
    def parse(self, response):
        """
        each element in headers_and_cookies follows [header, cookie]
        """
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8,zh-TW;q=0.5,ja;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            # 'Cookie': 'ltnSessionLast=1698955842513; _ss_pp_id=d5a7add3da5cdad125d1698318289093; fcmToken=0; ltnSession=1698955752660; status=æ\x99´æ\x99\x82å¤\x9aé\x9b²; icon=wi_0002_day.png; temperature=22-24  â\x84\x83; softPush=1; _td=802ee217-587b-43e1-8841-b9ca6a608c73; keyword=%E7%9A%84; date=%E4%B8%8D%E9%99%90%E6%99%82%E9%96%93; type=%E5%85%A8%E9%83%A8; sort=',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            }
        page = int(response.url.split("page=")[-1])
        pattern = re.compile("(?:start_time=)([0-9]{8})")
        date = pattern.search(response.url)[1]

        links = response.css("a.http::text").getall()

        for i in range(len(links)):
            yield {"date": date, "page": page, "link": links[i]}

        next_page = response.css("a.p_next::attr(href)").get()
        if next_page:
            yield scrapy.Request(url=response.url.split("page=")[0] + "page=" + str(page + 1))

        

        



