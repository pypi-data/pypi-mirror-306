#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

# Python modules
import argparse
import textwrap

# user
import wagascianpy.analysis.apply_detector_flags

###############################################################################
#                                  arguments                                  #
###############################################################################

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(usage='use "python %(prog)s --help" for more information',
                                     argument_default=None, description=textwrap.dedent('''\
                                     Apply the detector flags as an additional TTree called detector_flags'''))

    PARSER.add_argument('-f', '--input-file', metavar='<WAGASCI decoded file>', dest='input_file',
                        type=str, required=True, help=textwrap.dedent('''\
                        Path to a WAGASCI decoded file *_ecal_dif_X_tree.root or a directory containing those files.
                        If it is a directory all the files ending in *_ecal_dif_X_tree.root inside it will be analyzed.
                        If the "r" option is set the directory is traversed recursively.  
                        '''))

    PARSER.add_argument('-n', '--run-number', metavar='<WAGASCI run number>', dest='run_number',
                        type=int, required=False, default=-1, help=textwrap.dedent('''\
                        Run number. If not given the run number is guessed from the file or folder name.
                        '''))

    PARSER.add_argument('-b', '--wagasci-database', metavar='<WAGASCI database>', dest='wagasci_database', type=str,
                        required=True, help=textwrap.dedent('''\
                        Path to the WAGASCI run database file. This file is created by the 
                        Wagasci Database Viewer (wagasciviewer.py) program and is usually called wagascidb.db.
                        '''))

    ARGS = PARSER.parse_args()

    INPUT_FILE = ARGS.input_file
    RUN_NUMBER = ARGS.run_number
    WAGASCI_DATABASE = ARGS.wagasci_database

    wagascianpy.analysis.apply_detector_flags.apply_detector_flags(INPUT_FILE, RUN_NUMBER, WAGASCI_DATABASE)
