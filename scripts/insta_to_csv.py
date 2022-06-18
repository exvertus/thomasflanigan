import argparse
import bs4
import logging
import pathlib

log = logging.getLogger(__name__)

def parse_followers(read_filepath):
    log.info(f"Parsing followers from ${read_filepath}...")
    with open(read_filepath) as rf:
        soup = bs4.BeautifulSoup(rf, 'lxml')
    log.debug('stop here')
    return followers

def followers_to_csv(followers, write_filepath):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert scraped instagram data to CSV file.')
    parser.add_argument('data', help='path to readable file')
    parser.add_argument('target', required=False, 
        help='path to write CSV output to', default='./output.csv')
    args = parser.parse_args()
    followers = parse_followers(pathlib.Path(args.data))
    followers_to_csv(followers, pathlib.Path(args.target))
