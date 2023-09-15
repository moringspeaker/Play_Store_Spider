#!/usr/bin/env python
# coding: utf-8
import requests
from tqdm import tqdm


URL = 'https://d.apkpure.com/b/XAPK/'
VERSION = '?version=latest'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def download(id):
    url = URL + id + VERSION
    print('Downloading from: ' + url)
    r = requests.get(url, headers=HEADERS,stream=True)
    r.raise_for_status()

    total_size = int(r.headers.get('content-length', 0))
    chunk_size = 1024  # 1 KB

    # Download the file and save it chunk by chunk
    with open(id + '.xapk', 'wb') as f:
        for chunk in tqdm(r.iter_content(chunk_size), total=total_size // chunk_size, unit='KB'):
            if chunk:  # filter out keep-alive chunks
                f.write(chunk)

if __name__ == '__main__':

    download('com.facebook.katana')