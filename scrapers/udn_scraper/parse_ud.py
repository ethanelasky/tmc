from bs4 import BeautifulSoup
import glob
import numpy as np
import pandas as pd
import re
import sys

filepaths = glob.glob(sys.argv[1] + "/*.html")

with open(sys.argv[1] + "_processed.csv", 'w') as f:
    f.write("title,date,text,link\n")

for filepath in filepaths:
    with open(filepath) as html:
        index = re.search("/(\\d+)", filepath)[1]
        
        soup = BeautifulSoup(html.read(), "html.parser")
        is_error_page = "".join([str(title.text) for title in soup.select("span.error-text")])
        if re.search('404', is_error_page):
            continue
        else:
            title = "".join([str(title.text) for title in soup.select("h1")])
            if not title:
                meta_tag = soup.find('meta', {'property': 'og:title'})
                article_title = meta_tag['content'].split(' | ')[0] if meta_tag else np.NaN
            date = "".join([str(title.text) for title in soup.select("time.article-content__time")])
            if not date:
                date_tag = soup.find('meta', {'property': 'article:published_time'})
                date = date_tag['content'] if date_tag else 'Not Found'

            text = "".join([str(title.text) for title in soup.select("section.article-content__editor > p, article.story-article > p, div > main > p, section.article-content__wrapper > p")])
            if not text: 
                section = soup.find('section', class_='article-content__editor')
                text = section.get_text(strip=True) if section else None
                if not text:
                    script_tag = section.find('script') if section else None
                    url_match = re.search(r'window.location.href="([^"]+)"', script_tag.string if script_tag else '')
                    if url_match:
                        continue
            link = soup.find("meta", {"property":"og:url"})
            link = link['content'] if link else None
            df = pd.DataFrame(data={'title':title, 'date':date, 'text':text, 'link':link}, index=[index])
            df.to_csv(sys.argv[1] + "_processed.csv", mode='a', header=False)
            print("Wrote", filepath)

df = pd.read_csv(sys.argv[1] + "_processed.csv")
df = df.drop_duplicates()
df = df.sort_index()
df = df[~(df['text'].isna() & (df['link'].str.contains("money\\.") | df['link'].str.contains("vip\\.")))]
df = df[~(df['title'].isna() & (df['link'].str.contains("/story/8448/")))]
df.to_csv(sys.argv[1] + "_processed.csv")
print("Removed duplicates and sorted index!")