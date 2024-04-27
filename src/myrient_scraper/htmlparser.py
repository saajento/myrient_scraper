import re
import requests

from html.parser import HTMLParser


class Tags:
    tag_categories = {
        "region": [
            'Asia', 'Australia', 'Brazil', 'Canada', 'China', 'Europe',
            'Finland', 'France', 'Germany', 'Greece', 'Hong Kong',
            'Japan', 'Korea', 'New Zealand', 'Portugal', 'Russia',
            'Spain', 'Sweden', 'Taiwan', 'USA', 'United Kingdom', 'World'
        ],
        "language": [
            'Ar', 'Ca', 'De', 'El', 'En', 'Es', 'Fi', 'Fr', 'It',
            'Ja', 'Ko', 'Nl', 'Pl', 'Ru', 'Uk', 'Uz', 'Zh'
        ]
    }


    def __init__(self, title):
        self.misc = []
        self.languages = []
        self.regions = []
        tag_sets = re.findall(r'\([^\)]+\)', title)
        for value_string in [shuck[1:-1] for shuck in tag_sets]:
            set_values = value_string.split(',')
            try:
                self.sorter(set_values)
            except Exception:
                print(title)
                exit(1)

    def sorter(self, vals):
        stripped = [v.strip() for v in vals]
        for x in stripped:
            # if double-language code
            if len(x) > 4 and x[2]=='-' and x[0:2] in self.tag_categories['language']:
                self.languages = stripped
                return
            if x in self.tag_categories['language']:
                if self.languages:
                    print(f"L: {self.languages} but found:\n\t{stripped}")
                    raise Exception()
                self.languages = stripped
                return
            elif x in self.tag_categories['region']:
                if self.regions:
                    print(f"R: {self.regions} but found:\n\t{stripped}")
                    if self.regions == stripped:
                        continue
                    else:
                        raise Exception()
                self.regions = stripped
                return
        self.misc.extend(stripped)

    def __repr__(self):
        val = ""
        tg_l = ['M', 'L', 'R']
        for i, tag_group in enumerate([self.misc, self.languages, self.regions]):
            if tag_group:
                val += f" T-{tg_l[i]}: {tag_group}\n"
        return val


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
                tparse = self.parse_title(vals['title'])
                tparse['link'] = vals['href']
                if tparse['link'][-1] == '/':
                    tparse['extension'] = ''
                self.entries.append(tparse)
        elif tag == "td":
            if self.list_started and 'class' in vals and vals['class'] == 'size':
                self.data_ready = True
    
    def handle_data(self, data: str) -> None:
        if self.data_ready:
            self.entries[-1]['size'] = data
            self.data_ready = False

    def parse_title(self, title):
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
                # disregard if in open parens
                if tag_l > 0 and tag_r < 0:
                    continue
                e_i = i
        if name_r < 0:
            name_r = e_i if e_i > 0 else len(title)
        if e_i < 0:
            extension = ""
        else:
            extension = title[e_i:]
        name = title[0:name_r]
        return {
            "name": name,
            "extension": extension
        }