import re
import requests

from html.parser import HTMLParser


tag_categories = {
    "region": [
        "USA", "Europe", "Japan", "World", "Taiwan"
    ],
    "language": [
        "En", "Fr", "De", "Es", "It", "Nl", "Sv"
    ]
}

def parse_tags(tag_string):
    return re.findall(r'\([^\)]+\)', tag_string)

def parse_title(title):
    #print(title)
    name_r = -1
    tag_l = -1
    tag_r = -1
    e_i = -1
    for i, c in enumerate(title):
        if c == '(' and name_r < 0:
            name_r = i-1
            tag_l = i
            continue
        elif c == ')' and tag_l > 0:
            tag_r = i
        elif c == ".":
            e_i = i
    if name_r < 0:
        name_r = e_i if e_i > 0 else len(title)
    tag_string = ""
    if tag_l > 0:
        tag_string = title[tag_l:tag_r+1]
    if e_i < 0:
        extension = ""
    else:
        extension = title[e_i:]
    name = title[0:name_r]
    return {
        "name": name,
        #"tags": parse_tags(tag_string),
        "extension": extension
    }

class MyrientParser(HTMLParser):
    def __init__(self, url="", text=""):
        self.entries = []
        self.list_started = False
        self.data_ready = False
        super(MyrientParser, self).__init__()
        if url and not text:
            feed_source = requests.get(url, timeout=60).text
        elif text and not url:
            feed_source = text
        else:
            raise Exception("need a url or a block of text, chief")
        self.feed(feed_source)

    def handle_starttag(self, tag, attrs):
        if tag not in ['a', 'td']:
            return
        vals = {}
        for a in attrs:
            vals[a[0]] = a[1]
        if tag == "a":
            # if its a link of interest
            if 'title' in vals:
                self.list_started = True
                tparse = parse_title(vals['title'])
                tparse["link"] = vals['href']
                self.entries.append(tparse)
        elif tag == "td":
            if self.list_started and 'class' in vals and vals['class'] == 'size':
                self.data_ready = True
    
    def handle_data(self, data: str) -> None:
        if self.data_ready:
            self.entries[-1]['size'] = data
            self.data_ready = False
