import random
import hashlib
import requests
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}


def cache(url: str, prefix="", refresh_cache=False):
    filepath = f"cache/{prefix}{hashlib.md5(url.encode('utf8')).hexdigest()}"
    try:
        if refresh_cache:
            raise Exception("Refresh cache")
        print(f"Reading cache for {url}")
        return open(filepath, "rb").read().decode("utf8")
    except:
        time.sleep(random.random() * 2)
        print(f"Fetching for {url}")
        data = requests.get(url, headers=headers).content
        open(filepath, "wb").write(data)
        return data
