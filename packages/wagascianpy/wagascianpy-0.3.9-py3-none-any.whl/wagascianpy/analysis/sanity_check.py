#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Pintaudi Giorgio

import json

from typing import Optional

# ROOT
try:
    # noinspection PyPackageRequirements
    import ROOT

    ROOT.PyConfig.IgnoreCommandLineOptions = True
except ImportError:
    ROOT = None

from wagascianpy.utils.utils import parse_input_files
import wagascianpy.database.wagascidb
import wagascianpy.utils.treenames as treenames

SANITY_CHECK_ERROR_CODE = 1002

_TREE_FRIENDS = [treenames.BSD_TREE_NAME, treenames.FSN_TREE_NAME, treenames.PEU_TREE_NAME,
                 treenames.TIME_NS_TREE_NAME, treenames.FLAGS_TREE_NAME]


def sanity_check(input_path, wagasci_database, run_number=None):
    # type: (str, str, Optional[int]) -> None
    """
    Check the sanity of the decoded ROOT files. First it is checked if all the files are present by comparing the
    file list with the topology string. Then it is checked if all the TTrees inside the ROOT files are present.
    Finally it is checked if the number of spills in the trees is consistent.
    :param input_path: path to the input file or folder
    :param wagasci_database: path to the WAGASCI run database
    :param run_number: run number (optional)
    :return: True if all the sanity checks pass, False if one sanity check fails. In case of failure the following
    sanity checks are skipped.
    """
    if ROOT is None:
        raise ImportError("No ROOT module was found!")

    try:
        run_number, detectors = parse_input_files(input_path=input_path, run_number=run_number,
                                                  tree_friends=_TREE_FRIENDS)
    except ValueError as error:
        raise RuntimeError('Run number = {}, Input path = "{}" : {}'.format(run_number, input_path, error))

    with wagascianpy.database.wagascidb.WagasciDataBase(db_location=wagasci_database) as db:
        run_records = db.get_run_interval(run_number_start=run_number, only_good=False)
        if len(run_records) != 1:
            raise RuntimeError("Run {} not found in database".format(run_number))
        run_record = run_records[0]
        try:
            topology = json.loads(run_record.topology)
        except ValueError as error:
            raise RuntimeError('Error when parsing topology string "{}": {}'.format(topology, error))
        for dif_id in topology.keys():
            dif_id = int(dif_id)
            if not detectors.has_dif(dif_id):
                raise RuntimeError('Run number = {}, Input path = "{}" : DIF {} not found'.format(
                    run_number, input_path, dif_id))
            dif = detectors.get_dif(dif_id)
            num_spills = dif.get_tree().GetEntries()
            for friend in _TREE_FRIENDS:
                if not dif.has_friend(friend):
                    raise RuntimeError('Run number = {}, Input path = "{}", DIF = {} : tree "{}" not found'.format(
                        run_number, input_path, dif_id, friend))
                tree = dif.get_friend(friend)
                if tree.GetEntries() != num_spills:
                    raise RuntimeError('Run number = {}, Input path = "{}", DIF = {}, tree  = "{}" : num entries {} is '
                                       'different from {}'.format(run_number, input_path, dif_id, friend,
                                                                  tree.GetEntries(), num_spills))
