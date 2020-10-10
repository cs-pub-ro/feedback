#!/usr/bin/env python

import sys
import csv


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

    sems = ["L-A1", "L-A2", "L-A3", "L-A4", "M-A1", "M-A2"]
    res = {}
    for s in sems:
        for k in d.keys():
            if k.startswith(s):
                if s in res.keys():
                    res[s]["count"] += 1
                    res[s]["num"] += d[k]["num"]
                    res[s]["users"] += d[k]["users"]
                    res[s]["val"] += d[k]["val"] * d[k]["num"]
                else:
                    res[s] = {
                            "count": 1,
                            "num": d[k]["num"],
                            "users": d[k]["users"],
                            "val": d[k]["val"] * d[k]["num"]
                            }

    sems = ["L-A1-S1", "L-A1-S2", "L-A2-S1", "L-A2-S2", "L-A3-S1", "L-A3-S2", "L-A4-S1", "L-A4-S2", "M-A1-S1", "M-A1-S2", "M-A2-S1", "M-A2-S2"]
    for s in sems:
        for k in d.keys():
            if k.startswith(s):
                if s in res.keys():
                    res[s]["count"] += 1
                    res[s]["num"] += d[k]["num"]
                    res[s]["users"] += d[k]["users"]
                    res[s]["val"] += d[k]["val"] * d[k]["num"]
                else:
                    res[s] = {
                            "count": 1,
                            "num": d[k]["num"],
                            "users": d[k]["users"],
                            "val": d[k]["val"] * d[k]["num"]
                            }

    print("\"an/sem\",\"num_cursuri\",\"num_feedback\",\"proc_feedback\",\"num_utilizatori\",\"evaluare\"")
    for s in res.keys():
        print("\"{}\",\"{:d}\",\"{:d}\",\"{:4.2f}\",\"{:d}\",\"{:3.2f}\"".format(s, res[s]["count"], res[s]["num"], 100.0 * res[s]["num"] / res[s]["users"], res[s]["users"], res[s]["val"] / res[s]["num"]))


if __name__ == "__main__":
    sys.exit(main())
