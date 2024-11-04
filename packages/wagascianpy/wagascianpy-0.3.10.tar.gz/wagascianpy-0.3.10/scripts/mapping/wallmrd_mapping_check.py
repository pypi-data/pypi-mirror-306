#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

# Python modules
import argparse
import re

DIF_IFX = 0
CHIP_IDX = 1
CHAN_IDX = 2
POSX_IDX = 3
POSY_IDX = 4
POSZ_IDX = 5
VIEW_IDX = 6
PLANE_IDX = 7
SLOT_IDX = 8

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(usage='use "python %(prog)s --help" for more information',
                                     argument_default=None, description='Check sanity of WallMRD mapping file')

    PARSER.add_argument('-f', '--mapping-file', metavar='<mapping file>', dest='mapping_file', type=str,
                        required=True, help='Path to the WallMRD mapping file')

    ARGS = PARSER.parse_args()

    with open(ARGS.mapping_file, "r") as mapping_file:
        repl_str = re.compile('^[-+]?\d*\.\d+|\d+$')
        lines = mapping_file.readlines()
        counter = 0
        for line in lines:
            counter += 1
            output = []
            words = re.split(' |\t', line)
            for word in words:
                match = re.search(repl_str, word)
                if match:
                    output.append(float(match.group()))
            if len(output) == 9:
                if (output[POSZ_IDX] == 100 and output[SLOT_IDX] != 0) or \
                        (output[POSZ_IDX] == 300 and output[SLOT_IDX] != 1) or \
                        (output[POSZ_IDX] == 500 and output[SLOT_IDX] != 2) or \
                        (output[POSZ_IDX] == 700 and output[SLOT_IDX] != 3) or \
                        (output[POSZ_IDX] == 900 and output[SLOT_IDX] != 4) or \
                        (output[POSZ_IDX] == 1100 and output[SLOT_IDX] != 5) or \
                        (output[POSZ_IDX] == 1300 and output[SLOT_IDX] != 6) or \
                        (output[POSZ_IDX] == 1500 and output[SLOT_IDX] != 7):
                    print("ERROR in line %d : %s" % (counter, line))
            else:
                if line[0] != '#':
                    print("Line not recognized : %s" % line)
