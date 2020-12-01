#!/usr/bin/env python3

import csv
import sys
import os

# type,length,pos,motif,weight,average
WEIGHT_SOURCE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'nuccom4.csv')
WEIGHTS = {}
MOTIF_WIDTH = 4


def load_weights():
    with open(WEIGHT_SOURCE, newline='', encoding="utf-8") as csvfile:
        cs = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in cs:
            motif = "%s:%d:%s" % (row["type"], int(row["pos"]), row["motif"])
            weight = float(row["weight"])
            average = float(row["average"])

            WEIGHTS[motif] = {"weight": weight, "average": average}


def calculate_spacer(typ, spacer):
    weight = 0

    for i in range(0, len(spacer) - MOTIF_WIDTH + 1):
        motif = "%s:%d:%s" % (typ, i, spacer[i:i + MOTIF_WIDTH])
        if motif in WEIGHTS:
            weight += WEIGHTS[motif]["weight"] - WEIGHTS[motif]["average"]
            # print("%2i: %s %7.4f = %7.4f - %7.4f" % (i, spacer[i:i + MOTIF_WIDTH], WEIGHTS[motif]["weight"] - WEIGHTS[motif]["average"], WEIGHTS[motif]["weight"], WEIGHTS[motif]["average"]))
        else:
            # print("%2i: %s %7.4f" % (i, spacer[i:i + MOTIF_WIDTH], 0))
            pass

    return weight


def process_input():
    if len(sys.argv) < 2:
        print("Usage: %s <WT|HF> <Spacer>" % (sys.argv[0]))
        sys.exit(1)
    elif len(sys.argv) == 2:
        typ = sys.argv[1]
        for line in sys.stdin:
            spacer = line.rstrip()
            weight = calculate_spacer(typ, spacer)
            print("%s,%.4f" % (spacer, weight))
    else:
        typ = sys.argv[1]
        for spacer in sys.argv[2:]:
            weight = calculate_spacer(typ, spacer)
            print("%s,%.4f" % (spacer, weight))


if __name__ == '__main__':
    load_weights()
    process_input()
