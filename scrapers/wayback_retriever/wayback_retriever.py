import glob
import os
import pandas as pd
import py7zr
import re 
import sys
import wayback

session = wayback.WaybackSession(retries=15, backoff=2, timeout=60, user_agent=None, search_calls_per_second=1, memento_calls_per_second=30)
client = wayback.WaybackClient(session=session)
file_name = re.search("[^\\.]+", sys.argv[1])[0]
if not os.path.exists(file_name):
    os.makedirs(file_name)

df = pd.read_parquet(sys.argv[1])
if len(sys.argv) == 3:
        df = df.loc[int(sys.argv[2]):, :]
indices = df.index
links = df['link'].values
index_url_pairs = list(zip(indices, links))
for i in range(len(index_url_pairs)):
    pair = index_url_pairs[i]
    index = pair[0]
    url = pair[1]
    try:
        results = client.search(url, limit=1)
        result = next(results)
        page = client.get_memento(result)
        print(page.status_code)
        html_path = os.path.join(file_name, f"{str(index)}.html")
        with open(html_path, 'w', encoding="utf-8") as g:
            g.write(str(index) + ", " + url + ", " + page.text)
            print(f"Wrote {str(index)} to file.")
    except (wayback.exceptions.NoMementoError, StopIteration, wayback.exceptions.MementoPlaybackError) as e:
        with open(sys.argv[1][:-8] + "leftovers.csv", 'a', encoding="utf-8") as f:
                f.write(file_name + "/" + str(index) + ", " + url + "\n")
                print(f"Wrote {str(index)} to leftovers.")
        continue
    
html_files = glob.glob('*.html')

with py7zr.SevenZipFile(file_name + ".7z", 'w') as archive:
    html_files = glob.glob(os.path.join(file_name, '*.html'))
    for file_path in html_files:
        archive_name = os.path.basename(file_path)
        archive.write(file_path, arcname=archive_name)

for file in html_files:
    os.remove(file)
    print("Removed ", file, ".")

print("Scrape complete. All HTML files have been zipped into ", file_name + ".7z", " and deleted.")
        