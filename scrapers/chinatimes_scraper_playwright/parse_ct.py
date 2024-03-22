from bs4 import BeautifulSoup
import glob
import json
import numpy as np
import pandas as pd
import re
import sys

filepaths = glob.glob(sys.argv[1] + "/*.html")
with open(sys.argv[1] + "_processed.csv", 'w') as f:
    f.write("title,source,date,text,link\n")

for filepath in filepaths:
    with open(filepath) as html:
        index = re.search("/(\\d+)", filepath)[1]
        
        soup = BeautifulSoup(html.read(), "html.parser")
        title = "".join([str(title.text) for title in soup.select("h1")])
        if re.match("目前無法找到任何頁面！", title):
                continue
        source = "".join([str(title.text) for title in soup.select("div.source")])
        date = "".join([str(title.text) for title in soup.select(".date")])
        text = "".join([str(title.text) for title in soup.select("div.article-body > p")])
        link_tag = soup.find('amp-social-share', {'type': 'messenger'})
        link = link_tag['data-param-link'] if link_tag else None
        json_str = soup.find('script', {'type': 'application/ld+json'})
        if not link:
            json_works = False
            if json_str:
                if type(json_str) == list:
                    json_str = json_str[0]
                json_str = json_str.text.replace('\n', '').replace('\r', '').replace("\t", "").strip().replace("\\'", "'")
                try:
                    data = json.loads(json_str)
                    json_works = True
                except json.decoder.JSONDecodeError:
                    pass     
            if json_works:
                link = data[0].get("url")
        df = pd.DataFrame(data={'title':title, 'source':source, 'date':date, 'text':text, 'link': link}, index=[index])
        df.to_csv(sys.argv[1] + "_processed.csv", mode='a', header=False)
        print("Wrote", filepath)

df = pd.read_csv(sys.argv[1] + "_processed.csv")
df = df.drop_duplicates()
df = df.sort_index()
df.to_csv(sys.argv[1] + "_processed.csv")
print("Removed duplicates and sorted index!")