#!/usr/bin/env python

import sys
import csv
import glob
import os
import re


NUM_LIMIT = 10


def stats(asist):
    zones = {
            "4-5": {
                "nfeedback": 0,
                "eval": 0.0,
                "num": 0
                },
            "3-4": {
                "nfeedback": 0,
                "eval": 0.0,
                "num": 0
                },
            "2-3": {
                "nfeedback": 0,
                "eval": 0.0,
                "num": 0
                },
            "1-2": {
                "nfeedback": 0,
                "eval": 0.0,
                "num": 0
                }
            }
    for c in asist.keys():
        if asist[c]["asist_grade"] > 4:
            idx = "4-5"
        elif asist[c]["asist_grade"] > 3:
            idx = "3-4"
        elif asist[c]["asist_grade"] > 2:
            idx = "2-3"
        else:
            idx = "1-2"
        zones[idx]["num"] += 1
        zones[idx]["nfeedback"] += asist[c]["nfeedback"]
        zones[idx]["eval"] += asist[c]["nfeedback"] * asist[c]["asist_grade"]

    print("\"zona\",\"num_prof\",\"proc_prof\",\"n_med_feedback\",\"eval_med\"")
    for idx in zones.keys():
        if zones[idx]["num"]:
            print("\"{}\",\"{:d}\",\"{:4.2f}\",\"{:5.2f}\",\"{:3.2f}\"".format(idx, zones[idx]["num"], 100.0 * zones[idx]["num"] / len(asist), float(zones[idx]["nfeedback"]) / zones[idx]["num"], float(zones[idx]["eval"]) / zones[idx]["nfeedback"]))


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
        if int(row[1]) < NUM_LIMIT:
            continue
        asist[row[0]] = {
                "nfeedback": int(row[1]),
                "course_grade": float(row[2]),
                "asist_grade": float(row[3])
                }
    csvfile.close()

    stats(asist)


if __name__ == "__main__":
    sys.exit(main())
