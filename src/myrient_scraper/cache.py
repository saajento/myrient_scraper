from myrient_scraper.myrient import Myrient
import json
import os


CACHE_FILE = "cache.json"

def create_cache():
    my = Myrient()
    with open(CACHE_FILE, 'w') as f:
        json.dump(my.contents, f)
