#!/usr/bin/env python

import sys
import csv
import re


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <all-mapping-course-feedback-csv-file>\n".format(sys.argv[0]))
        sys.exit(1)

    courses = {}
    csvfile = open(sys.argv[1], "rt")
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if not re.match("[LM]-", row[0]):
            continue
        if re.match("M-.*-Cercetare-", row[0]):
            continue
        if re.match("M-.*-CSP-", row[0]):
            continue
        if re.match("M-.*-ELD-", row[0]):
            continue
        if re.match("M-.*-CSPED-", row[0]):
            continue
        if re.match("M-.*-ET-", row[0]):
            continue
        if re.match("M-.*-AR-", row[0]):
            continue
        if re.match("[LM]-A[1-4]-S[1-2]-[^-]+-[^-]+-[^-]+", row[0]):
            continue
        if not re.match("[LM]-A[1-4]-S[1-2]-", row[0]):
            continue
        if int(row[3]) < 5:
            continue
        courses[row[0]] = {
                "nfeedback": int(row[1]),
                "perc": float(row[2]),
                "users": int(row[3]),
                "course_grade": float(row[4]),
                }
    csvfile.close()

    print("\"curs\",\"num_feedback\",\"proc_feedback\",\"num_utilizatori\",\"evaluare_curs\"")
    for k in courses:
        print("\"{}\",\"{:d}\",\"{:4.2f}\",\"{:d}\",\"{:3.2f}\"".format(k, courses[k]["nfeedback"], courses[k]["perc"], courses[k]["users"], courses[k]["course_grade"]))


if __name__ == "__main__":
    sys.exit(main())
