from myrient_scraper.cache import Cache
from myrient_scraper.htmlparser import Tags

url1='https://myrient.erista.me/files/No-Intro/SNK%20-%20NeoGeo%20Pocket/'
url2='https://myrient.erista.me/files/'

c = Cache()

s = set()

def setify(root):
    r_keys = root.keys()
    if 'size' in r_keys:
        return
    for key in r_keys:
        s.update(
            t for t in Tags(key).sets if ',' in t
        )
        setify(root[key])

def printify(root):
    r_keys = root.keys()
    if 'size' in r_keys:
        return
    for key in r_keys:
        t = Tags(key)
        print(f"{key}:")
        print(f"{t}")

count_set = {}
def countify(root):
    r_keys = root.keys()
    if 'size' in r_keys:
        return
    for key in r_keys:
        ts = Tags(key)
        for t in ts.languages + ts.regions + ts.misc:
            if t not in count_set:
                count_set[t] = 1
            else:
                count_set[t] += 1
            countify(root[key])

ul = set()
ur = set()
um = set()
def uniquefy(root):
    r_keys = root.keys()
    if 'size' in r_keys:
        return
    for key in r_keys:
        ts = Tags(key)
        for t in ts.languages:
            ul.add(t)
        for t in ts.regions:
            ur.add(t)
        for t in ts.misc:
            um.add(t)
        uniquefy(root[key])


uniquefy(c.get_url('No-Intro/'))
#count_sort = sorted(count_set, key=lambda x: count_set[x])
#for cs in count_sort:
#    print(f"{cs:20s}:\t{count_set[cs]}")

print(f"Unique Langs:\n\t{sorted(ul)}\n")
print(f"Unique Regs: \n\t{sorted(ur)}\n")
#print(f"Unique Misc: \n\t{sorted(um)}\n")

#printify(c.get_url('No-Intro/Nintendo - Nintendo Entertainment System (Headered)/'))

#setify(c.get_url('No-Intro/Nintendo - Nintendo Entertainment System (Headered)/'))