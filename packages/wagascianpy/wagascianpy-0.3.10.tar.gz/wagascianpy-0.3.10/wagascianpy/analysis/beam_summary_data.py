#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

# Python modules
import operator
import os
import re
import sys
from collections import namedtuple
from itertools import islice
from typing import Tuple, List, Optional, Union, Iterable, Dict

import wagascianpy.analysis.spill
import wagascianpy.database.db_record
import wagascianpy.utils.treenames as treenames
import wagascianpy.utils.utils
from wagascianpy.analysis.spill import open_raw_tree
from wagascianpy.database.bsddb import BunchNumber, CTNumber

# ROOT
try:
    import ROOT

    ROOT.PyConfig.IgnoreCommandLineOptions = True
except ImportError:
    ROOT = None

BSD_ERROR_CODE = 1000

_CONVERTION_FACTOR = 0x7FFF
_OFFSET = 1
_SEARCH_WINDOW = 500
_BSD_INTERVAL_OFFSET = 3600  # seconds

MatchedSpill = namedtuple('MatchedSpill', ['WagasciSpill', 'BsdSpill'])


def _set_wagasci_spills(input_file, matched_spills):
    ttree, tfile = open_raw_tree(input_file=input_file,
                                 branch_list=["spill_count", "spill_mode", "fixed_spill_number", "good_spill_flag"],
                                 mode="UPDATE")
    if tfile.GetListOfKeys().Contains(treenames.BSD_TREE_NAME):
        for key in tfile.GetListOfKeys():
            if key.GetName() == treenames.BSD_TREE_NAME:
                tfile.Delete("{};{}".format(treenames.BSD_TREE_NAME, key.GetCycle()))

    friend_tree = ROOT.TTree(treenames.BSD_TREE_NAME, "ROOT tree containing Beam Summary Data related information")
    friend_tree.SetDirectory(tfile)
    ttree.AddFriend(friend_tree)

    empty_bsd_spill = wagascianpy.analysis.spill.SpillFactory.get_spill("bsd")
    array_list = empty_bsd_spill.get_array_list()
    for array_info in array_list:
        friend_tree.Branch(array_info.name, array_info.array, array_info.type_str)

    for event in ttree:
        current_spill_number = event.fixed_spill_number
        current_spill_count = event.spill_count
        current_spill_mode = event.spill_mode
        if current_spill_mode != wagascianpy.analysis.spill.WAGASCI_SPILL_BEAM_MODE:
            matched_spill = None
        else:
            matched_spill = next((matched_spill for matched_spill in matched_spills
                                  if matched_spill.WagasciSpill.spill_number == current_spill_number and
                                  matched_spill.WagasciSpill.spill_count == current_spill_count), None)
        if matched_spill is None:
            bsd_spill = wagascianpy.analysis.spill.SpillFactory.get_spill("bsd")
        else:
            bsd_spill = matched_spill.BsdSpill
        bsd_spill.set_array_list(array_list)
        friend_tree.Fill()

    ttree.SetBranchStatus("*", 1)
    friend_tree.Write("", ROOT.TObject.kWriteDelete)
    tfile.Write("", ROOT.TObject.kWriteDelete)
    tfile.Close()


def _get_wagasci_spills(input_file):
    # type: (str) -> Tuple[List[wagascianpy.analysis.spill.WagasciSpill], int, int]
    """
    Read all the WAGASCI spills contained in the input file into a list of WagasciSpill objects.
    Each element of the list correspond to a single spill.
    :param input_file: path to the input file
    :return: list of WagasciSpill, starting timestamp, stopping timestamp
    """

    ttree, tfile = open_raw_tree(input_file=input_file,
                                 branch_list=["spill_count", "spill_mode", "fixed_spill_number", "good_spill_flag"],
                                 mode="READ")

    assert (ttree.GetUserInfo().FindObject("start_time") not in [ROOT.nullptr, None, 0]), \
        "Start time not found in {} TTree of file {}".format(ttree.GetName(), input_file)
    start_time = ttree.GetUserInfo().FindObject("start_time").GetVal()
    assert (ttree.GetUserInfo().FindObject("stop_time") not in [ROOT.nullptr, None, 0]), \
        "stop time not found in {} TTree of file {}".format(ttree.GetName(), input_file)
    stop_time = ttree.GetUserInfo().FindObject("stop_time").GetVal()
    dif_id = ttree.GetUserInfo().FindObject("dif_id").GetVal()
    print("Run start time %s" % wagascianpy.database.db_record.DBRecord.timestamp2str(start_time))
    print("Run stop time %s" % wagascianpy.database.db_record.DBRecord.timestamp2str(stop_time))
    print("DIF %s" % dif_id)
    regex = re.compile(r'_([\d]+)_ecal_dif_\d+_tree.root')
    match = re.search(regex, input_file)
    run = match.group(1) if match else 0
    wagasci_spills = []
    for event in ttree:
        if event.spill_mode != wagascianpy.analysis.spill.WAGASCI_SPILL_BEAM_MODE:
            continue
        wagasci_spill = wagascianpy.analysis.spill.SpillFactory.get_spill("wagasci")
        wagasci_spill.spill_number = event.fixed_spill_number
        wagasci_spill.spill_count = event.spill_count
        wagasci_spill.converted_spill_number = wagasci_spill.spill_number & _CONVERTION_FACTOR
        wagasci_spill.spill_mode = event.spill_mode
        wagasci_spill.good_spill_flag = event.good_spill_flag
        wagasci_spill.wagasci_run = run
        if wagasci_spill.are_all_defined():
            wagasci_spills.append(wagasci_spill)

    tfile.Close()
    return wagasci_spills, start_time, stop_time


def _check_bsd_file(bsd_record, bsd_repository, file_path):
    # type: (Dict, str, str) -> None
    if not os.path.exists(file_path):
        if bsd_repository is None:
            raise RuntimeError("Please specify a valid BSD local repository")
        file_path = wagascianpy.utils.utils.find_first_match(bsd_record["name"], bsd_repository)
        if file_path is None:
            raise RuntimeError("Please specify a valid BSD local repository")


def get_bsd_spills(bsd_database, bsd_repository, t2krun, start_time, stop_time):
    # type: (str, str, int, int, int) -> List[wagascianpy.analysis.spill.BsdSpill]
    """
    Read all the BSD spills from the BSD repository in the selected time interval
    :param bsd_database: path to BSD database file
    :param bsd_repository: path to the BSD repository directory
    :param t2krun: number of T2K run
    :param start_time: starting timestamp
    :param stop_time: stopping timestamp
    :return:
    """
    bsd_spills = []
    timestamp_start = wagascianpy.database.db_record.DBRecord.datetime2timestamp(start_time) - _BSD_INTERVAL_OFFSET
    timestamp_stop = wagascianpy.database.db_record.DBRecord.datetime2timestamp(stop_time) + _BSD_INTERVAL_OFFSET
    with wagascianpy.database.bsddb.BsdDataBase(bsd_database, bsd_repository, None, t2krun) as db:
        bsd_records = db.get_time_interval(datetime_start=timestamp_start, datetime_stop=timestamp_stop,
                                           include_overlapping=False)
        if not bsd_records:
            RuntimeError("Please specify a valid BSD database")
        for bsd_record in sorted(bsd_records, key=operator.itemgetter("name")):
            file_path = bsd_record["file_path"]
            if not os.path.exists(file_path):
                file_path = os.path.join(bsd_repository, "t2krun{}".format(t2krun),
                                         os.path.basename(bsd_record["file_path"]))
                if not os.path.exists(file_path):
                    file_path = os.path.join(bsd_repository, os.path.basename(bsd_record["file_path"]))
                    if not os.path.exists(file_path):
                        raise RuntimeError(
                            "BSD file {} not found in repository {}".format(bsd_record["file_path"], bsd_repository))
            _check_bsd_file(bsd_record=bsd_record, bsd_repository=bsd_repository, file_path=file_path)
            print('Reading file "{}"'.format(file_path))
            bsd_file = ROOT.TFile(file_path, "READ")
            bsd_tree = bsd_file.Get(treenames.BSD_TREE_NAME)

            bsd_tree.SetBranchStatus("*", 0)
            bsd_tree.SetBranchStatus("spillnum", 1)
            bsd_tree.SetBranchStatus("trg_sec", 1)
            bsd_tree.SetBranchStatus("trg_nano", 1)
            bsd_tree.SetBranchStatus("good_spill_flag", 1)

            ct_pot = bsd_tree.GetListOfBranches().FindObject("ct_pot")
            if ct_pot:
                bsd_tree.SetBranchStatus("ct_pot", 1)
            ct_np = bsd_tree.GetListOfBranches().FindObject("ct_np")
            if ct_np:
                bsd_tree.SetBranchStatus("ct_np", 1)

            for event in bsd_tree:
                # print("Spill number = %s" % event.spillnum)
                # print("POT = %s" % event.ct_pot[BunchNumber.TotalCurrent])
                # print("Is bad spill = %s" % event.good_spill_flag)
                # print("Timestamp = %s" % bsd_tree.trg_sec[TriggerTime.RubidiumClock]

                bsd_spill = wagascianpy.analysis.spill.SpillFactory.get_spill("bsd")
                bsd_spill.bsd_spill_number = int(event.spillnum)
                bsd_spill.converted_spill_number = (bsd_spill.bsd_spill_number + _OFFSET) & _CONVERTION_FACTOR
                bsd_spill.timestamp = float(event.trg_sec[wagascianpy.database.bsddb.TriggerTime.RubidiumClock])
                bsd_spill.timestamp += float(event.trg_nano[wagascianpy.database.bsddb.TriggerTime.RubidiumClock]) / 1e9
                bsd_spill.bsd_good_spill_flag = event.good_spill_flag
                bsd_spill.t2k_run = t2krun
                bsd_spill.main_ring_run = bsd_record.main_ring_run
                bsd_spill.neutrino_daq_run = bsd_record.neutrino_daq_run
                bsd_spill.horn_current = bsd_record.mean_horn_current  # TODO
                bsd_spill.neutrino_mode = bsd_record.neutrino_type

                for i in [i for i in BunchNumber if i != BunchNumber.TotalCurrent]:
                    if ct_pot:
                        bunch_pot = float(event.ct_pot[i])
                    elif ct_np:
                        bunch_pot = float(event.ct_np[CTNumber.Fifth * len(BunchNumber) + i])
                    else:
                        bunch_pot = 0
                    bsd_spill.bunch_pot[i - BunchNumber.First] = bunch_pot
                if ct_pot:
                    bsd_spill.pot = float(event.ct_pot[BunchNumber.TotalCurrent])
                elif ct_np:
                    bsd_spill.pot = float(event.ct_np[CTNumber.Fifth * len(BunchNumber) + BunchNumber.TotalCurrent])
                else:
                    bsd_spill.pot = 0

                if bsd_spill.are_all_defined():
                    bsd_spills.append(bsd_spill)
                else:
                    raise ValueError("Some fields of BSD spill are not initialized")

    return bsd_spills


def _match_spills(wagasci_spills,  # type: List[wagascianpy.analysis.spill.WagasciSpill]
                  bsd_spills,  # type: List[wagascianpy.analysis.spill.BsdSpill]
                  start_time,  # type: int
                  stop_time  # type: int
                  ):
    # type: (...) -> List[MatchedSpill]
    """
    Match the WAGASCI spill list with the BSD spill list and put the matched spills in a new list
    :param wagasci_spills: list of WAGASCI spills
    :param bsd_spills: list of BSD spills
    :param start_time: start timestamp of the lists
    :param stop_time: stop timestamp of the lists
    :return: list of matched spills
    """

    matched_spills = []

    if not wagasci_spills:
        raise ValueError("WAGASCI spill list is empty")
    if not bsd_spills:
        return matched_spills

    if bsd_spills[0].timestamp > start_time:
        ignore_spills = True
        print("[WARNING] first BSD spill %s is after run start %s" % (bsd_spills[0].timestamp, start_time))
    else:
        ignore_spills = False
    if bsd_spills[-1].timestamp < stop_time:
        print("[WARNING] last BSD spill %s is before run stop %s" % (bsd_spills[-1].timestamp, stop_time))

    good_spills = [wagasci_spill for wagasci_spill in wagasci_spills
                   if wagasci_spill.good_spill_flag == wagascianpy.analysis.spill.IS_GOOD_SPILL and
                   wagasci_spill.spill_mode == wagascianpy.analysis.spill.WAGASCI_SPILL_BEAM_MODE]

    found_index = None
    start_index = 0

    if ignore_spills:
        while good_spills:
            if abs(good_spills[0].converted_spill_number - bsd_spills[0].converted_spill_number) > 100:
                good_spills.pop(0)
            else:
                break

    for i, wagasci_spill in enumerate(good_spills):
        if i != 0 and i % 1000 == 0:
            print("Processed {} spills".format(i))
        # In case the previous spill was not found, increase the search window by a factor 10
        start_slice = int(max(start_index - _SEARCH_WINDOW / 2, 0))
        if found_index is None:
            stop_slice = int(min(start_slice + 10 * _SEARCH_WINDOW, sys.maxsize))
        else:
            stop_slice = int(min(start_slice + _SEARCH_WINDOW, sys.maxsize))

        # If the spill is not found, found_index and bsd_spill are set to None
        # Keep in mind that found_index is relative to the start of the slice and not to the start of bsd_spills
        found_index, bsd_spill = _find_spill(wagasci_spill.converted_spill_number,
                                             islice(bsd_spills, start_slice, stop_slice))

        # If the spill was found, set the start index as the found index
        if found_index is not None:
            start_index = int(start_slice + found_index)
            matched_spill = MatchedSpill(wagasci_spill, bsd_spill)
            matched_spills.append(matched_spill)
        else:
            start_index += 1
    return matched_spills


###############################################################################
#                                 find_spill                                  #
###############################################################################

def _find_spill(converted_spill_number,  # type: int
                spills  # type: Union[islice, Iterable[wagascianpy.analysis.spill.BsdSpill]]
                ):
    # type: (...) -> Tuple[Optional[int], Optional[wagascianpy.analysis.spill.BsdSpill]]
    """
    Find a spill with converted spill number in the input list of spills. Returns None in case of failure
    :param converted_spill_number: converted spill number (using the convertion flag)
    :param spills: slice of BSD spills
    :return: index of found spill, found BSD spill with matching converted spill number
    """
    for index, spill in enumerate(spills):
        if spill.converted_spill_number == converted_spill_number:
            return index, spill
    return None, None


###############################################################################
#                             beam_summary_data                               #
###############################################################################

def beam_summary_data(input_path, bsd_database, bsd_repository, t2krun, recursive):
    # type: (str, str, str, int, bool) -> None
    """
    Integrate the beam summary data (BSD) into the WAGASCI decoded data
    :param input_path: path to the tree.root file containing the WAGASCI decoded data or
                       a directory containing those files
    :param bsd_database: path to BSD database file .db
    :param bsd_repository: path to the BSD repository (where the BSD .root files are stored)
    :param t2krun: number of T2K run
    :param recursive: if True all the tree.root files in the input directory are analyzed
    :return: None
    """
    if ROOT is None:
        raise ImportError("No ROOT module was found!")
    if not os.path.exists(input_path):
        raise IOError("Input file %s not found" % input_path)
    input_files = []
    if os.path.isfile(input_path):
        input_files.append(input_path)
    elif os.path.isdir(input_path):
        if recursive:
            for root, dirs, files in os.walk(input_path):
                for file_name in files:
                    if re.search(r'_ecal_dif_([\d]+)_tree.root$', file_name) is not None:
                        input_files.append(os.path.join(root, file_name))
        else:
            for file_name in os.listdir(input_path):
                if re.search(r'_ecal_dif_([\d]+)_tree.root', file_name).groups() is not None:
                    input_files.append(os.path.join(input_path, file_name))

    if not os.path.exists(bsd_database):
        raise IOError("Beam summary data database %s not found" % bsd_database)

    for input_file in input_files:
        print("Start reading WAGASCI spills")
        wagasci_spills, start_time, stop_time = _get_wagasci_spills(input_file)
        print("Finished reading WAGASCI spills")
        print("Start reading BSD spills")
        bsd_spills = get_bsd_spills(bsd_database, bsd_repository, t2krun, start_time, stop_time)
        print("Finished reading BSD spills")
        print("Start WAGASCI-BSD spill matching")
        matched_spills = _match_spills(wagasci_spills, bsd_spills, start_time, stop_time)
        print("Finished WAGASCI-BSD spill matching")
        print("Start writing matched spills")
        _set_wagasci_spills(input_file, matched_spills)
        print("Finished writing matched spills")
