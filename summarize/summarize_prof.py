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
                "prof": row[1],
                "num": int(row[2]),
                "perc": float(row[3]),
                "users": int(row[4]),
                "val": float(row[5])
                }
    csvfile.close()

    res = {}
    for k in d.keys():
        prof = d[k]["prof"]
        if prof in res.keys():
            res[prof]["count"] += 1
            res[prof]["num"] += d[k]["num"]
            res[prof]["users"] += d[k]["users"]
            res[prof]["val"] += d[k]["val"] * d[k]["num"]
        else:
            res[prof] = {
                    "count": 1,
                    "num": d[k]["num"],
                    "users": d[k]["users"],
                    "val": d[k]["val"] * d[k]["num"]
                    }

    print("\"prof\",\"num_cursuri\",\"num_feedback\",\"proc_feedback\",\"num_utilizatori\",\"evaluare\"")
    for prof in res.keys():
        print("\"{}\",\"{:d}\",\"{:d}\",\"{:4.2f}\",\"{:d}\",\"{:3.2f}\"".format(prof, res[prof]["count"], res[prof]["num"], 100.0 * res[prof]["num"] / res[prof]["users"], res[prof]["users"], res[prof]["val"] / res[prof]["num"]))


if __name__ == "__main__":
    sys.exit(main())
