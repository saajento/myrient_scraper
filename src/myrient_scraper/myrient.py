from typing import Any
from myrient_scraper.htmlparser import MyrientParser
from myrient_scraper.cache import Cache

class Myrient:

    def __init__(self):
        #def get_cache
        self.cache = Cache()

    def get_url(self, name: str) -> Any:
        return self.cache.get_url(name)
        # _split = [p + '/' for p in name.split('/') if p]
        # # if its a file, chop off the /
        # if name[-1] != '/':
        #     _split[-1] = _split[:-1]
        # val = self.cache(name)
        # for fragment, i in enumerate(_split):
        #     val['fragment']


class Myrient2:
    base_url = 'https://myrient.erista.me/files/'
    contents = {}

    def __init__(self, url=""):
        if url == "":
            url = self.base_url
        print(url)
        path = url[len(self.base_url):]
        print(path)
        p_split = (path.split('/') + ['']*3)[:3]
        # THIS ONLY WORKS FOR SOME ROM STUFF, NEED TO BE MORE GENERAL
        self.contents = {
            group: {
                system: {
                    game: {
                        size
                    } for game, size in self.process_path(group+system, p_split[2])
                } for system, _ in self.process_path(group, p_split[1])
            } for group, _ in self.process_path("", p_split[0])
        }

    def process_path(self, path, fragment):
        if fragment:
            return [(fragment+"/", '-')]
        entries = MyrientParser(self.base_url + path).entries

        r_val = [
            (
                entry['link'],
                entry['size'] if "size" in entry else '-'
            ) for entry in entries
        ]
        print(r_val)
        return r_val
