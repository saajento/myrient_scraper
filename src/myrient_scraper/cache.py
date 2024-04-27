from myrient_scraper.htmlparser import MyrientParser
import json
import os
import requests
import urllib.parse
import time
import sys


CACHE_FILE = 'cache.json'
SITE_CACHE_DIR = 'myrient-cache/'
base_url = 'https://myrient.erista.me/files/'


class Cache:
    base_url = base_url
    CACHE_FILE = 'cache.json'
    SITE_CACHE_DIR = 'myrient-cache/'

    def __init__(self):
        # check for json json
        if os.path.isfile(self.CACHE_FILE):
            with open(self.CACHE_FILE, 'r') as f:
                self._cache = json.load(f)
        else:
            raise Exception("No cache found")

    def query(self, path, constraints=[]):
        raw_q = self.get_url(path)
        results = {}
        for c in constraints:
            pass
        return results

    def get_url(self, path):
        val = self._cache
        _split = [p + '/' for p in path.split('/') if p]
        # if its a file, chop off the /
        if path[-1] != '/':
            _split[-1] = _split[:-1]
        for layer in _split:
            val = val[layer]
        return val


def create_cache_file():
    def create_json(url='') -> dict:
        result = {}
        for entry in cached_entries(url):
            name = urllib.parse.unquote(entry['link'])
            print(name)
            if is_file(entry):
                result[name]={
                    'size': entry['size']
                }
            else:
                result[name]=create_json(url+name)
        return result

    cache_dict = {
        item: create_json(item)
        for item in create_json()
    }

    with open(CACHE_FILE, 'w') as f:
        json.dump(cache_dict, f)


def cached_entries(url):
    path = SITE_CACHE_DIR + url
    i_path = path + 'index.htm'
    if os.path.isfile(i_path):
        with open(i_path, 'r') as f:
            text = f.read()
        if text:
            return MyrientParser(text=text).entries
        raise Exception(f"ERR - {i_path} is invalid")
    else:
        raise Exception(f"Err - {i_path} doesnt exist")


def is_file(entry) -> bool:
    if entry['size'] != '-' or entry['extension']:
        if entry['size'] == '-':
            print(f'!!!!! no size for {entry}')
        return True
    return False


def check_site_cache(url=''):
    path = SITE_CACHE_DIR + url
    f_path = path + 'index.htm'
    DBGMSG=f"{url}{' '*30}"[:30]
    if os.path.isfile(f_path):
        with open(f_path, 'r') as f:
            text = f.read()
        if text:
            entries = MyrientParser(text=text).entries
            DBGMSG+=f"\t{len(entries)}"
            fc = 0
            dc = 0
            for entry in entries:
                item = urllib.parse.unquote(entry['link'])
                if item == "/":
                    raise Exception("preventing loop over '/'")
                if is_file(entry):
                    fc += 1
                    continue
                if item[-1] == "/":
                    dc += 1
                    check_site_cache(url + item)
            print(f"{DBGMSG}\t{fc}\t{dc} - {fc+dc}")



def create_site_cache(url = "", reuse=True, remote=True) -> None:
    DBGMSG=f"[S]{url}:{reuse}:{remote}\t"
    path = SITE_CACHE_DIR + url
    f_path = path + 'index.htm'
    if reuse and os.path.isfile(f_path):
        DBGMSG+=":C"
        with open(f_path, 'r') as f:
            idx_text = f.read()
        if not idx_text:
            print(f"{DBGMSG}: BAD INDEX")
            os.remove(f_path)
            os.rmdir(path)
            return
        #time.sleep(.05)
    elif remote:
        DBGMSG+=":R"
        idx_text = requests.get(base_url + url).text
        os.makedirs(path, exist_ok=True)
        # write to file
        with open(f_path, 'w') as f:
            f.write(idx_text)
        time.sleep(1)
    else:
        print(f"{DBGMSG}-SKIP")
        return
    # parse content
    print(f"{DBGMSG}:", end='')
    entries = MyrientParser(text=idx_text).entries
    print(f"E{len(entries)}")
    for entry in entries:
        item = urllib.parse.unquote(entry['link'])
        DBGMSG=f"\t{item}"
        #determine if file or directory
        #  does it have a size?
        if entry['size'] != '-' or entry['extension']:
            print(f"{DBGMSG}-{entry['size']}-{entry['extension']}")
            continue
        if item == "/":
            raise Exception("drat")
        if item[-1] == "/":
            create_site_cache(url + item, reuse=reuse, remote=remote)