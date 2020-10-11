#!/usr/bin/env python

import sys
import csv
import glob
import os
import re


PERC_LIMIT = 7.0
NUM_LIMIT = 3


def semester_stats(courses):
    courses_per_semester = {}
    for c in courses.keys():
        m = re.match("[LM]-A[1-4]-S[1-2]", c)
        if m:
            k = m.group(0)
            if not k in courses_per_semester.keys():
                courses_per_semester[k] = {
                        "count_all": 0,
                        "count_not_zero": 0,
                        "count_over_perc": 0,
                        }
            courses_per_semester[k]["count_all"] += 1
            if courses[c]["nfeedback"] > 0:
                courses_per_semester[k]["count_not_zero"] += 1
            if courses[c]["perc"] >= PERC_LIMIT and courses[c]["nfeedback"] >= NUM_LIMIT:
                courses_per_semester[k]["count_over_perc"] += 1

    for c in courses.keys():
        m = re.match("[LM]-A[1-4]", c)
        if m:
            k = m.group(0)
            if not k in courses_per_semester.keys():
                courses_per_semester[k] = {
                        "count_all": 0,
                        "count_not_zero": 0,
                        "count_over_perc": 0,
                        }
            courses_per_semester[k]["count_all"] += 1
            if courses[c]["nfeedback"] > 0:
                courses_per_semester[k]["count_not_zero"] += 1
            if courses[c]["perc"] >= PERC_LIMIT and courses[c]["nfeedback"] >= NUM_LIMIT:
                courses_per_semester[k]["count_over_perc"] += 1

    for c in courses.keys():
        m = re.match("[LM]", c)
        if m:
            k = m.group(0)
            if not k in courses_per_semester.keys():
                courses_per_semester[k] = {
                        "count_all": 0,
                        "count_not_zero": 0,
                        "count_over_perc": 0,
                        }
            courses_per_semester[k]["count_all"] += 1
            if courses[c]["nfeedback"] > 0:
                courses_per_semester[k]["count_not_zero"] += 1
            if courses[c]["perc"] >= PERC_LIMIT and courses[c]["nfeedback"] >= NUM_LIMIT:
                courses_per_semester[k]["count_over_perc"] += 1

    k = "all"
    for c in courses.keys():
        if not k in courses_per_semester.keys():
            courses_per_semester[k] = {
                    "count_all": 0,
                    "count_not_zero": 0,
                    "count_over_perc": 0,
                    }
        courses_per_semester[k]["count_all"] += 1
        if courses[c]["nfeedback"] > 0:
            courses_per_semester[k]["count_not_zero"] += 1
        if courses[c]["perc"] >= PERC_LIMIT and courses[c]["nfeedback"] >= NUM_LIMIT:
            courses_per_semester[k]["count_over_perc"] += 1

    print("\"grup\",\"total\",\"non_zero\",\"cu_procentaj\"")
    for k in courses_per_semester.keys():
        t = courses_per_semester[k]
        print("\"{}\",\"{:d}\",\"{:d}\",\"{:d}\"".format(\
                k, t["count_all"], t["count_not_zero"], t["count_over_perc"]))


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <full-mapping-course-feedback-csv-file>\n".format(sys.argv[0]))
        sys.exit(1)

    courses = {}
    csvfile = open(sys.argv[1], "rt")
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    # Skip header.
    h = next(reader)
    for row in reader:
        courses[row[0]] = {
                "name": row[0],
                "nfeedback": int(row[1]),
                "perc": float(row[2]),
                "users": int(row[3]),
                "course_grade": float(row[4]),
                }
    csvfile.close()

    semester_stats(courses)

if __name__ == "__main__":
    sys.exit(main())
