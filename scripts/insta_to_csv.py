import argparse
import bs4
import csv
import logging
import pathlib
import re
from urllib.parse import urljoin

log = logging.getLogger(__name__)

CLASS_PATTERN = re.compile("^notranslate")
BASE_PATH = "https://www.instagram.com"

def parse_followers(read_filepath):
    log.info(f"Parsing followers from ${read_filepath}...")
    soup = bs4.BeautifulSoup(
        bs4.UnicodeDammit.detwingle(open(read_filepath, 'rb').read()), 'lxml')
    followers = [a.attrs['href'] for a in soup.find_all("a", class_=CLASS_PATTERN)]
    log.info(f"Found ${len(followers)} followers.")
    return followers

def followers_to_csv(followers, write_filepath):
    fields = ('username', 'link')
    followers = [(f.strip('/') ,urljoin(BASE_PATH, f)) for f in followers]
    with open(write_filepath, 'w') as wf:
        csvwriter = csv.writer(wf)
        csvwriter.writerow(fields)
        csvwriter.writerows(followers)
    log.info(f"wrote output to ${write_filepath}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert scraped instagram data to CSV file.')
    parser.add_argument('data', help='path to readable file')
    parser.add_argument('target', 
        help='path to write CSV output to', default='../build/output.csv')
    args = parser.parse_args()
    followers = parse_followers(pathlib.Path(args.data).expanduser())
    followers_to_csv(followers, pathlib.Path(args.target).expanduser())
    log.info('Done.')
