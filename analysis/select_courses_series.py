#!/usr/bin/env python

import sys
import csv
import glob
import os
import re


def semester_stats(courses):
    courses_per_semester = {}
    for c in courses.keys():
        m = re.match("[LM]-A[1-4]-S[1-2]-[^-]+-[^-]+", c)
        if m:
            k1 = re.match("[LM]-A[1-4]-S[1-2]", c)[0]
            k2 = re.split("-", c)[4]
            k = k1+"-"+k2
            if not k in courses_per_semester.keys():
                courses_per_semester[k] = {
                        "count": 1,
                        "nfeedback": courses[c]["nfeedback"],
                        "users": courses[c]["users"],
                        "val": courses[c]["course_grade"] * courses[c]["nfeedback"]
                        }
            else:
                courses_per_semester[k]["count"] += 1
                courses_per_semester[k]["nfeedback"] += courses[c]["nfeedback"]
                courses_per_semester[k]["users"] += courses[c]["users"]
                courses_per_semester[k]["val"] += courses[c]["course_grade"] * courses[c]["nfeedback"]

    print("\"grup\",\"num_cursuri\",\"num_feedback\",\"proc_feedback\",\"num_utilizatori\",\"evaluare\"")
    for k in courses_per_semester.keys():
        t = courses_per_semester[k]
        if t["count"] < 2:
            continue
        print("\"{}\",\"{:d}\",\"{:d}\",\"{:4.2f}\",\"{:d}\",\"{:3.2f}\"".format(\
                k, t["count"], t["nfeedback"], 100.0 * t["nfeedback"] / t["users"], t["users"], t["val"] / t["nfeedback"]))


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <mapping-course-feedback-csv-file>\n".format(sys.argv[0]))
        sys.exit(1)

    courses = {}
    csvfile = open(sys.argv[1], "rt")
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    # Skip header.
    h = next(reader)
    for row in reader:
        courses[row[0]] = {
                "name": row[0],
                "nfeedback": int(row[2]),
                "perc": float(row[3]),
                "users": int(row[4]),
                "course_grade": float(row[5]),
                }
    csvfile.close()

    semester_stats(courses)

if __name__ == "__main__":
    sys.exit(main())
