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
PX_IDX = 9

CHANNEL_ID_TO_PX = {
    15: 1,
    11: 2,
    14: 3,
    10: 4,
    13: 5,
    9: 6,
    12: 7,
    8: 8,
    0: 9,
    1: 10,
    2: 11,
    3: 12,
    4: 13,
    5: 14,
    6: 15,
    7: 16,
    26: 17,
    23: 18,
    27: 19,
    22: 20,
    25: 21,
    21: 22,
    24: 23,
    20: 24,
    28: 25,
    19: 26,
    29: 27,
    18: 28,
    30: 29,
    17: 30,
    31: 31,
    16: 32
}

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(usage='use "python %(prog)s --help" for more information',
                                     argument_default=None, description='Insert PX information into mapping file')

    PARSER.add_argument('-f', '--mapping-file-input', metavar='<mapping file>', dest='mapping_file_input', type=str,
                        required=True, help='Path to the input WallMRD mapping file')

    PARSER.add_argument('-o', '--mapping-file-output', metavar='<mapping file>', dest='mapping_file_output', type=str,
                        required=True, help='Path to the output WallMRD mapping file')

    ARGS = PARSER.parse_args()

    with open(ARGS.mapping_file_input, "r") as mapping_file_input:
        with open(ARGS.mapping_file_output, "w") as mapping_file_output:
            repl_str = re.compile('^[-+]?\d*\.\d+|\d+$')
            input_lines = mapping_file_input.readlines()
            counter = 0
            for input_line in input_lines:
                counter += 1
                input_fields = []
                input_words = re.split(' |\t', input_line)
                for input_word in input_words:
                    match = re.search(repl_str, input_word)
                    if match:
                        input_fields.append(float(match.group()))
                if len(input_fields) == 10:
                    mapping_file_output.write(input_line)
                elif len(input_fields) == 9:
                    output_line = "{}\t{}\n".format(input_line.strip('\n'), CHANNEL_ID_TO_PX[input_fields[CHAN_IDX]])
                    mapping_file_output.write(output_line)
                else:
                    if input_line[0] == '#':
                        mapping_file_output.write(input_line)
                    else:
                        print("Line not recognized : %s" % input_line)
