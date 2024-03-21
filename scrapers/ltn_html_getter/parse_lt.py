from bs4 import BeautifulSoup
import glob
import json
import numpy as np
import pandas as pd
import re
import sys

text_selector = """
    .boxTitle[id!=checkIE][data-desc!=圖片] > p:not(.appE1121, .after_ir, .before_ir, .copyright),
    .boxText[id!=checkIE][data-desc!=圖片] > p:not(.appE1121, .after_ir, .before_ir, .copyright),
    .text[id!=checkIE][data-desc!=圖片] > p:not(.appE1121, .after_ir, .before_ir, .copyright),
    .text[id!=checkIE][data-desc!=圖片] > div > p:not(.appE1121, .after_ir, .before_ir, .copyright)"""
filepaths = glob.glob(sys.argv[1] + "/*.html")

with open(sys.argv[1] + "_processed.csv", 'w') as f:
    f.write("title,date,text,link\n")

for filepath in filepaths:
    json_works = False
    with open(filepath) as html:
        index = re.search("/(\\d+)", filepath)[1]
        print("Writing", str(index))
        soup = BeautifulSoup(html.read(), "html.parser")
        is_error_page = "".join([str(title.text) for title in soup.select("h3")])

        if re.search('頁面不見了', is_error_page):
            continue

        json_str = soup.find('script', {'type': 'application/ld+json'})
        if json_str:
            json_str = json_str.text.replace('\n', '').replace('\r', '').replace("\t", "").strip().replace("\\'", "'")
            try:
                data = json.loads(json_str)
                json_works = True
            except json.decoder.JSONDecodeError:
                pass
        
        if json_works:
            title = data.get("headline")
            date = data.get("datePublished")
            link = data.get("mainEntityOfPage")

        else:
            title = "".join([str(title.text) for title in soup.select("h1")])
            if not title:
                meta_tag = soup.find('meta', {'property': 'og:title'})
                article_title = meta_tag['content'].split('-')[0] if meta_tag else "".join([str(title.text) for title in soup.select('h1')])
            date = "".join([str(title.text) for title in soup.select("time.article-content__time")])
            if not date:
                date_tag = soup.find('meta', {'property': 'article:published_time'})
                date = date_tag['content'] if date_tag else "".join([str(time.text) for time in soup.select('*:is(time, .time):not(.auther)')])
            link = soup.find("meta", {"property":"og:url"})
            link = link['content'] if link else None
        
        if re.search("ltn.com.tw/$", link): # Skip articles that redirected to the main page of or a main section page of the website
            continue

        text = "".join([str(p.text) for p in soup.select(text_selector)])
        if not text: 
            section = soup.find('section', class_='article-content__editor')
            text = section.get_text(strip=True) if section else None
            if not text:
                text = "".join([str(p.text) for p in soup.select("div[data-en-clipboard=true] > p")])

        if re.search("ent.ltn.com.tw/news/breakingnews/", link) and not text: # Skip headline-only entertainment news with no article body
            continue
            
        
        h4 = "".join([str(p.text) for p in soup.select("h4")])
        is_video_only = bool(re.search("更多內容\\s*請見影片", h4)) or bool(re.search("訂閱【自由追新聞】", h4)) or bool(re.search("自由說新聞", title))
        
        if is_video_only: # Skip articles that are video-only with no article body
            continue 

        if not (bool(index) and bool(title) and bool(text) and bool(link)):
            print("Error at", index)
            print("from JSON:", bool(json_str))
            print("Title:", title)
            print("Date:", date)
            print("Text:, ...")
            print("Link:", link)
            break
        
        df = pd.DataFrame(data={'title':title, 'date':date, 'text':text, 'link':link}, index=[index])
        df.to_csv(sys.argv[1] + "_processed.csv", mode='a', header=False)

df = pd.read_csv(sys.argv[1] + "_processed.csv")
df = df.drop_duplicates()
df = df.sort_index()
df.to_csv(sys.argv[1] + "_processed.csv")
print("Removed duplicates and sorted index!")