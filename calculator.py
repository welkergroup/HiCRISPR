#!/usr/bin/env python3

import nuccom4
import deepcas9
import deepactivecrispr


def init():
    nuccom4.load_weights()
    deepactivecrispr.load_weights()


def calculate_sequence(seq):
    a_value = nuccom4.calculate_spacer('HF', seq[0:20])
    b_value = deepactivecrispr.calculate_spacer(seq[0:23])
    c_value = deepcas9.calculate_spacer(seq[0:20])

    return {
        'hi_crispr_a': a_value,
        'hi_crispr_a_cut': a_value > -0.5,
        'hi_crispr_b': b_value,
        'hi_crispr_b_cut': b_value > 0.6,
        'hi_crispr_c': c_value,
        'hi_crispr_c_cut': c_value > 0.7,
    }


def process_input():
    import sys
    if len(sys.argv) < 1:
        print("Usage: %s <Spacer>" % (sys.argv[0]))
        sys.exit(1)
    else:
        print("Spacer,Hi-CRISPR A,Hi-CRISPR B,Hi-CRISPR C")
        if len(sys.argv) == 1:
            for line in sys.stdin:
                spacer = line.rstrip()
                print_spacer(spacer)
        else:
            for spacer in sys.argv[1:]:
                print_spacer(spacer)


def print_spacer(spacer):
    weight = calculate_sequence(spacer)
    print("%s,%.4f,%.4f,%.4f" % (spacer, weight['hi_crispr_a'], weight['hi_crispr_b'], weight['hi_crispr_c']))


if __name__ == '__main__':
    init()
    process_input()
