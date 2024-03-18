"""
USAGE: python zip_delete_utility.py [name of parquet file extracted]

"""

import glob
import lzma
import os
import re
import sys
import tarfile
file_name = re.search("[^\.]+", sys.argv[1])[0]

with tarfile.open(file_name + ".tar", "w") as tar:
    tar.add(file_name, arcname=os.path.basename(file_name))


with open(file_name + ".7z", 'w') as tar:
    with lzma.open(file_name, "w") as f:
        f.write(tar.read())

os.remove(file_name + ".tar")
os.removedirs(file_name)

print("Scrape complete. Created", file_name + ".tar.xz", "with solid compression.")