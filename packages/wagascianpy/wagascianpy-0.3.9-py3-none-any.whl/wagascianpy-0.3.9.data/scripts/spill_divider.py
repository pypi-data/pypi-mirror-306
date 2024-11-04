#!python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#
import argparse
import os
import textwrap
from datetime import datetime, timedelta, date, time
from typing import Generator, List

import ROOT

import wagascianpy.database.wagascidb as db
import wagascianpy.utils.utils
import wagascianpy.utils.treenames as treenames
from wagascianpy.analysis.spill import WAGASCI_SPILL_BEAM_MODE
from wagascianpy.database.db_record import DBRecord as DBr
from wagascianpy.plotting.detector import Detectors

ROOT.PyConfig.IgnoreCommandLineOptions = True


def _daterange(start_date, end_date):
    # type: (date, date) -> Generator[date]
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def _decoded_path(root_dir, file, runname, dif_id):
    # type: (str, str, str, int) -> str
    decoded_filename = None
    filename, file_extension = os.path.splitext(file)
    if file_extension == '.raw':
        decoded_filename = "{}_ecal_dif_{}_tree.root".format(runname, dif_id)
    elif file_extension == '.root':
        decoded_filename = file
    return os.path.join(root_dir, runname, decoded_filename)


def _get_active_detectors(runs, root_dir):
    # type: (List[db.WagasciRunRecord], str) -> Detectors
    detectors = Detectors()
    detectors.disable_all_difs()
    for one_run in runs:
        for dif_id, file in one_run.raw_files.items():
            decoded_fpath = _decoded_path(root_dir=root_dir, file=file, runname=one_run.name, dif_id=dif_id)
            print("Day {}: DIF {} is enabled".format(day.strftime("%Y-%m-%d"), dif_id))
            print("Adding DIF {} decoded file : {}".format(dif_id, decoded_fpath))
            detectors.enable_dif(dif_id)
            detectors.get_dif(dif_id).add_tree(root_file=decoded_fpath,
                                               tree_name=wagascianpy.utils.utils.extract_raw_tree_name(decoded_fpath),
                                               tree_friends=[treenames.BSD_TREE_NAME, treenames.FSN_TREE_NAME,
                                                             treenames.TEMPHUM_TREE_NAME, treenames.PEU_TREE_NAME,
                                                             treenames.TIME_NS_TREE_NAME, treenames.FLAGS_TREE_NAME])
    return detectors


def _clone_tree(input_tree, output_tfile):
    # type: (str, ROOT.TFile) -> ROOT.TChain
    output_tree = input_tree.CloneTree(0)
    output_tree.SetDirectory(output_tfile)
    output_tree.SetAutoFlush(100)
    output_tree.SetAutoSave(100)
    return output_tree


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage='use "python %(prog)s --help" for more information',
                                     argument_default=None, description=textwrap.dedent('''\
                                     Split the decoded runs into one folder per each day.'''))

    parser.add_argument('-d', '--wagasci-database', metavar='<WAGASCI run database>', dest='wagasci_database',
                        type=str, required=True, help=textwrap.dedent('''\
                        Path to the WAGASCI run database file. This file is created by the 
                        Wagasci Database Viewer (wagasciviewer.py) program and is usually called wagascidb.db.
                        '''))

    parser.add_argument('-f', '--wagasci-decoded', metavar='<WAGASCI runs directory>',
                        dest='wagasci_decoded', type=str, required=True, help=textwrap.dedent('''\
                        Path to the directory containing all the WAGASCI decoded runs.'''))

    parser.add_argument('-o', '--output-directory', metavar='<output directory>', dest='output_directory',
                        type=str, required=True, help=textwrap.dedent('''\
                        Directory where to store all the output files
                        '''))

    parser.add_argument('-a', '--start-time', metavar='<start time>', dest='start_time', type=str,
                        help='Start date and time in the format "%%Y/%%m/%%d %%H:%%M:%%S"', default=None,
                        required=False)

    parser.add_argument('-b', '--stop-time', metavar='<stop time>', dest='stop_time', type=str,
                        help='Stop date and time in the format "%%Y/%%m/%%d %%H:%%M:%%S"', default=None,
                        required=False)

    parser.add_argument('-m', '--start-run', metavar='<start run>', dest='start_run', type=int,
                        help='start run number', default=None, required=False)

    parser.add_argument('-n', '--stop-run', metavar='<stop run>', dest='stop_run', type=int,
                        help='Stop run number', default=None, required=False)

    parser.add_argument('-t', '--t2krun', metavar='<T2K run>', dest='t2krun', type=int,
                        help='T2K run number (default is 10)', default=10, required=False)

    parser.add_argument('-g', '--only-good', dest='only_good', required=False, default=True,
                        action='store_true', help=textwrap.dedent('''\
                        Only select runs and detectors whose flag is set to good (good run or good data)'''))

    parser.add_argument('-c', '--day-counter-offset', metavar='<offset>', type=int, dest='day_counter_offset',
                        required=False, default=0, help=textwrap.dedent('''\
                        Offset to be added to the counter that counts the number of days. The day counter is used 
                        as a placeholder for the run number. It is useful to give an offset if you are running this 
                        script multiple times and want to keep the run number consecutive.'''))

    arguments = parser.parse_args()

    time_interval = bool(arguments.start_time) and bool(arguments.stop_time)
    run_interval = bool(arguments.start_run) and bool(arguments.stop_run)

    if time_interval and not run_interval:
        start = DBr.str2datetime(arguments.start_time)
        stop = DBr.str2datetime(arguments.stop_time)
    elif run_interval and not time_interval:
        start = arguments.start_run
        stop = arguments.stop_run
    else:
        raise ValueError("Please specify (--start-time AND --stop-time) OR (--start-run AND --stop-run)")

    # If the run interval is given extract the start and stop time (if the start and stop time is already set this
    # function does nothing)
    start, stop = db.run_to_interval(start=start, stop=stop, database=arguments.wagasci_database)
    print("Start time : {}".format(start.strftime("%Y-%m-%d %H:%M:%S")))
    print("Stop time : {}".format(stop.strftime("%Y-%m-%d %H:%M:%S")))

    # for each day in the range
    for day_counter, day in enumerate(_daterange(start_date=start.date(), end_date=stop.date())):
        print("Splitting day {}".format(day.strftime("%Y-%m-%d")))

        day_begin = DBr.datetime2timestamp(datetime.combine(
            date=day, time=time(hour=0, minute=0, second=0, microsecond=0)))
        day_end = DBr.datetime2timestamp(datetime.combine(
            date=day, time=time(hour=23, minute=59, second=59, microsecond=999999)))

        with db.WagasciDataBase(db_location=arguments.wagasci_database, repo_location=arguments.wagasci_decoded,
                                is_borg_repo=False) as database:
            daily_runs = database.get_time_interval(datetime_start=day_begin,
                                                    datetime_stop=day_end,
                                                    only_good=arguments.only_good,
                                                    include_overlapping=True)
            if not daily_runs:
                print("No run found in day {}".format(day.strftime("%Y-%m-%d")))
                continue

            print("Found {} runs in day {}".format(len(daily_runs), day.strftime("%Y-%m-%d")))
            for i, run in enumerate(daily_runs):
                print("  Run {}: {}".format(i, run.name))

            active_detectors = _get_active_detectors(runs=daily_runs, root_dir=arguments.wagasci_decoded)

            if not active_detectors:
                print("No active detector found in day {}".format(day.strftime("%Y-%m-%d")))
                continue

            output_directory = "physics_run_{}".format(day.strftime("%Y-%m-%d"))

            for detector in active_detectors:
                for dif in [dif for dif in detector if dif.is_enabled()]:
                    print("Day {}: Saving DIF {} data".format(day.strftime("%Y-%m-%d"), dif.dif_id))
                    output_runname = "physics_run_{}_00-00-00_{}".format(day.strftime("%Y-%m-%d"),
                                                                         arguments.day_counter_offset + day_counter)
                    output_filename = "{}_ecal_dif_{}_tree.root".format(output_runname, dif.dif_id)
                    output_directory = os.path.join(arguments.output_directory, output_runname)
                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory, mode=0o775)
                    output_path = os.path.join(output_directory, output_filename)

                    tfile = ROOT.TFile(output_path, "RECREATE")
                    raw = _clone_tree(input_tree=dif.get_tree(), output_tfile=tfile)

                    tree_friends = {treenames.BSD_TREE_NAME: None,
                                    treenames.FSN_TREE_NAME: None,
                                    treenames.TEMPHUM_TREE_NAME: None,
                                    treenames.PEU_TREE_NAME: None,
                                    treenames.TIME_NS_TREE_NAME: None,
                                    treenames.FLAGS_TREE_NAME: None}
                    tree_clones = tree_friends.copy()
                    for friend in tree_friends.keys():
                        if dif.has_friend(friend):
                            tree_friends[friend] = dif.get_friend(friend)
                    for friend, tree in tree_friends.items():
                        if tree is not None:
                            tree_clones[friend] = _clone_tree(input_tree=dif.get_friend(friend), output_tfile=tfile)
                    for j, event in enumerate(dif.get_tree()):
                        if j % 1000 == 0:
                            print("Day {}: DIF {}: processed {} events".format(day.strftime("%Y-%m-%d"), dif.dif_id, j))
                        if event.spill_mode == WAGASCI_SPILL_BEAM_MODE and day_begin < event.timestamp < day_end:
                            raw.Fill()
                            for tree in tree_clones.values():
                                if tree is not None:
                                    tree.Fill()
