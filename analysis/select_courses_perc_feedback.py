#!/usr/bin/env python

import sys
import csv

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
                "prof": row[1],
                "nfeedback": int(row[2]),
                "perc": float(row[3]),
                "users": int(row[4]),
                "course_grade": float(row[5]),
                }
    csvfile.close()

    print("\"curs\",\"prof\",\"num_feedback\",\"proc_feedback\",\"num_utilizatori\",\"evaluare\"")
    for k in sorted(courses, key=lambda x: courses[x]["perc"], reverse=True):
        print("\"{}\",\"{}\",\"{:d}\",\"{:4.2f}\",\"{:d}\",\"{:3.2f}\"".format(k, courses[k]["prof"], courses[k]["nfeedback"], courses[k]["perc"], courses[k]["users"], courses[k]["course_grade"]))


if __name__ == "__main__":
    sys.exit(main())
