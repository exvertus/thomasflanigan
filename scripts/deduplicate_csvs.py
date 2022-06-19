import argparse
import csv
import logging
import pathlib
from re import U

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
FIELD_ROWS = (('username','link'), )

def consolidate_csvs(*csvfiles):
    csv_sets = dict()
    for filepath in csvfiles:
        this_set = set()
        with open(filepath, newline='') as fp:
            csvreader = csv.reader(fp)
            for row in FIELD_ROWS:
                next(csvreader)
            for row in csvreader:
                if row:
                    this_set.add(tuple(row))
        csv_sets[filepath] = this_set
    # debugging stuff
    first_set = csv_sets[args.files[0].expanduser()]
    second_set = csv_sets[args.files[1].expanduser()]
    difference = first_set - second_set
    with open(pathlib.Path('~/Desktop/art/deleted_followers.csv').expanduser(), 'w') as wf:
        csvwriter = csv.writer(wf)
        for row in FIELD_ROWS:
            csvwriter.writerow(row)
        csvwriter.writerows(difference)
    # end debugging stuff
    return list(set().union(*csv_sets.values()))

def results_to_csv(target, results):
    with open(target, 'w') as wf:
        csvwriter = csv.writer(wf)
        for row in FIELD_ROWS:
            csvwriter.writerow(row)
        csvwriter.writerows(results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=\
        'Perform a set union and De-duplicate identical rows in CSV file.')
    parser.add_argument('files', help='two or more csv paths',
        action="extend", nargs="+", type=pathlib.Path)
    parser.add_argument('--target', help='file path for main output',
        default=f"../build/${__name__}-output.csv", type=pathlib.Path)
    args = parser.parse_args()
    unique_rows = consolidate_csvs(*[f.expanduser() for f in args.files])
    results_to_csv(args.target.expanduser(), unique_rows)
    log.info('Done.')
