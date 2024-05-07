from myrient_scraper.cache import Cache


class MyrientObject:
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


    def __init__(self, title: str):
        self.misc = []
        self.languages = []
        self.regions = []
        self.parse_title(title)

    def parse_title(self, title:str):
        name_r = -1
        tag_l = -1
        e_i = -1
        tag_sets = []
        for i, c in enumerate(title):
            if c == '(':
                if name_r < 0:
                    name_r = i-1
                tag_l = i
            elif c == ')' and tag_l > 0:
                tag_sets.append(title[tag_l+1:i])
                tag_l = -1
            elif c == ".":
                # disregard if in open parens
                if tag_l > 0:
                    continue
                e_i = i
        if name_r < 0:
            name_r = e_i if e_i > 0 else len(title)
        self.name = title[0:name_r]

        if e_i < 0:
            self.extension = ""
        else:
            self.extension = title[e_i+1:]

        for tag_string in tag_sets:
            set_values = tag_string.split(',')
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
        val = f"{self.name}:({self.extension})\n"
        tg_l = ['M', 'L', 'R']
        for t_char, tag_group in [('M', self.misc), ('L', self.languages), ('R', self.regions)]:
            if tag_group:
                val += f" {t_char}: {tag_group}\n"
        return val

class Myrient(Cache):
    pass

#     def __init__(self):
#         self.cache = Cache()

#     def get_url(self, name: str) -> dict:
#         return self.cache.get_url(name)
