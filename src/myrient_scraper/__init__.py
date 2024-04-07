from argparse import ArgumentParser

'''
asdf
'''

if __name__ == "__main__":
    parser = ArgumentParser(
        prog='Myrient Scraper',
        description='Scrapes Myrient',
        epilog='~~~~~~~~~~~~~~~~~~'
    )
    parser.add_argument('-u','--url')
    args = parser.parse_args()
    print("args: {args}")