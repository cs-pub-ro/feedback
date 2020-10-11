#!/usr/bin/env python

import sys
import csv
import glob
import os
import re

NUM_LIMIT = 10

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <prof-file>\n".format(sys.argv[0]))
        sys.exit(1)

    asist = {}
    csvfile = open(sys.argv[1], "rt")
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    # Skip header.
    h = next(reader)
    for row in reader:
        asist[row[0]] = {
                "nfeedback": int(row[1]),
                "course_grade": float(row[2]),
                "asist_grade": float(row[3])
                }
    csvfile.close()

    print("\"asist\",\"num_feedback\",\"evaluare_curs\",\"evaluare_prof\"")
    for k in sorted(asist, key=lambda x: asist[x]["asist_grade"], reverse=True):
        if asist[k]["nfeedback"] < NUM_LIMIT:
            continue
        print("\"{}\",\"{:d}\",\"{:3.2f}\",\"{:3.2f}\"".format(k, asist[k]["nfeedback"], asist[k]["course_grade"], asist[k]["asist_grade"]))


if __name__ == "__main__":
    sys.exit(main())
