from myrient_scraper.myrient import Myrient


url1='https://myrient.erista.me/files/No-Intro/SNK%20-%20NeoGeo%20Pocket/'
url2='https://myrient.erista.me/files/'
my = Myrient(url1)
for group in my.contents:
    print(f"Group {group}")
    _g = my.contents[group]
    for system in _g:
        print(f"  - System {system}")
        for game in _g[system]:
            print(f"    - Game - {game}\n      - {_g[system][game]}")