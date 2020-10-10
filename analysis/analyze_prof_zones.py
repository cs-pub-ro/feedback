#!/usr/bin/env python

import sys
import csv
import glob
import os
import re


PERC_LIMIT = 7.0
NUM_LIMIT = 15


def stats(profs):
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
    for c in profs.keys():
        if profs[c]["prof_grade"] > 4:
            idx = "4-5"
        elif profs[c]["prof_grade"] > 3:
            idx = "3-4"
        elif profs[c]["prof_grade"] > 2:
            idx = "2-3"
        else:
            idx = "1-2"
        zones[idx]["num"] += 1
        zones[idx]["nfeedback"] += profs[c]["nfeedback"]
        zones[idx]["eval"] += profs[c]["nfeedback"] * profs[c]["prof_grade"]
        zones[idx]["users"] += profs[c]["users"]

    print("\"zona\",\"num_prof\",\"proc_prof\",\"n_med_feedback\",\"proc_med\",\"eval_med\"")
    for idx in zones.keys():
        if zones[idx]["num"]:
            print("\"{}\",\"{:d}\",\"{:4.2f}\",\"{:5.2f}\",\"{:4.2f}\",\"{:3.2f}\"".format(idx, zones[idx]["num"], 100.0 * zones[idx]["num"] / len(profs), float(zones[idx]["nfeedback"]) / zones[idx]["num"], 100.0 * float(zones[idx]["nfeedback"]) / zones[idx]["users"], float(zones[idx]["eval"]) / zones[idx]["nfeedback"]))


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
        if float(row[3]) < PERC_LIMIT or int(row[2]) < NUM_LIMIT:
            continue
        profs[row[0]] = {
                "ncourses": int(row[1]),
                "nfeedback": int(row[2]),
                "perc": float(row[3]),
                "users": int(row[4]),
                "course_grade": float(row[5]),
                "prof_grade": float(row[6])
                }
    csvfile.close()

    stats(profs)


if __name__ == "__main__":
    sys.exit(main())
