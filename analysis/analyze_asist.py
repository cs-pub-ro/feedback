#!/usr/bin/env python

import sys
import csv
import glob
import os
import re


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <asist-raw-feedback-csv-file>\n".format(sys.argv[0]))
        sys.exit(1)

    asist = {}
    csvfile = open(sys.argv[1], "rt")
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        asist[row[0]] = {
                "nfeedback": int(row[1]),
                "course_grade": float(row[2]),
                "asist_grade": 0.0
                }
        asist[row[0]]["asist_grade"] = (float(row[12]) + float(row[13]) + float(row[14]) + float(row[15])) / 4
    csvfile.close()

    print("\"asist\",\"num_feedback\",\"evaluare_curs\",\"evaluare_prof\"")
    for k in sorted(asist, key=lambda x: asist[x]["asist_grade"], reverse=True):
        print("\"{}\",\"{:d}\",\"{:3.2f}\",\"{:3.2f}\"".format(k, asist[k]["nfeedback"], asist[k]["course_grade"], asist[k]["asist_grade"]))


if __name__ == "__main__":
    sys.exit(main())
