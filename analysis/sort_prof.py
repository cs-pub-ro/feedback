#!/usr/bin/env python

import sys
import csv
import glob
import os
import re


def main():
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: {} <prof-raw-feedback-csv-file> <prof-feedback-mapping>\n".format(sys.argv[0]))
        sys.exit(1)

    profs = {}
    csvfile = open(sys.argv[2], "rt")
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
                "prof_grade": 0.0
                }
    csvfile.close()

    csvfile = open(sys.argv[1], "rt")
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if row[0] in profs.keys():
            profs[row[0]]["prof_grade"] = (float(row[7]) + float(row[8]) + float(row[9]) + float(row[10])) / 4

    print("\"prof\",\"num_cursuri\",\"num_feedback\",\"proc_feedback\",\"num_utilizatori\",\"evaluare_curs\",\"evaluare_prof\"")
    for k in sorted(profs, key=lambda x: profs[x]["prof_grade"], reverse=True):
        print("\"{}\",\"{:d}\",\"{:d}\",\"{:4.2f}\",\"{:d}\",\"{:3.2f}\",\"{:3.2f}\"".format(k, profs[k]["ncourses"], profs[k]["nfeedback"], profs[k]["perc"], profs[k]["users"], profs[k]["course_grade"], profs[k]["prof_grade"]))


if __name__ == "__main__":
    sys.exit(main())
