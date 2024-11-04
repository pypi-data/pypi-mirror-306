#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio

"""Script to calibration the gain of the high gain preamp the SPIROC2D ASIC

"""

# Python modules
import argparse
import json
import os
import re
from typing import Dict

import ROOT
from bitarray import bitarray

# WAGASCI modules
from wagascianpy.analysis.analysis import WagasciAnalysis, ThreadWithReturnValue
from wagascianpy.utils.environment import WagasciEnvironment
from wagascianpy.utils.utils import limit_threads, join_threads

PEU_LEVEL = 1
MAX_NB_THREAD_CHAINS = 8
IDAC_FORM = "iDAC%s"
PEU_FORM = "PEU%s"


# ================================================================ #
#                                                                  #
#                        Analysis functions                        #
#                                                                  #
# ================================================================ #

def _gain_decoder(process, run_root_dir, input_dac, peu, threshold_dir, acq_name, dif, n_chips, overwrite_flag):
    # type: (WagasciAnalysis, str, int, int, str, str, int, int, bool) -> ThreadWithReturnValue
    """ wgDecoder for the gain_run.py script """
    peu = int(peu)
    dif = int(dif)
    n_chips = int(n_chips)
    overwrite_flag = bool(overwrite_flag)
    input_raw_file = os.path.join(run_root_dir, IDAC_FORM % input_dac, PEU_FORM % peu, threshold_dir,
                                  "RawData", "%s_ecal_dif_%s.raw" % (acq_name, dif))
    output_dir = os.path.join(run_root_dir, IDAC_FORM % input_dac, PEU_FORM % peu, threshold_dir, "wgDecoder")
    compatibility_mode = False
    return process.spawn("decoder", input_raw_file, "", output_dir, overwrite_flag, compatibility_mode, dif, n_chips)


def _gain_make_hist(process, run_root_dir, input_dac, peu, threshold_dir, acq_name, acq_config_xml, dif):
    # type: (WagasciAnalysis, str, int, int, str, str, str, int) -> ThreadWithReturnValue
    """ wgMakeHist for the gain_run.py script """
    peu = int(peu)
    dif = int(dif)
    input_tree_file = os.path.join(run_root_dir, IDAC_FORM % input_dac, PEU_FORM % peu, threshold_dir,
                                   "wgDecoder", "%s_ecal_dif_%s_tree.root" % (acq_name, dif))
    output_dir = os.path.join(run_root_dir, IDAC_FORM % input_dac, PEU_FORM % peu, threshold_dir, "wgMakeHist")
    flags = bitarray('0' * 9, endian='big')
    flags[7] = True  # dark noise
    flags[4] = True  # charge hit HG
    flags[0] = True  # overwrite
    ul_flags = int(flags.to01(), 2)
    return process.make_hist(input_file=input_tree_file, config_file=acq_config_xml, output_dir=output_dir,
                             ul_flags=ul_flags, dif=dif)


def _gain_gain_calib(process, run_root_dir):
    # type: (WagasciAnalysis, str) -> ThreadWithReturnValue
    """ wgGainCalib for the gain_run.py script """
    output_xml_dir = os.path.join(run_root_dir, "wgGainCalib", "Xml")
    output_img_dir = os.path.join(run_root_dir, "wgGainCalib", "Images")
    return process.gain_calib(input_dir=run_root_dir, output_xml_dir=output_xml_dir, output_img_dir=output_img_dir,
                              print_flag=False)


def _get_idac_dirs(run_root_dir):
    # type: (str) -> Dict[int, str]
    dirs = {}
    for name in [name for name in os.listdir(run_root_dir)
                 if os.path.isdir(os.path.join(run_root_dir, name))]:
        idac = re.findall(r'\d+', name)
        if len(idac) == 1:
            dirs[int(idac[0])] = name
    return dirs


# ============================================================================ #
#                                                                              #
#                                gain_analysis                                 #
#                                                                              #
# ============================================================================ #

def gain_analysis(run, decoder=True, makehist=True, overwrite=False, single_threshold=False):
    # type: (str, bool, bool, bool, bool) -> None
    """ Analyze gain calibration data """

    decoder = bool(decoder)
    makehist = bool(makehist)
    single_threshold = bool(single_threshold)

    # Environmental variables
    env = WagasciEnvironment()
    wagasci_lib = env['WAGASCI_LIBDIR']

    if not os.path.exists(run):
        run = os.path.join(env['WAGASCI_CALIBDATADIR'], run)

    run_name = os.path.basename(run)
    run_root_dir = run

    acq_config_path = os.path.join(run_root_dir, os.path.basename(env['WAGASCI_ACQCONFIGDIR']))
    acq_config_xml = os.path.join(acq_config_path, env['WAGASCI_ACQCONFIGXML'])
    if not os.path.exists(acq_config_xml):
        raise EnvironmentError("Acquisition configuration XML file not found : %s" % acq_config_xml)

    idac_dirs = _get_idac_dirs(run_root_dir)

    if single_threshold:
        threshold_dirs = ["SingleTh"]
    else:
        threshold_dirs = ["LowTh", "MiddleTh", "HighTh"]

    # =========================================================== #
    #                        ANALYZE DATA                         #
    # =========================================================== #

    process = WagasciAnalysis(wagasci_lib)
    topology_string, pointer = process.get_dif_topology(acq_config_xml)
    dif_topology = json.loads(topology_string)
    process.free_topology(pointer)
    process.enable_thread_safety()
    del process

    ###########################################################################
    #                                 decoder                                 #
    ###########################################################################

    # The decoder is completely multithread safe so we can spawn as many threads
    # as the amount of available memory allows

    if decoder:

        threads = []

        for input_dac, idac_dir in idac_dirs.items():
            for threshold_dir in threshold_dirs:
                acq_name = "%s_iDAC%s_PEU%s_%s" % (run_name, input_dac, PEU_LEVEL, threshold_dir)
                for dif in dif_topology:
                    filepath = os.path.join(run_root_dir, idac_dir, PEU_FORM % PEU_LEVEL, threshold_dir,
                                            "wgDecoder", "%s_ecal_dif_%s_tree.root" % (acq_name, dif))
                    if not overwrite and os.path.exists(filepath):
                        tfile = ROOT.TFile(filepath, "READ")
                        if not tfile.IsZombie():
                            print("Skipping %s" % filepath)
                            continue
                        else:
                            print("Removing zombie file %s" % filepath)
                            os.remove(filepath)
                    limit_threads(threads, MAX_NB_THREAD_CHAINS)
                    process = WagasciAnalysis(wagasci_lib)
                    n_chips = len(dif_topology[dif])
                    threads.append(_gain_decoder(process=process, run_root_dir=run_root_dir, input_dac=input_dac,
                                                 peu=PEU_LEVEL, threshold_dir=threshold_dir, acq_name=acq_name,
                                                 dif=dif, n_chips=n_chips, overwrite_flag=overwrite))
                    del process
                # dif loop
            # threshold loop
        # input_dac loop

        # Wait until all the threads have returned
        join_threads(threads)

    ###########################################################################
    #                                make_hist                                #
    ###########################################################################

    if makehist:

        for input_dac in idac_dirs:
            for threshold_dir in threshold_dirs:
                acq_name = "%s_iDAC%s_PEU%s_%s" % (run_name, input_dac, PEU_LEVEL, threshold_dir)
                actual_acq_config_xml = os.path.join(run_root_dir, IDAC_FORM % input_dac, PEU_FORM % PEU_LEVEL,
                                                     threshold_dir, "RawData", "%s.xml" % acq_name)
                for dif in dif_topology:
                    filepath = os.path.join(run_root_dir, IDAC_FORM % input_dac, PEU_FORM % PEU_LEVEL,
                                            threshold_dir, "wgMakeHist", "%s_ecal_dif_%s_hist.root" % (acq_name, dif))
                    if not overwrite and os.path.exists(filepath):
                        tfile = ROOT.TFile(filepath, "READ")
                        if not tfile.IsZombie():
                            print("Skipping %s" % filepath)
                            continue
                        else:
                            print("Removing zombie file %s" % filepath)
                            os.remove(filepath)
                    process = WagasciAnalysis(wagasci_lib)
                    result = _gain_make_hist(process=process, run_root_dir=run_root_dir, input_dac=input_dac,
                                             peu=PEU_LEVEL, threshold_dir=threshold_dir, acq_name=acq_name,
                                             acq_config_xml=actual_acq_config_xml, dif=dif)
                    if result != 0:
                        print("wgMakeHist returned error code %s" % result)
                        exit(result)
                    del process
                # dif loop
            # threshold loop
        # input_dac loop

    ###########################################################################
    #                             gain_calib                                 #
    ###########################################################################

    process = WagasciAnalysis(wagasci_lib)
    result = _gain_gain_calib(process=process, run_root_dir=run_root_dir)
    del process
    if result != 0:
        print("wgGainCalib returned error code %s" % result)
        exit(result)


###############################################################################
#                                     MAIN                                    #
###############################################################################

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(usage='use "python %(prog)s --help" for more information',
                                     argument_default=None, description='Analyze the gain calibration data')

    PARSER.add_argument('-f', '--run', metavar='<run name or path>', type=str, required=True,
                        help='Name or path of the run to analyze. If only the run name is given the run must be inside '
                             'the ${WAGASCI_CALIBDATADIR} folder.')
    PARSER.add_argument('-d', '--disable-decoder', dest='decoder', action='store_false',
                        required=False, default=True, help="Disable the wgDecoder.")
    PARSER.add_argument('-m', '--disable-makehist', dest='makehist', action='store_false',
                        required=False, default=True, help="Disable the wgMakeHist.")
    PARSER.add_argument('-r', '--overwrite', dest='overwrite', action='store_true',
                        required=False, default=False, help="Overwrite flag.")

    ARGS = PARSER.parse_args()

    RUN = ARGS.run
    DECODER = ARGS.decoder
    MAKEHIST = ARGS.makehist
    OVERWRITE = ARGS.overwrite

    gain_analysis(run=RUN, decoder=DECODER, makehist=MAKEHIST, overwrite=OVERWRITE)
