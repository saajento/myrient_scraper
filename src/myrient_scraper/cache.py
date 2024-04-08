from myrient_scraper.myrient import Myrient
from myrient_scraper.htmlparser import MyrientParser
import json
import os
import requests
import urllib.parse
import time

CACHE_FILE = 'cache.json'
SITE_CACHE_DIR = 'myrient-cache/'

base_url = Myrient.base_url

def create_cache_file():
    my = Myrient()
    with open(CACHE_FILE, 'w') as f:
        json.dump(my.contents, f)

def create_site_cache(url = ""):
    addr = base_url + url
    # fetch content
    resp = requests.get(addr)
    time.sleep(1)
    # write to file
    path = SITE_CACHE_DIR + url
    f_path = path + 'index.htm'
    os.makedirs(path, exist_ok=True)
    with open(f_path, 'w') as f:
        f.write(resp.text)
    # parse content
    entries = MyrientParser(text=resp.text).entries
    for entry in entries:
        #determine if file or directory
        #  does it have a size?
        if entry['size'] != '-':
            return 
        #  does it have an extension?
        if entry['extension']:
            return
        item = urllib.parse.unquote(entry['link'])
        if item[-1] == "/":
            create_site_cache(url + item)
    # create other files