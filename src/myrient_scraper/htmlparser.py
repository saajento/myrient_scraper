import requests

from html.parser import HTMLParser


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
                tparse = {
                    'link': vals['href'],
                }
                self.entries.append(tparse)
        elif tag == "td":
            if self.list_started and 'class' in vals and vals['class'] == 'size':
                self.data_ready = True

    def handle_data(self, data: str) -> None:
        if self.data_ready:
            self.entries[-1]['size'] = data
            self.data_ready = False
