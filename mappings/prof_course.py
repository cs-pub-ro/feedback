#!/usr/bin/env python

import sys
import csv


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <courses-profs-file>\n".format(sys.argv[0]))
        sys.exit(1)

    in_file = sys.argv[1]
    d = {}

    csvfile = open(in_file, "rt")
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        course = row[0]
        prof = row[1]
        num = row[2]
        if course in d.keys():
            if d[course]["num"] > num:
                continue
        d[course] = {
                "prof": prof,
                "num": num
                }

    for course in d:
        print("\"{}\",\"{}\"".format(course, d[course]["prof"]))

    csvfile.close()

if __name__ == "__main__":
    sys.exit(main())
