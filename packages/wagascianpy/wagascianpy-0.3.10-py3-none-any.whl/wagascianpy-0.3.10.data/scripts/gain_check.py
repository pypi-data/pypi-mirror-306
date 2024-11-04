#!python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio

"""Check the gain of the SPIROC2D ASIC (method 1)"""

# Python modules
import argparse
import json
import os
import textwrap

import ROOT
from bitarray import bitarray

# WAGASCI modules
from wagascianpy.analysis.analysis import WagasciAnalysis, ThreadWithReturnValue
from wagascianpy.utils.environment import WagasciEnvironment
from wagascianpy.utils.utils import limit_threads, join_threads

MAX_NB_THREAD_CHAINS = 8
PEU_LEVEL = 1
IDAC_FORM = "iDACOPTIMIZE"
PEU_FORM = "PEU%s"


# ================================================================ #
#                                                                  #
#                        Analysis functions                        #
#                                                                  #
# ================================================================ #

def _gain_decoder(process, run_root_dir, peu, threshold, acq_name, dif, n_chips, overwrite_flag):
    # type: (WagasciAnalysis, str, int, str, str, int, int, bool) -> ThreadWithReturnValue
    """ wgDecoder for the gain_run.py script """
    peu = int(peu)
    dif = int(dif)
    n_chips = int(n_chips)
    overwrite_flag = bool(overwrite_flag)
    input_raw_file = os.path.join(run_root_dir, IDAC_FORM, PEU_FORM % peu, threshold,
                                  "RawData", "{}_ecal_dif_{}.raw".format(acq_name, dif))
    output_dir = os.path.join(run_root_dir, IDAC_FORM, PEU_FORM % peu, threshold, "wgDecoder")
    compatibility_mode = False
    return process.spawn("decoder", input_raw_file, "", output_dir, overwrite_flag, compatibility_mode,
                         dif, n_chips)


def _gain_make_hist(process, run_root_dir, peu, threshold, acq_name, acq_config_xml, dif):
    # type: (WagasciAnalysis, str, int, str, str, str, int) -> ThreadWithReturnValue
    """ wgMakeHist for the gain_check.py script """
    dif = int(dif)
    input_tree_file = os.path.join(run_root_dir, IDAC_FORM, PEU_FORM % peu, threshold, "wgDecoder",
                                   "{}_ecal_dif_{}_tree.root".format(acq_name, dif))
    output_dir = os.path.join(run_root_dir, IDAC_FORM, PEU_FORM % peu, threshold, "wgMakeHist")
    flags = bitarray('0' * 9, endian='big')
    flags[0] = True  # overwrite
    flags[4] = True  # charge hit HG
    flags[7] = True  # Dark noise
    ul_flags = int(flags.to01(), 2)
    return process.make_hist(input_file=input_tree_file, config_file=acq_config_xml, output_dir=output_dir,
                             ul_flags=ul_flags, dif=dif)


def _gain_gain_check(process, run_root_dir, acq_config_xml, only_wallmrd, only_wagasci):
    # type: (WagasciAnalysis, str, str, bool, bool) -> ThreadWithReturnValue
    """ wgGainCalib for the gain_check.py script """
    only_wallmrd = bool(only_wallmrd)
    only_wagasci = bool(only_wagasci)
    output_dir = os.path.join(run_root_dir, "wgGainCheck")
    return process.gain_check(input_dir=run_root_dir, xml_config_file=acq_config_xml, output_img_dir=output_dir,
                              only_wallmrd=only_wallmrd, only_wagasci=only_wagasci)


def _gain_gain_tune(process, run_root_dir, acq_config_xml, only_wallmrd, only_wagasci):
    # type: (WagasciAnalysis, str, str, bool, bool) -> ThreadWithReturnValue
    """ wgGainCalib for the gain_check.py script """
    only_wallmrd = bool(only_wallmrd)
    only_wagasci = bool(only_wagasci)
    output_dir = os.path.join(run_root_dir, "wgGainTune")
    return process.gain_tune(input_dir=run_root_dir, xml_config_file=acq_config_xml, output_img_dir=output_dir,
                             only_wallmrd=only_wallmrd, only_wagasci=only_wagasci)


# ============================================================================ #
#                                                                              #
#                                gain_analysis                                 #
#                                                                              #
# ============================================================================ #

def gain_check_analysis(run, only_wallmrd=False, only_wagasci=False, decoder=True, makehist=True,
                        overwrite=False, single_threshold=False):
    """ Analyze gain check data """

    only_wallmrd = bool(only_wallmrd)
    only_wagasci = bool(only_wagasci)
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

        for threshold_dir in threshold_dirs:
            for dif in dif_topology:
                if only_wagasci and int(dif) < 4:
                    continue
                if only_wallmrd and int(dif) >= 4:
                    continue
                acq_name = "{}_{}_{}".format(run_name, PEU_FORM % PEU_LEVEL, threshold_dir)
                filepath = os.path.join(run_root_dir, IDAC_FORM, PEU_FORM % PEU_LEVEL, threshold_dir, "wgDecoder",
                                        "{}_ecal_dif_{}_tree.root".format(acq_name, dif))
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
                threads.append(_gain_decoder(process=process, run_root_dir=run_root_dir, peu=PEU_LEVEL,
                                             threshold=threshold_dir, acq_name=acq_name, dif=dif, n_chips=n_chips,
                                             overwrite_flag=overwrite))
                del process
            # dif loop
        # threshold loop

        # Wait until all the threads have returned
        join_threads(threads)

    ###########################################################################
    #                                make_hist                                #
    ###########################################################################

    if makehist:

        for threshold_dir in threshold_dirs:
            for dif in dif_topology:
                if only_wagasci and int(dif) < 4:
                    continue
                if only_wallmrd and int(dif) >= 4:
                    continue
                acq_name = "{}_{}_{}".format(run_name, PEU_FORM % PEU_LEVEL, threshold_dir)
                filepath = os.path.join(run_root_dir, IDAC_FORM, PEU_FORM % PEU_LEVEL, threshold_dir, "wgMakeHist",
                                        "{}_ecal_dif_{}_hist.root".format(acq_name, dif))
                if not overwrite and os.path.exists(filepath):
                    tfile = ROOT.TFile(filepath, "READ")
                    if not tfile.IsZombie():
                        print("Skipping %s" % filepath)
                        continue
                    else:
                        print("Removing zombie file %s" % filepath)
                        os.remove(filepath)
                process = WagasciAnalysis(wagasci_lib)
                result = _gain_make_hist(process=process, run_root_dir=run_root_dir, peu=PEU_LEVEL,
                                         threshold=threshold_dir, acq_name=acq_name, acq_config_xml=acq_config_xml,
                                         dif=dif)
                if result != 0:
                    print("wgMakeHist returned error code %d" % result)
                    exit(result)
                del process
            # dif loop
        # threshold loop

    ###########################################################################
    #                             gain_check                                  #
    ###########################################################################

    process = WagasciAnalysis(wagasci_lib)
    threshold_dir = "SingleTh" if single_threshold else "MiddleTh"
    acq_name = "{}_{}_{}".format(run_name, PEU_FORM % PEU_LEVEL, threshold_dir)
    acq_config_xml = os.path.join(run_root_dir, IDAC_FORM, PEU_FORM % PEU_LEVEL, threshold_dir, "RawData",
                                  "{}.xml".format(acq_name))
    result = _gain_gain_check(process=process, run_root_dir=run_root_dir, acq_config_xml=acq_config_xml,
                              only_wallmrd=only_wallmrd, only_wagasci=only_wagasci)
    del process
    if result != 0:
        print("wgGainCheck returned error code %d" % result)
        exit(result)

    process = WagasciAnalysis(wagasci_lib)
    result = _gain_gain_tune(process=process, run_root_dir=run_root_dir, acq_config_xml=acq_config_xml,
                             only_wallmrd=only_wallmrd, only_wagasci=only_wagasci)
    del process
    if result != 0:
        print("wgGainTune returned error code %d" % result)
        exit(result)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(usage='use "python %(prog)s --help" for more information',
                                     argument_default=None, description='Check and tune the gain calibration')

    PARSER.add_argument('-f', '--run', metavar='<run name or path>', type=str, required=True,
                        help='Name or path of the run to analyze. If only the run name is given the run must be inside '
                             'the ${WAGASCI_CALIBDATADIR} folder.')
    PARSER.add_argument('--only-wallmrd', dest='only_wallmrd', action='store_true', help="Only analyze WallMRD data")
    PARSER.add_argument('--only-wagasci', dest='only_wagasci', action='store_true', help="Only analyze WAGASCI data")
    PARSER.add_argument('-d', '--disable-decoder', dest='decoder', action='store_false',
                        required=False, default=True, help="Disable the wgDecoder.")
    PARSER.add_argument('-m', '--disable-makehist', dest='makehist', action='store_false',
                        required=False, default=True, help="Disable the wgMakeHist.")
    PARSER.add_argument('-r', '--overwrite', dest='overwrite', action='store_true',
                        required=False, default=False, help="Overwrite flag.")
    PARSER.add_argument('-s', '--single-threshold', dest='single_threshold', action='store_true',
                        required=False, default=False, help=textwrap.dedent('''
                        If not set it is assumed that the low threshold LowTh, high threshold HighTh and middle
                        threshold MiddleTh folders are present. If set only the SingleTh folder is analyzed.
                        '''))

    ARGS = PARSER.parse_args()

    RUN = ARGS.run
    DECODER = ARGS.decoder
    MAKEHIST = ARGS.makehist
    OVERWRITE = ARGS.overwrite
    ONLY_WAGASCI = ARGS.only_wagasci
    ONLY_WALLMRD = ARGS.only_wallmrd
    SINGLE_THRESHOLD = ARGS.single_threshold

    gain_check_analysis(run=RUN, only_wallmrd=ONLY_WALLMRD, only_wagasci=ONLY_WAGASCI,
                        decoder=DECODER, makehist=MAKEHIST, overwrite=OVERWRITE, single_threshold=SINGLE_THRESHOLD)
