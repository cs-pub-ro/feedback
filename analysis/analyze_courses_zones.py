#!/usr/bin/env python

import sys
import csv
import glob
import os
import re


PERC_LIMIT = 10


def stats(courses):
    zones = {
            "4-5": {
                "nfeedback": 0,
                "eval": 0.0,
                "users": 0,
                "num": 0
                },
            "3-4": {
                "nfeedback": 0,
                "eval": 0.0,
                "users": 0,
                "num": 0
                },
            "2-3": {
                "nfeedback": 0,
                "eval": 0.0,
                "users": 0,
                "num": 0
                },
            "1-2": {
                "nfeedback": 0,
                "eval": 0.0,
                "users": 0,
                "num": 0
                }
            }
    for c in courses.keys():
        if courses[c]["course_grade"] > 4:
            idx = "4-5"
        elif courses[c]["course_grade"] > 3:
            idx = "3-4"
        elif courses[c]["course_grade"] > 2:
            idx = "2-3"
        else:
            idx = "1-2"
        zones[idx]["num"] += 1
        zones[idx]["nfeedback"] += courses[c]["nfeedback"]
        zones[idx]["eval"] += courses[c]["nfeedback"] * courses[c]["course_grade"]
        zones[idx]["users"] += courses[c]["users"]

    print("\"zona\",\"num_cursuri\",\"proc_cursuri\",\"n_med_feedback\",\"proc_med\",\"eval_med\"")
    for idx in zones.keys():
        if zones[idx]["num"]:
            print("\"{}\",\"{:d}\",\"{:4.2f}\",\"{:5.2f}\",\"{:4.2f}\",\"{:3.2f}\"".format(idx, zones[idx]["num"], 100.0 * zones[idx]["num"] / len(courses), float(zones[idx]["nfeedback"]) / zones[idx]["num"], 100.0 * float(zones[idx]["nfeedback"]) / zones[idx]["users"], float(zones[idx]["eval"]) / zones[idx]["nfeedback"]))


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <course-feedback-csv-file>\n".format(sys.argv[0]))
        sys.exit(1)

    courses = {}
    csvfile = open(sys.argv[1], "rt")
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    # Skip header.
    h = next(reader)
    for row in reader:
        if float(row[2]) < PERC_LIMIT:
            continue
        courses[row[0]] = {
                "name": row[0],
                "nfeedback": int(row[1]),
                "perc": float(row[2]),
                "users": int(row[3]),
                "course_grade": float(row[4]),
                }
    csvfile.close()

    stats(courses)

if __name__ == "__main__":
    sys.exit(main())
