#!/usr/bin/env python

import sys
import csv
import re


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <raw-feedback-csv-file>\n".format(sys.argv[0]))
        sys.exit(1)

    d = {}
    csvfile = open(sys.argv[1], "rt")
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        d[row[0]] = {
                "num": int(row[2]),
                "perc": float(row[3]),
                "users": int(row[4]),
                "val": float(row[5])
                }
    csvfile.close()

    courses = []
    for k in d.keys():
        m = re.match("[LM]-A[1-4]-S[1-2]-[^-]+", k)
        if not m:
            continue
        p = m.group(0)
        if not p in courses:
            courses.append(p)

    sems = ["L-A1", "L-A2", "L-A3", "L-A4", "M-A1", "M-A2"]
    res = {}
    for c in courses:
        for k in d.keys():
            if k.startswith(c):
                if c in res.keys():
                    name = c+"-all"
                    res[c]["name"] = name
                    res[c]["count"] += 1
                    res[c]["num"] += d[k]["num"]
                    res[c]["users"] += d[k]["users"]
                    res[c]["val"] += d[k]["val"] * d[k]["num"]
                else:
                    res[c] = {
                            "name": k,
                            "count": 1,
                            "num": d[k]["num"],
                            "users": d[k]["users"],
                            "val": d[k]["val"] * d[k]["num"]
                            }

    print("\"curs\",\"num_cursuri\",\"num_feedback\",\"proc_feedback\",\"num_utilizatori\",\"evaluare\"")
    for c in res.keys():
        print("\"{}\",\"{:d}\",\"{:d}\",\"{:4.2f}\",\"{:d}\",\"{:3.2f}\"".format(res[c]["name"], res[c]["count"], res[c]["num"], 100.0 * res[c]["num"] / res[c]["users"], res[c]["users"], res[c]["val"] / res[c]["num"]))


if __name__ == "__main__":
    sys.exit(main())
