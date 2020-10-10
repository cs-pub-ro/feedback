#!/usr/bin/env python

import sys
import csv
import glob
import os
import re

PERC_LIMIT = 7.0
NUM_LIMIT = 15

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <prof-file>\n".format(sys.argv[0]))
        sys.exit(1)

    profs = {}
    csvfile = open(sys.argv[1], "rt")
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    # Skip header.
    h = next(reader)
    for row in reader:
        profs[row[0]] = {
                "ncourses": int(row[1]),
                "nfeedback": int(row[2]),
                "perc": float(row[3]),
                "users": int(row[4]),
                "course_grade": float(row[5]),
                "prof_grade": float(row[6])
                }
    csvfile.close()

    print("\"prof\",\"num_cursuri\",\"num_feedback\",\"proc_feedback\"")
    for k in sorted(profs, key=lambda x: profs[x]["perc"], reverse=True):
        if profs[k]["perc"] < PERC_LIMIT or profs[k]["nfeedback"] < NUM_LIMIT:
            continue
        print("\"{}\",\"{:d}\",\"{:d}\",\"{:4.2f}\"".format(k, profs[k]["ncourses"], profs[k]["nfeedback"], profs[k]["perc"]))


if __name__ == "__main__":
    sys.exit(main())
