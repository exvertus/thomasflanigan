import argparse
import csv
import logging
import pathlib

log = logging.getLogger(__name__).setLevel(logging.INFO)

def deduplicate(*csvfiles):
    for filepath in csvfiles:
        with open(filepath, newline='') as fp:
            csvreader = csv.reader(fp)
            log.info('break here')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='De-duplicate identical rows in CSV file.')
    parser.add_argument('files', help='two or more csv paths',
        action="extend", nargs="+", type=pathlib.Path)
    args = parser.parse_args()
    deduplicate(args.files)
    log.info('Done.')
